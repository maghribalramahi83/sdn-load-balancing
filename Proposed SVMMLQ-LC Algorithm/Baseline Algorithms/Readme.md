# Baseline Load-Balancing Algorithms

This folder contains the four baseline load-balancing algorithms used for comparison with the proposed SVMMLQ-LC framework in the manuscript:

> **SVMMLQ-LC: An Intelligent Machine Learning-Based Load-Balancing Framework with Multi-Level Queue Scheduling and Least-Connection Selection for Software-Defined Networking**

The baseline algorithms were implemented in the same POX/OpenFlow and Mininet-based SDN environment used for the proposed model. They provide conventional server-selection strategies for evaluating response time, processing time, load-distribution behavior, and other performance measures.

## Baseline Algorithms

### 1. `R-Algorithm.py`

Implements the **Random** load-balancing algorithm.

For each new TCP flow, the controller randomly selects one available live server from the server pool. This method does not consider the current number of active server connections, traffic characteristics, queue state, or server workload.

**Selection rule:**

```text
Select one live server randomly.
```

---

### 2. `RR-Algorithm.py`

Implements the **Round Robin (RR)** load-balancing algorithm.

The controller assigns successive incoming TCP flows to available servers in cyclic order. After the last server is selected, the algorithm returns to the first server and continues the same sequence.

**Selection rule:**

```text
Server 1 → Server 2 → Server 3 → Server 1 → ...
```

---

### 3. `WRR-Algorithm.py`

Implements the **Weighted Round Robin (WRR)** load-balancing algorithm.

The controller assigns incoming flows according to predefined server weights. In the reported implementation, the scheduling sequence gives Server 1 a larger allocation than Servers 2 and 3.

**Selection rule used in the implementation:**

```text
Server 1 → Server 1 → Server 2 → Server 3 → repeat
```

This corresponds to the relative weight pattern:

```text
Server 1 : Server 2 : Server 3 = 2 : 1 : 1
```

---

### 4. `LC-Algorithm.py`

Implements the **Least-Connection (LC)** load-balancing algorithm.

For each new TCP flow, the controller selects the available server with the smallest current number of active connections. Connection counts are updated when new flows are assigned and reduced when remembered flows expire.

**Selection rule:**

```text
Select the server with the minimum number of active connections.
```

Mathematically:

```text
Selected server = arg min (active connections per server)
```

## Common SDN Functions

All baseline implementations include common POX/OpenFlow functions required for the controlled Mininet testbed:

- Detection of available servers through ARP probes.
- Monitoring of server liveness.
- Processing of TCP PacketIn events.
- Installation of OpenFlow forwarding rules.
- Forward and reverse flow mapping between clients and servers.
- Temporary storage of flow information.
- Flow expiration and connection-state updates.

## Experimental Context

The baseline algorithms were evaluated under the same controlled SDN topology, HTTP traffic-generation procedure, server pool, traffic loads, and performance-measurement process used for the proposed SVMMLQ-LC model.

The comparison is intended to evaluate the added effect of integrating:

- SVM-based traffic classification.
- Threshold-based multi-level queue scheduling.
- Starvation prevention for lower-priority traffic.
- Least-Connection server selection.

## Requirements

The code requires a compatible POX controller and Mininet/OpenFlow environment.

Main requirements include:

```text
Python
POX controller
OpenFlow 1.0
Mininet
Open vSwitch
```

Before execution, verify the service IP address, server IP addresses, network topology, and POX module paths according to the local testbed configuration.

## Reproducibility Notes

- The algorithms are baseline implementations used for controlled comparison.
- Server addresses and POX launch parameters may need to be adapted to the local Mininet topology.
- Results may vary if traffic workloads, server configuration, timeouts, software versions, or network conditions differ from those reported in the manuscript.
- The baseline files retain the original implementation structure used in the experiments.

## Citation and Attribution

The baseline implementations are used for comparison in the SVMMLQ-LC experimental study. The files retain their original source and copyright notices where applicable.

If you use or refer to the experimental comparison, please cite the associated manuscript and repository:

M. A. M. Alrammahi, “SVMMLQ-LC: Proposed Algorithm – Datasets, Source Code, and Experimental Figures,” GitHub repository, May 2026. Available:  
https://github.com/maghribalramahi83/sdn-load-balancing/tree/main/Proposed%20SVMMLQ-LC%20Algorithm
