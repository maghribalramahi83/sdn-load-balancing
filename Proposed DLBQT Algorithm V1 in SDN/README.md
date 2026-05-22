# DLBQT: Queueing-Theory-Based Dynamic Load Balancing Model for SDN

---

## 📌 Overview

This folder contains the complete asset package for the **DLBQT** model,
including figures, key result tables, and Python code for the proposed
queueing-theory-based dynamic load balancing algorithm in SDN.

**DLBQT** integrates:
- Centralized SDN control using the POX controller in a Mininet environment.
- Queueing-theory parameters (arrival rate, service rate, utilization, weight) for server selection.
- Dynamic load balancing across **homogeneous** and **heterogeneous** server environments.
- Statistical evaluation using effect size, confidence intervals, and normality tests.

---

## 📂 Folder Contents

### 🏗️ Architectural & Methodology Diagrams (4 Figures)

| File | Description |
|------|-------------|
| `fig01_sdn_architecture.png` | **Figure 1 – Architecture of SDN Layers** — conceptual three-layer SDN structure (application, control, data) used as background for DLBQT. |
| `fig02_dlbqt_diagram.png` | **Figure 2 – Diagram of the Proposed DLBQT Algorithm** — high-level block diagram of the DLBQT mechanism inside the SDN controller and its interaction with the data plane. |
| `fig03_dlbqt_flowchart.png` | **Figure 3 – Stages / Flowchart of the Proposed DLBQT Model** — sequential steps: traffic arrival, parameter calculation (λ, μ, ρ, W), overloaded-server protection, and server selection. |
| `fig04_network_topology.png` | **Figure 4 – Proposed Network Topology** — Mininet single-switch topology with multiple hosts and two servers managed by the POX controller. |

---

### 🖼️ Implementation & Analysis Figures (Performance & Statistics)

| File | Description |
|------|-------------|
| `fig05_waiting_time_comparison.png` | **Figure 5 – Average Waiting Time Comparison** — DLBQT vs. LCPU, LRAM, LC in homogeneous and heterogeneous environments. |
| `fig06_service_time_comparison.png` | **Figure 6 – Average Service Time Comparison** — DLBQT vs. baseline algorithms, showing mixed behavior across environments. |
| `fig07_execution_time_comparison.png` | **Figure 7 – Average Execution Time Comparison** — DLBQT vs. baseline algorithms, highlighting execution time reduction. |
| `fig08_effect_size_waiting_time.png` | **Figure 8 – Effect Size of Average Waiting Time** — Cohen’s d for DLBQT vs. LCPU, LRAM, LC. |
| `fig09_effect_size_service_time.png` | **Figure 9 – Effect Size of Average Service Time** — Cohen’s d for service time comparisons. |
| `fig10_effect_size_execution_time.png` | **Figure 10 – Effect Size of Execution Time** — Cohen’s d for execution time in both environments. |
| `fig11_statistical_waiting_time.png` | **Figure 11 – Statistical Analysis of Average Waiting Time** — mean, std, skewness, normality test, confidence intervals. |
| `fig12_statistical_service_time.png` | **Figure 12 – Statistical Analysis of Average Service Time** — statistical summary across environments. |
| `fig13_statistical_execution_time.png` | **Figure 13 – Statistical Analysis of Average Execution Time** — distribution and 95% confidence intervals. |

---

### 📊 Key Result Tables (10 CSV Files)

| File | Manuscript Table | Description |
|------|------------------|-------------|
| `table01_server_specifications.csv` | Table 1 | Server specifications in homogeneous and heterogeneous scenarios. |
| `table02_waiting_time_homogeneous.csv` | Table 2 | Average waiting time in homogeneous environment (LCPU, LRAM, LC, DLBQT). |
| `table03_waiting_time_heterogeneous.csv` | Table 3 | Average waiting time in heterogeneous environment. |
| `table04_service_time_homogeneous.csv` | Table 4 | Average service time in homogeneous environment. |
| `table05_service_time_heterogeneous.csv` | Table 5 | Average service time in heterogeneous environment. |
| `table06_execution_time_homogeneous.csv` | Table 6 | Average execution time in homogeneous environment. |
| `table07_execution_time_heterogeneous.csv` | Table 7 | Average execution time in heterogeneous environment. |
| `table08_effect_size_waiting_time.csv` | Table 8 | Cohen’s d for average waiting time. |
| `table09_effect_size_service_time.csv` | Table 9 | Cohen’s d for average service time. |
| `table10_effect_size_execution_time.csv` | Table 10 | Cohen’s d for execution time. |

