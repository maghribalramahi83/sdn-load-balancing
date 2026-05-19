By Maghrib Alramahi - Iraq

```python
"""
ML-QTLB: Hybrid Machine Learning and Queueing-Theory
         Based Load Balancing for SDN
─────────────────────────────────────────────────────
Model    : Random Forest (RF) Classifier
Scheduler: M/M/1 Queueing Theory (QT)
Platform : POX Controller + Mininet + OpenFlow
─────────────────────────────────────────────────────
"""

import joblib
import random
import time
import threading
import psutil

from urllib.parse import urlparse, parse_qs
from pox.core import core
import pox.openflow.libopenflow_01 as of

from pox.lib.packet.ethernet import ethernet, ETHER_BROADCAST
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.arp import arp
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.util import str_to_bool, dpid_to_str

log = core.getLogger("ML_QTLB")

# ══════════════════════════════════════════════
# Constants
# ══════════════════════════════════════════════
FLOW_IDLE_TIMEOUT   = 10
FLOW_MEMORY_TIMEOUT = 60
STARVATION_THRESHOLD = 15   # T: seconds before promoting Low-priority


# ══════════════════════════════════════════════
# Memory Entry (unchanged from original)
# ══════════════════════════════════════════════
class MemoryEntry(object):
    def __init__(self, server, first_packet, client_port):
        self.server       = server
        self.first_packet = first_packet
        self.client_port  = client_port
        self.refresh()

    def refresh(self):
        self.timeout = time.time() + FLOW_MEMORY_TIMEOUT

    @property
    def is_expired(self):
        return time.time() > self.timeout

    @property
    def from_client_to_server(self):
        ethp = self.first_packet
        ipp  = ethp.find('ipv4')
        tcpp = ethp.find('tcp')
        return ipp.srcip, ipp.dstip, tcpp.srcport, tcpp.dstport

    @property
    def from_server_to_client(self):
        ethp = self.first_packet
        ipp  = ethp.find('ipv4')
        tcpp = ethp.find('tcp')
        return self.server, ipp.srcip, tcpp.dstport, tcpp.srcport


# ══════════════════════════════════════════════
# ML-QTLB Main Class
# ══════════════════════════════════════════════
class iplb(object):

    # ─────────────────────────────────────────
    # Stage 4: RF Classifier (replaces old KNN)
    # ─────────────────────────────────────────
    class RFClassifier(object):
        """
        Random Forest Classifier for traffic class prediction.
        Class 1 = Low-priority  (Light traffic)
        Class 2 = High-priority (Heavy traffic)
        Hyperparameters: criterion=entropy, n_estimators=80,
                         max_depth=4, min_samples_split=7,
                         random_state=0
        Accuracy: 95.3%
        """
        def __init__(self, model_path):
            self.model = joblib.load(model_path)
            log.info("ML-QTLB: RF Classifier loaded from %s" % model_path)

        def predict_class(self, features):
            """
            Predict traffic class from 8 normalized features.
            Features: [Packets, Bytes, Pkts_A→B, Bytes_A→B,
                       Pkts_B→A, Bytes_B→A, Bits/s_A→B, Bits/s_B→A]
            Returns: 1 (Low) or 2 (High)
            """
            predicted_class = self.model.predict([features])[0]
            log.debug("RF predicted class: %s" % predicted_class)
            return predicted_class

    # ─────────────────────────────────────────
    # Starvation Prevention (Anti-Starvation)
    # ─────────────────────────────────────────
    class StarvationGuard(object):
        """
        Aging-based mechanism to prevent starvation
        of Low-priority (Class 1) requests.
        If t_wait(r) >= T → promote r to High-priority (Class 2)
        """
        def __init__(self, threshold=STARVATION_THRESHOLD):
            self.T        = threshold      # Aging threshold (seconds)
            self.registry = {}             # request_key → arrival_time

        def register(self, key):
            """Register arrival time for a new Low-priority request."""
            self.registry[key] = time.time()

        def should_promote(self, key):
            """
            Check if waiting time has exceeded threshold T.
            Returns True if request should be promoted.
            """
            arrival = self.registry.get(key, None)
            if arrival is None:
                return False
            t_wait = time.time() - arrival
            if t_wait >= self.T:
                log.info("Starvation prevention: promoting request %s "
                         "(waited %.1fs >= T=%.1fs)" % (key, t_wait, self.T))
                return True
            return False

        def remove(self, key):
            self.registry.pop(key, None)

    # ─────────────────────────────────────────
    # Stage 5: QT Scheduler (M/M/1)
    # ─────────────────────────────────────────
    class QTScheduler(object):
        """
        M/M/1 Queueing Theory based server weight computation.
        For each server Sk:
          λk = incoming_requests / elapsed_time
          μk = completed_requests / elapsed_time
          ρk = λk / μk
          Wk = ρk / (μk × (1 - ρk))   if ρk < 1
               ∞                        otherwise
        Routing: S* = argmin(Wk)
        """
        def __init__(self, servers):
            self.servers    = servers
            # Counters per server
            self.incoming   = {s: 0   for s in servers}   # λ numerator
            self.completed  = {s: 0   for s in servers}   # μ numerator
            self.start_time = {s: time.time() for s in servers}
            self.Wk         = {s: 0.0 for s in servers}

        def record_incoming(self, server):
            """Call when a new request is sent to server."""
            self.incoming[server] = self.incoming.get(server, 0) + 1

        def record_completed(self, server):
            """Call when a request is completed by server."""
            self.completed[server] = self.completed.get(server, 0) + 1

        def compute_weights(self, live_servers):
            """
            Compute Wk for all live servers.
            Returns dict: {server_ip: Wk}
            """
            weights = {}
            for sk in live_servers:
                elapsed = max(time.time() - self.start_time.get(sk, time.time()), 0.001)

                # λk: arrival rate
                lam = self.incoming.get(sk, 0) / elapsed

                # μk: service rate
                mu  = self.completed.get(sk, 0) / elapsed

                # ρk: utilization
                if mu > 0:
                    rho = lam / mu
                else:
                    rho = 0.0

                # Wk: expected system time
                if rho < 1.0 and mu > 0:
                    Wk = rho / (mu * (1.0 - rho))
                else:
                    Wk = float('inf')   # saturated server

                weights[sk] = Wk
                log.debug("QT | Server %s | λ=%.3f | μ=%.3f | "
                          "ρ=%.3f | W=%.4f" % (sk, lam, mu, rho, Wk))

            self.Wk = weights
            return weights

        def select_server(self, live_servers):
            """
            S* = argmin(Wk) for k in live_servers
            Returns the server IP with minimum expected system time.
            """
            weights = self.compute_weights(live_servers)
            if not weights:
                return None

            best = min(weights, key=weights.get)
            log.info("QT selected: %s  (W=%.4f)" % (best, weights[best]))
            return best

    # ─────────────────────────────────────────
    # __init__
    # ─────────────────────────────────────────
    def __init__(self, connection, service_ip, servers=[]):
        self.service_ip = IPAddr(service_ip)
        self.servers    = [IPAddr(a) for a in servers]
        self.con        = connection
        self.mac        = self.con.eth_addr

        # Stage 4: RF Classifier
        self.rf = self.RFClassifier('rf_mlqtlb_model.pkl')

        # Stage 5: QT Scheduler
        self.qt = self.QTScheduler(self.servers)

        # Starvation Prevention
        self.sg = self.StarvationGuard(threshold=STARVATION_THRESHOLD)

        # Network state
        self.live_servers       = {}   # IP → (MAC, port)
        self.memory             = {}   # flow_key → MemoryEntry
        self.outstanding_probes = {}   # IP → expire_time
        self.total_connection   = {str(ip): 0 for ip in servers}

        # Monitoring
        self.cpu_usages    = {}
        self.memory_usages = {}
        self._start_monitoring()

        # Probe config
        self.probe_cycle_time = 5
        self.arp_timeout      = 3

        try:
            self.log = log.getChild(dpid_to_str(self.con.dpid))
        except:
            self.log = log

        self._do_probe()

    # ─────────────────────────────────────────
    # ARP Probing (unchanged)
    # ─────────────────────────────────────────
    def _do_expire(self):
        t = time.time()
        for ip, expire_at in list(self.outstanding_probes.items()):
            if t > expire_at:
                self.outstanding_probes.pop(ip, None)
                if ip in self.live_servers:
                    self.log.warn("Server %s down", ip)
                    del self.live_servers[ip]

        memory = self.memory.copy()
        self.memory.clear()
        for key, val in memory.items():
            if not val.is_expired:
                self.memory[key] = val
            else:
                self.qt.record_completed(val.server)

    def _do_probe(self):
        self._do_expire()
        server = self.servers.pop(0)
        self.servers.append(server)
        r = arp()
        r.hwtype   = r.HW_TYPE_ETHERNET
        r.prototype= r.PROTO_TYPE_IP
        r.opcode   = r.REQUEST
        r.hwdst    = ETHER_BROADCAST
        r.protodst = server
        r.hwsrc    = self.mac
        r.protosrc = self.service_ip
        e = ethernet(type=ethernet.ARP_TYPE,
                     src=self.mac, dst=ETHER_BROADCAST)
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

    # ─────────────────────────────────────────
    # ML-QTLB: _pick_server (QT-based)
    # ─────────────────────────────────────────
    def _pick_server(self, key, inport):
        """
        Stage 5: Select optimal server using QT Scheduler.
        S* = argmin(Wk) for all live servers.
        """
        if not self.live_servers:
            return None

        best = self.qt.select_server(self.live_servers)

        if best is None:
            # Fallback: pick server with lowest CPU if QT fails
            best = min(self.live_servers,
                       key=lambda s: self.cpu_usages.get(s, float('inf')))
            log.warn("QT fallback: selected by CPU → %s" % best)

        return best

    # ─────────────────────────────────────────
    # ML-QTLB: _extract_features
    # ─────────────────────────────────────────
    def _extract_features(self, packet, inport):
        """
        Extract 8 normalized features from the incoming packet.
        Features: [Packets, Bytes, Pkts_A→B, Bytes_A→B,
                   Pkts_B→A, Bytes_B→A, Bits/s_A→B, Bits/s_B→A]
        Returns a list of 8 float values in range [0, 1].
        """
        try:
            ipp  = packet.find('ipv4')
            tcpp = packet.find('tcp')

            pkt_len   = len(packet.pack()) if packet else 64
            src_port  = tcpp.srcport if tcpp else 0
            dst_port  = tcpp.dstport if tcpp else 0

            # Normalized features (Min-Max scaled to [0,1])
            features = 