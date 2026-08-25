"""
Copyright (c) 2026
Maghrib Abidalreda Maky Alrammahi
Email: maghrib.alramahi@uokufa.edu.iq

This code is part of the SVNMLQ-LC research project and was prepared solely by
Maghrib Abidalreda Maky Alrammahi.

Any use of this code, in whole or in part, in research, academic publication,
software development, reproduction, or derivative work should acknowledge the
author by citing the published ML-QTLB paper and referencing the official
project GitHub repository.

Official GitHub repository:
https://github.com/maghribalramahi83/sdn-load-balancing
""" 

import numpy as np
import pandas as pd

from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

from pox.core import core
from pox.lib.packet.ethernet import ethernet, ETHER_BROADCAST
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.arp import arp
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.util import str_to_bool, dpid_to_str
import pox.openflow.libopenflow_01 as of


class PriorityQueue:
    def __init__(self):
        self.queue = [[], []]  # Two queues: 0 and 1
        self._counter = 0
        self._threshold = 3  # process 3 priority 0 packets before servicing next priority 1 packet

    def push(self, packet, priority):
        self.queue[priority].append(packet)
        print(f"Packet: {packet}, Priority: {priority}")

    def pop(self):
        if self._counter == self._threshold:
            self._counter = 0
            if self.queue[1]:
                return 1, self.queue[1].pop(0)
            else:
                return 0, self.queue[0].pop(0)
        elif self.queue[0]:
            self._counter += 1
            return 0, self.queue[0].pop(0)
        elif self.queue[1]:
            return 1, self.queue[1].pop(0)
        else:
            return None, None


class LeastConnection(object):
    def __init__(self):
        self.connections = {}
        self.pq = PriorityQueue()

    def _handle_ConnectionUp(self, event):
        self.connections[event.connection.dpid] = {}

    def _handle_ConnectionDown(self, event):
        del self.connections[event.dpid]

    def _handle_PacketIn(self, event):
        dst_ip = event.parsed.find('ipv4').dstip
        server = self.choose_server(dst_ip)
        priority, packet = self.pq.pop()
        if packet is not None:
            if priority == 0:
                self.send_high_priority_packet(event, server)
            else:
                self.send_packet(event, server)
                

    def choose_server(self, dst_ip):
        min_connections = None
        chosen_server = None
        for server, connections in self.connections.items():
            if min_connections is None or len(connections) < min_connections:
                min_connections = len(connections)
                chosen_server = server
        self.connections[chosen_server][dst_ip] = True
        return chosen_server

    def send_packet(self, event, server):
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_TABLE))
        event.connection.send(msg)

    def send_high_priority_packet(self, event, server):
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_NORMAL))
        event.connection.send(msg)

    def get_priority(self):
        dataset = pd.read_csv('E:\\my dataset cleaning data - K Means.csv')
        X = dataset.iloc[:, 0:6]
        y = dataset.iloc[:, 6]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        clf = SVC(C=1, kernel='linear', max_iter=100, gamma='auto')
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        return int(y_pred[0])

def launch():
    # Create and launch POX component
    core.registerNew(LeastConnection)