> 💾 All CSV files should be placed under `tables/`.

---

### 🐍 Python Files (DLBQT Algorithm & Parameters)

| File | Description |
|------|-------------|
| `DLBQT_Proposed_Algorithm.py` | **Python implementation of the proposed DLBQT algorithm** running in the SDN controller, including server selection logic based on queueing-theory parameters. |
| `DLBQT_Parameter_Calculations.py` | **Parameter calculation module** — computes arrival rate (λ), service rate (μ), utilization (ρ), and weight (W) for each server. |
| `DLBQT_Performance_Metrics.py` | **Performance metrics script** — calculates waiting time, service time, execution time, and percentage improvement used in Tables 2–7. |
| `DLBQT_Statistical_Analysis.py` | **Statistical analysis script** — implements effect size (Cohen’s d), mean, standard deviation, p-values, skewness, and confidence intervals (matching Tables 8–10). |

> 📁 Place all Python files in a `code/` directory: `dlbqt_algorithm/code/`.

---

## ⚙️ DLBQT Pipeline

The DLBQT pipeline (corresponding to the manuscript’s methodology) includes:

1. **Traffic Generation & Arrival** — real traffic files based on Facebook data center traces (16 files, 1 KB–6.8 MB).
2. **Queueing-Theory Parameter Computation** — for each server:
   - Arrival rate \( \lambda \)
   - Service rate \( \mu \)
   - Utilization factor \( \rho = \lambda / \mu \)
   - Weight \( W \) approximating total time in the system.
3. **Overload Handling** — overloaded servers are assigned a very high default weight and excluded from new assignments.
4. **Dynamic Server Selection** — selecting the server with minimum weight.
5. **Performance Measurement** — waiting time, service time, execution time for each algorithm and environment.
6. **Statistical Analysis** — effect size, normality tests, and confidence intervals.

---

## 📈 Results Summary (Link to Baseline Paper)

The DLBQT results are compared against three dynamic load-balancing algorithms (LCPU, LRAM, LC) previously proposed in:

> **Reference [20]**  
> Maghrib A. M. Alrammahi, *Optimizing Server-Side Dynamic Load Balancing in SDN Using Novel Algorithms Based on CPU, RAM, and Connection Metrics*,  
> **International Journal of Advanced Research in Computer Science**, 2026, 17(1), pp. 21–27.  
> DOI: [http://dx.doi.org/10.26483/ijarcs.v17i1.7401](http://dx.doi.org/10.26483/ijarcs.v17i1.7401)

DLBQT achieves:
- Waiting time reductions of **7.47–9.42% (homogeneous)** and **9.09–16.92% (heterogeneous)**.
- Execution time improvements of **8.96–17.15% (homogeneous)** and **8.60–23.48% (heterogeneous)**.
- Mixed but statistically interpretable behavior for service time across environments.

(Full numerical values are stored in the CSV tables under `tables/`.)

---

## 🛠️ Experimental Environment

| Parameter | Value |
|----------|-------|
| Emulator | Mininet |
| OS | Linux (Ubuntu) |
| Controller | POX |
| Switch | OpenFlow switch (single-switch topology) |
| Servers | 2 servers (homogeneous & heterogeneous setups) |
| Metrics | Average waiting time, average service time, average execution time |
| Statistical Tool | OriginPro 2026 (95% CI, Cohen’s d, normality tests) |

---

## 🚀 How to Use This Folder

1. Browse the `figures/` directory for all manuscript figures (1–13).
2. Use the `tables/` directory for CSV versions of Tables 1–10 (for plotting or re-analysis).
3. Use the `code/` directory for:
   - Running or studying the DLBQT algorithm.
   - Recomputing queueing parameters and performance metrics.
   - Replicating statistical analyses.

---

## 📖 Citation

If you use these assets or the DLBQT implementation in your research, please cite the corresponding DLBQT paper (once published) and reference [20] for baseline algorithms.

---

## 📬 Contact

**Maghrib Abidalreda Maky Alrammahi**  
University of Kufa — ITRDC, Najaf, Iraq  
📧 maghrib.alramahi@uokufa.edu.iq

---

## 📜 License

MIT License
