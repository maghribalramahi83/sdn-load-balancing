"""
DLBQT: Queueing-Theory-Based Dynamic Load Balancing Algorithm for SDN

Original algorithm design:
Dr. Maghrib A. M. Alrammahi
Mohammed Fadhil Mohammed 

The DLBQT algorithmic design, decision logic, and methodological formulation
presented in this file were originally developed by Dr. Maghrib A. M. Alrammahi and Mohammed Fadhil Mohammed.
This implementation documents the proposed model for research transparency
and reproducibility.

Unauthorized removal of this attribution is not permitted.
""" 


from pox.core import core
import pox
log = core.getLogger("iplb")
from pox.lib.packet.ethernet import ethernet, ETHER_BROADCAST
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.arp import arp
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.util import str_to_bool, dpid_to_str
import pox.openflow.libopenflow_01 as of
import time
import random

FLOW_IDLE_TIMEOUT = 10
FLOW_MEMORY_TIMEOUT = 10  # نافذة زمنية لتحديث البيانات

class MemoryEntry(object):
    def __init__(self, server, first_packet, client_port):
        self.server = server
        self.first_packet = first_packet
        self.client_port = client_port
        self.refresh()

    def refresh(self):
        self.timeout = time.time() + FLOW_MEMORY_TIMEOUT

    @property
    def is_expired(self):
        return time.time() > self.timeout

    @property
    def from_client_to_server(self):
        ethp = self.first_packet
        ipp = ethp.find('ipv4')
        tcpp = ethp.find('tcp')
        return ipp.srcip, ipp.dstip, tcpp.srcport, tcpp.dstport

    @property
    def from_server_to_client(self):
        ethp = self.first_packet
        ipp = ethp.find('ipv4')
        tcpp = ethp.find('tcp')
        return self.server, ipp.srcip, tcpp.dstport, tcpp.srcport

