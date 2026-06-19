"""
Copyright (c) 2026
Maghrib Abidalreda Maky Alrammahi
Email: maghrib.alramahi@uokufa.edu.iq

This code is part of the ML-QTLB research project and was prepared solely by
Maghrib Abidalreda Maky Alrammahi.

Any use of this code, in whole or in part, in research, academic publication,
software development, reproduction, or derivative work should acknowledge the
author by citing the published ML-QTLB paper and referencing the official
project GitHub repository.

Official GitHub repository:
https://github.com/maghribalramahi83/sdn-load-balancing
"""

import time
import random
import joblib

from pox.core import core
from pox.lib.packet.ethernet import ethernet, ETHER_BROADCAST
from pox.lib.packet.arp import arp
from pox.lib.addresses import IPAddr
from pox.lib.util import dpid_to_str
import pox.openflow.libopenflow_01 as of

log = core.getLogger("ml_qtlb")

FLOW_IDLE_TIMEOUT = 10
FLOW_MEMORY_TIMEOUT = 60
STARVATION_THRESHOLD = 3.0


class MemoryEntry(object):
    def __init__(self, server, first_packet, client_port, priority):
        self.server = server
        self.first_packet = first_packet
        self.client_port = client_port
        self.priority = priority
        self.created_at = time.time()
        self.refresh()

    def refresh(self):
        self.timeout = time.time() + FLOW_MEMORY_TIMEOUT

    @property
    def is_expired(self):
        return time.time() > self.timeout

    @property
    def waiting_time(self):
        return time.time() - self.created_at

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


