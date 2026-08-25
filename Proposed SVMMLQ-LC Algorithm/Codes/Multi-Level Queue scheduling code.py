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
"""
 (MLQ) multilevel queue scheduling code
"""

import random

class PriorityQueue:
    def __init__(self):
        self.queue = [[], []] # Two queues: 0 and 1
        self._counter = 0
        self._threshold = 3  # process 3 priority 0 packets before servicing next priority 1 packet

    def push(self, packet, priority):
        self.queue[priority].append(packet)
        print(f"Packet: {packet}, Priority: {priority}")
        print(f"-----------------------")
    def pop(self):
        # Check if the threshold has been reached
        if self._counter == self._threshold:
            self._counter = 0  # Reset counter if priority 1 packet is processed
            if self.queue[1]:  # Retrieve packets with priority 1 if available
                return 1, self.queue[1].pop(0)
            else:
                return 0, self.queue[0].pop(0)
        elif self.queue[0]:  # Retrieve packets with priority 0 if available
            self._counter += 1
            return 0, self.queue[0].pop(0)
        elif self.queue[1]:  # Retrieve packets with priority 1 if no packets with priority 0
            return 1, self.queue[1].pop(0)
        else:
            return None, None  # Return None if both queues are empty


def generate_packet():
    packet = "Packet"
    priority = random.randint(0, 1)
    return packet, priority
pq = PriorityQueue()

# Add packets to the queue with random priorities
for i in range(10):
    packet, priority = generate_packet()
    pq.push(packet, priority)

# Retrieve and print packets and their priorities from the queue
while True:
    priority, packet = pq.pop()
    if packet is None:
        break
    print(f"Packet: {packet}, Priority: {priority}")