class iplb(object):
    def __init__(self, connection, service_ip, servers=[]):
        self.service_ip = IPAddr(service_ip)
        self.servers = [IPAddr(a) for a in servers]
        self.con = connection
        self.mac = self.con.eth_addr
        self.live_servers = {}  # IP -> (MAC, port)
        self.outstanding_probes = {}  # IP -> expire_time
        self.probe_cycle_time = 5
        self.arp_timeout = 3
        self.arrivals = {server: 0 for server in servers}
        self.completions = {server: 0 for server in servers}
        self.time_window_start = time.time()
        self.arrivals_history = {server: [] for server in servers}
        self.completions_history = {server: [] for server in servers}
        self.memory = {}
        self._do_probe()

    def _update_rates(self):
        current_time = time.time()
        time_elapsed = max(current_time - self.time_window_start, 1.0)
        self.rates = {}
        for server in self.servers:
            self.arrivals_history[server].append(self.arrivals[server])
            self.completions_history[server].append(self.completions[server])
            avg_arrivals = sum(self.arrivals_history[server][-10:]) / len(self.arrivals_history[server][-10:])
            avg_completions = sum(self.completions_history[server][-10:]) / len(self.completions_history[server][-10:])
            lambda_ = avg_arrivals / time_elapsed
            mu = max(avg_completions / time_elapsed, 0.1)
            p = lambda_ / mu if mu != 0 else 0
            self.rates[server] = {"lambda": lambda_, "mu": mu, "p": p}
            log.debug(f"Server {server}: λ={lambda_:.8f}, μ={mu:.8f}, p={p:.8f}")

        self.arrivals = {server: 0 for server in self.servers}
        self.completions = {server: 0 for server in self.servers}
        self.time_window_start = current_time

    def _pick_server(self, key, inport):
        if not self.live_servers:
            return None
        self._update_rates()
        best_server = None
        min_w = float('inf')
        selected_server = None  # لتخزين السيرفر النهائي المختار

        for server in self.live_servers:
            rates = self.rates.get(server, {"lambda": 0, "mu": 0, "p": 0})
            p = rates["p"]
            mu = rates["mu"]
            try:
                w = p / (mu * (1 - p)) if p < 1 else 1000.0
            except:
                w = 1000.0
            if w < min_w:
                min_w = w
                best_server = server

        selected_server = best_server or self.servers[0]
        rates = self.rates.get(selected_server, {"lambda": 0, "mu": 0, "p": 0})
        p = rates["p"]
        mu = rates["mu"]
        w = p / (mu * (1 - p)) if p < 1 else 1000.0
        log.info(f"The best server is {selected_server} | λ={rates['lambda']:.8f}, μ={mu:.8f}, p={p:.8f}, W={w:.8f}")
        return selected_server

    def _do_probe(self):
        self._do_expire()
        server = self.servers.pop(0)
        self.servers.append(server)
        r = arp()
        r.hwtype = r.HW_TYPE_ETHERNET
        r.prototype = r.PROTO_TYPE_IP
        r.opcode = r.REQUEST
        r.hwdst = ETHER_BROADCAST
        r.protodst = server
        r.hwsrc = self.mac
        r.protosrc = self.service_ip
        e = ethernet(type=ethernet.ARP_TYPE, src=self.mac, dst=ETHER_BROADCAST)
        e.set_payload(r)
        msg = of.ofp_packet_out()
        msg.data = e.pack()
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        msg.in_port = of.OFPP_NONE
        self.con.send(msg)
        self.outstanding_probes[server] = time.time() + self.arp_timeout
        core.callDelayed(self._probe_wait_time, self._do_probe)

    def _do_expire(self):
        t = time.time()
        for ip, expire_at in list(self.outstanding_probes.items()):
            if t > expire_at:
                self.outstanding_probes.pop(ip, None)
                if ip in self.live_servers:
                    log.warn(f"Server {ip} down")
                    del self.live_servers[ip]

    @property
    def _probe_wait_time(self):
        return max(0.25, self.probe_cycle_time / float(len(self.servers)))

    def _handle_PacketIn(self, event):
        inport = event.port
        packet = event.parsed

        def drop():
            if event.ofp.buffer_id is not None:
                msg = of.ofp_packet_out(data=event.ofp)
                self.con.send(msg)
            return None

        tcpp = packet.find('tcp')
        if not tcpp:
            arpp = packet.find('arp')
            if arpp and arpp.opcode == arpp.REPLY:
                if arpp.protosrc in self.outstanding_probes:
                    del self.outstanding_probes[arpp.protosrc]
                    if (self.live_servers.get(arpp.protosrc, (None, None)) !=
                            (arpp.hwsrc, inport)):
                        self.live_servers[arpp.protosrc] = (arpp.hwsrc, inport)
                        log.info(f"Server {arpp.protosrc} up")
            return

        ipp = packet.find('ipv4')
        if ipp.srcip in self.servers:
            key = ipp.srcip, ipp.dstip, tcpp.srcport, tcpp.dstport
            entry = self.memory.get(key)
            if entry:
                self.completions[entry.server] = max(self.completions[entry.server] + 1, 1)
                actions = [
                    of.ofp_action_dl_addr.set_src(self.mac),
                    of.ofp_action_nw_addr.set_src(self.service_ip),
                    of.ofp_action_output(port=entry.client_port)
                ]
                match = of.ofp_match.from_packet(packet, inport)
                msg = of.ofp_flow_mod(
                    command=of.OFPFC_ADD,
                    idle_timeout=FLOW_IDLE_TIMEOUT,
                    data=event.ofp,
                    actions=actions,
                    match=match
                )
                self.con.send(msg)
        elif ipp.dstip == self.service_ip:
            key = ipp.srcip, ipp.dstip, tcpp.srcport, tcpp.dstport
            entry = self.memory.get(key)
            if entry is None or entry.server not in self.live_servers:
                if not self.live_servers:
                    log.warn("No servers available!")
                    return drop()
                server = self._pick_server(key, inport)
                if server is None:
                    log.warn("No eligible servers available!")
                    return drop()
                entry = MemoryEntry(server, packet, inport)
                self.memory[entry.from_client_to_server] = entry
                self.memory[entry.from_server_to_client] = entry
                self.arrivals[server] = max(self.arrivals[server] + 1, 1)
                # تسجيل توجيه الطلب مع المعاملات
                rates = self.rates.get(server, {"lambda": 0, "mu": 0, "p": 0})
                p = rates["p"]
                mu = rates["mu"]
                w = p / (mu * (1 - p)) if p < 1 else 1000.0

            entry.refresh()
            mac, port = self.live_servers[entry.server]
            actions = [
                of.ofp_action_dl_addr.set_dst(mac),
                of.ofp_action_nw_addr.set_dst(entry.server),
                of.ofp_action_output(port=port)
            ]
            match = of.ofp_match.from_packet(packet, inport)
            msg = of.ofp_flow_mod(
                command=of.OFPFC_ADD,
                idle_timeout=FLOW_IDLE_TIMEOUT,
                data=event.ofp,
                actions=actions,
                match=match
            )
            self.con.send(msg)

_dpid = None

def launch(ip, servers):
    servers = servers.replace(",", " ").split()
    servers = [IPAddr(x) for x in servers]
    ip = IPAddr(ip)
    from proto.arp_responder import launch as arp_launch
    arp_launch(eat_packets=False, **{str(ip): True})
    import logging
    logging.getLogger("proto.arp_responder").setLevel(logging.WARN)
    def _handle_ConnectionUp(event):
        global _dpid
        if _dpid is None:
            log.info("IP Load Balancer Ready.")
            core.registerNew(iplb, event.connection, IPAddr(ip), servers)
            _dpid = event.dpid
        if _dpid != event.dpid:
            log.warn(f"Ignoring switch {event.connection}")
        else:
            log.info(f"Load Balancing on {event.connection}")
            core.iplb.con = event.connection
            event.connection.addListeners(core.iplb)
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