class MLQTLB(object):
    class RFClassifier(object):
        def __init__(self, model_path):
            self.model = joblib.load(model_path)

        def get_priority(self, features):
            return int(self.model.predict([features])[0])

    class PriorityQueue(object):
        def __init__(self, threshold=STARVATION_THRESHOLD):
            self.high_priority = []
            self.low_priority = []
            self.threshold = threshold

        def push(self, event, priority):
            item = {'event': event, 'priority': priority, 'timestamp': time.time()}
            if priority == 1:
                self.high_priority.append(item)
            else:
                self.low_priority.append(item)

        def pop(self):
            now = time.time()
            for item in list(self.low_priority):
                if now - item['timestamp'] >= self.threshold:
                    self.low_priority.remove(item)
                    item['priority'] = 1
                    return item
            if self.high_priority:
                return self.high_priority.pop(0)
            if self.low_priority:
                return self.low_priority.pop(0)
            return None

    def __init__(self, connection, service_ip, servers=None, model_path='rf_model.pkl'):
        if servers is None:
            servers = []

        self.service_ip = IPAddr(service_ip)
        self.servers = [IPAddr(a) for a in servers]
        self.rf_classifier = self.RFClassifier(model_path)
        self.priority_queue = self.PriorityQueue()
        self.con = connection
        self.mac = self.con.eth_addr
        self.live_servers = {}

        try:
            self.log = log.getChild(dpid_to_str(self.con.dpid))
        except Exception:
            self.log = log

        self.outstanding_probes = {}
        self.probe_cycle_time = 5
        self.arp_timeout = 3
        self.memory = {}

        self.server_stats = {}
        for ip in self.servers:
            self.server_stats[ip] = {
                'connections': 0,
                'lambda': 0.0,
                'mu': 100.0,
                'rho': 0.0,
                'weight': 0.0,
                'last_update': time.time()
            }

        self._do_probe()

    def _do_expire(self):
        t = time.time()

        for ip, expire_at in list(self.outstanding_probes.items()):
            if t > expire_at:
                self.outstanding_probes.pop(ip, None)
                if ip in self.live_servers:
                    self.log.warn('Server %s down', ip)
                    del self.live_servers[ip]

        memory = self.memory.copy()
        self.memory.clear()
        for key, val in memory.items():
            if not val.is_expired:
                self.memory[key] = val
            else:
                server = val.server
                if server in self.server_stats and self.server_stats[server]['connections'] > 0:
                    self.server_stats[server]['connections'] -= 1
                    self._update_server_weight(server)

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

    @property
    def _probe_wait_time(self):
        r = self.probe_cycle_time / float(len(self.servers))
        return max(.25, r)

    def _extract_features(self, packet):
        tcpp = packet.find('tcp')
        packet_length = len(packet.raw) if packet.raw is not None else 0
        tcp_payload = len(tcpp.payload) if tcpp and tcpp.payload is not None else 0
        return [
            round(min(packet_length / 1500.0, 1.0), 3),
            round(min(tcp_payload / 1460.0, 1.0), 3),
            round(random.uniform(0.05, 0.50), 3),
            round(random.uniform(0.05, 0.50), 3),
            round(random.uniform(0.05, 0.50), 3),
            round(random.uniform(0.05, 0.50), 3),
            round(random.uniform(0.05, 0.50), 3),
            round(random.uniform(0.05, 0.50), 3),
        ]

    def _update_server_weight(self, server):
        stats = self.server_stats[server]
        now = time.time()
        elapsed = max(now - stats['last_update'], 0.001)
        stats['last_update'] = now
        stats['lambda'] = stats['connections'] / elapsed
        stats['mu'] = max(1.0, 100.0 - (stats['connections'] * 5.0))
        stats['rho'] = min(stats['lambda'] / stats['mu'], 0.99)
        stats['weight'] = stats['rho'] / (stats['mu'] * (1.0 - stats['rho']))

    def _pick_server(self):
        available = [s for s in self.live_servers.keys() if s in self.server_stats]
        if not available:
            return None
        for server in available:
            self._update_server_weight(server)
        return min(available, key=lambda s: self.server_stats[s]['weight'])

    def _install_flow_to_server(self, event, packet, entry, inport):
        mac, port = self.live_servers[entry.server]
        actions = [
            of.ofp_action_dl_addr.set_dst(mac),
            of.ofp_action_nw_addr.set_dst(entry.server),
            of.ofp_action_output(port=port)
        ]
        match = of.ofp_match.from_packet(packet, inport)
        msg = of.ofp_flow_mod(command=of.OFPFC_ADD,
                              idle_timeout=FLOW_IDLE_TIMEOUT,
                              hard_timeout=of.OFP_FLOW_PERMANENT,
                              data=event.ofp,
                              actions=actions,
                              match=match)
        self.con.send(msg)

    def _install_reverse_flow(self, event, packet, entry, inport):
        actions = [
            of.ofp_action_dl_addr.set_src(self.mac),
            of.ofp_action_nw_addr.set_src(self.service_ip),
            of.ofp_action_output(port=entry.client_port)
        ]
        match = of.ofp_match.from_packet(packet, inport)
        msg = of.ofp_flow_mod(command=of.OFPFC_ADD,
                              idle_timeout=FLOW_IDLE_TIMEOUT,
                              hard_timeout=of.OFP_FLOW_PERMANENT,
                              data=event.ofp,
                              actions=actions,
                              match=match)
        self.con.send(msg)

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
            if arpp:
                if arpp.opcode == arpp.REPLY and arpp.protosrc in self.outstanding_probes:
                    del self.outstanding_probes[arpp.protosrc]
                    if self.live_servers.get(arpp.protosrc, (None, None)) != (arpp.hwsrc, inport):
                        self.live_servers[arpp.protosrc] = (arpp.hwsrc, inport)
                        self.log.info('Server %s up', arpp.protosrc)
                return
            return drop()

        ipp = packet.find('ipv4')

        if ipp.srcip in self.servers:
            key = ipp.srcip, ipp.dstip, tcpp.srcport, tcpp.dstport
            entry = self.memory.get(key)
            if entry is None:
                self.log.debug('No client for %s', key)
                return drop()
            entry.refresh()
            self._install_reverse_flow(event, packet, entry, inport)
            return

        if ipp.dstip == self.service_ip:
            features = self._extract_features(packet)
            self.log.info('Extracted features: %s', features)

            priority = self.rf_classifier.get_priority(features)
            self.log.info('RF predicted priority: %s', priority)

            self.priority_queue.push(event, priority)
            queued_item = self.priority_queue.pop()
            if queued_item is None:
                return drop()

            key = ipp.srcip, ipp.dstip, tcpp.srcport, tcpp.dstport
            entry = self.memory.get(key)

            if entry is None or entry.server not in self.live_servers:
                if len(self.live_servers) == 0:
                    self.log.warn('No servers available')
                    return drop()

                server = self._pick_server()
                if server is None:
                    return drop()

                self.log.debug('Directing traffic to %s', server)
                entry = MemoryEntry(server, packet, inport, queued_item['priority'])
                self.memory[entry.from_client_to_server] = entry
                self.memory[entry.from_server_to_client] = entry
                self.server_stats[server]['connections'] += 1
                self._update_server_weight(server)

            entry.refresh()
            self._install_flow_to_server(event, packet, entry, inport)
            return

        return drop()


_dpid = None


def launch(ip, servers, model_path='rf_model.pkl'):
    servers = servers.replace(',', ' ').split()
    servers = [IPAddr(x) for x in servers]
    ip = IPAddr(ip)

    from proto.arp_responder import launch as arp_launch
    arp_launch(eat_packets=False, **{str(ip): True})

    import logging
    logging.getLogger('proto.arp_responder').setLevel(logging.WARN)

    def _handle_ConnectionUp(event):
        global _dpid
        if _dpid is None:
            log.info('ML-QTLB RF/QT Load Balancer Ready')
            core.registerNew(MLQTLB, event.connection, IPAddr(ip), servers, model_path)
            _dpid = event.dpid

        if _dpid != event.dpid:
            log.warn('Ignoring switch %s', event.connection)
        else:
            log.info('Load balancing enabled on %s', event.connection)
            core.MLQTLB.con = event.connection
            event.connection.addListeners(core.MLQTLB)

    core.openflow.addListenerByName('ConnectionUp', _handle_ConnectionUp)