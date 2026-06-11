#  A Queueing Theory-Based Dynamic Load Balancing Algorithm for Optimizing Software-Defined Networking Performance in Homogeneous and Heterogeneous Environments

***

## 📌 Overview

This repository contains the complete asset package for the **DLBQT** algorithm,
including figures, key result tables, and Python code for the proposed
queueing-theory-based dynamic load balancing algorithm in SDN.

**DLBQT** (Dynamic Load Balancing based on Queueing Theory) integrates:
- Centralized SDN control using the **Python OpenFlow eXtensible (POX)** controller in a **Mininet** environment.
- Queueing-theory parameters (arrival rate λ, service rate μ, utilization ρ, weight W) for server selection based on the **M/M/1 queueing model**.
- Dynamic load balancing across **homogeneous** and **heterogeneous** server environments.
- Statistical evaluation using **Cohen's d effect size**, **95% confidence intervals**, and **normality tests** (OriginPro 2026).
- Comparison against three dynamic baselines: **Least CPU (LCPU)**, **Least RAM (LRAM)**, and **Least Connection (LC)**.

***

## 📂 Folder Contents

### 🏗️ Architectural & Methodology Diagrams (Figures 1–5)

| File | Description |
|------|-------------|
| `fig01_proposed_model_architecture.png` | **Figure 1 – Architectural Design of the Proposed Model** — three-layer SDN structure (application, control, data) with DLBQT integrated in the control layer. |
| `fig02_dlbqt_diagram.png` | **Figure 2 – Diagram of the Proposed DLBQT Algorithm** — block diagram showing queueing-theory-based decision mechanism in the SDN controller. |
| `fig03_dlbqt_flowchart_conceptual.png` | **Figure 3 – Simplified Conceptual Flow of DLBQT** — sequential steps: traffic arrival, parameter computation (λ, μ, ρ, W), overload protection, and server selection. |
| `fig04_dlbqt_flowchart_full.png` | **Figure 4 – Full Flowchart of the Proposed DLBQT Algorithm** — detailed flowchart including QoS measurement and request completion cycle. |
| `fig05_network_topology.png` | **Figure 5 – Proposed Network Topology in SDN** — Mininet single-switch topology with hosts (host1–host4), one central switch, two servers, and POX controller. |

***

### 📊 Performance Result Figures (Figures 6–8)

| File | Description |
|------|-------------|
| `fig06_packet_loss.png` | **Figure 6 – Packet Loss in Homogeneous and Heterogeneous Environments** — DLBQT vs. LCPU, LC, LRAM at 1,000 / 100,000 / 1,000,000 requests with ±1 SD error bars. |
| `fig07_response_time.png` | **Figure 7 – Response Time in Homogeneous and Heterogeneous Environments** — comparison across all load levels and both environments. |
| `fig08_throughput.png` | **Figure 8 – Throughput in Homogeneous and Heterogeneous Environments** — DLBQT achieves highest throughput at medium and high loads. |

***

### 📈 Statistical Analysis Figures (Figures 9–17)

| File | Description |
|------|-------------|
| `fig09_effect_size_packet_loss.png` | **Figure 9 – Effect Size (Cohen's d) for Packet Loss** — large d values (≥ 1.32) for DLBQT vs. all baselines in both environments. |
| `fig10_effect_size_response_time.png` | **Figure 10 – Effect Size (Cohen's d) for Response Time** — large d values (≥ 1.35) confirming substantial latency reduction. |
| `fig11_effect_size_throughput.png` | **Figure 11 – Effect Size (Cohen's d) for Throughput** — large d values (≥ 1.05) indicating stable throughput improvement. |
| `fig12_stats_packet_loss_homo.png` | **Figure 12 – Statistical Analysis of Packet Loss Improvement – Homogeneous** — mean, SD, 95% CI, normality test. |
| `fig13_stats_packet_loss_hetero.png` | **Figure 13 – Statistical Analysis of Packet Loss Improvement – Heterogeneous** — distribution and confidence intervals. |
| `fig14_stats_response_time_homo.png` | **Figure 14 – Statistical Analysis of Response Time Improvement – Homogeneous** — mean 7.78%, SD 0.84, 95% CI [5.70–9.85]. |
| `fig15_stats_response_time_hetero.png` | **Figure 15 – Statistical Analysis of Response Time Improvement – Heterogeneous** — mean 8.69%, SD 2.38, 95% CI [2.78–14.6]. |
| `fig16_stats_throughput_homo.png` | **Figure 16 – Statistical Analysis of Throughput Improvement – Homogeneous** — distribution across three load levels. |
| `fig17_stats_throughput_hetero.png` | **Figure 17 – Statistical Analysis of Throughput Improvement – Heterogeneous** — mean 14.63%, SD 5.35, 95% CI [2.17–27.09]. |

> 📁 Place all figure files under `figures/`.

***

### 📋 Key Result Tables (CSV Files)

| File | Manuscript Table | Description |
|------|------------------|-------------|
| `table01_abbreviations.csv` | Table 1 | Abbreviations used in the paper (SDN, DLBQT, LC, LCPU, LRAM, QoS, CI, SD, M/M/1, R). |
| `table02_modules_parameters.csv` | Table 2 | Main modules and parameters of the DLBQT controller (Traffic Monitoring, Utilization Estimator, Weight Calculator, QoS Collector). |
| `table03_symbols_units.csv` | Table 3 | Symbols and units used in the DLBQT algorithm (λ, μ, ρ, W, T_win). |
| `table04_server_specs.csv` | Table 4 | Server specifications for homogeneous (12 cores / 32 GB RAM each) and heterogeneous (3 cores/8 GB vs. 1 core/3 GB) environments. |
| `table05_algorithm_config.csv` | Table 5 | Configuration of load balancing algorithms: LC, LCPU, LRAM, DLBQT — decision metrics and update mechanisms. |
| `table06_experimental_config.csv` | Table 6 | Unified experimental configuration (Mininet, POX, Ubuntu 22.04, Intel Core i7-10850H, 32 GB RAM, 512 GB SSD). |
| `table07_packet_loss_homo.csv` | Table 7 | Packet loss (%) in homogeneous environment — DLBQT improves over LCPU by 37.5%, LC by 26.4%, LRAM by 29.2%. |
| `table08_packet_loss_hetero.csv` | Table 8 | Packet loss (%) in heterogeneous environment — DLBQT improves over LCPU by 36.8%, LC by 28.2%, LRAM by 39.2%. |
| `table09_response_time_homo.csv` | Table 9 | Response time (s) in homogeneous environment — DLBQT improves over LCPU by 8.61%, LC by 7.78%, LRAM by 6.94%. |
| `table10_response_time_hetero.csv` | Table 10 | Response time (s) in heterogeneous environment — DLBQT improves over LCPU by 11.4%, LC by 7.75%, LRAM by 6.93%. |
| `table11_throughput_homo.csv` | Table 11 | Throughput (bits/s) in homogeneous environment — DLBQT improves over LCPU by 4.34%, LC by 1.33%, LRAM by 6.61%. |
| `table12_throughput_hetero.csv` | Table 12 | Throughput (bits/s) in heterogeneous environment — DLBQT improves over LCPU by 17.1%, LC by 8.4%, LRAM by 18.4%. |
| `table13_effect_size_packet_loss.csv` | Table 13 | Cohen's d for packet loss — homogeneous: d = 1.32–1.43; heterogeneous: d = 1.40–1.60 (all Large). |
| `table14_effect_size_response_time.csv` | Table 14 | Cohen's d for response time — homogeneous: d = 1.35–1.42; heterogeneous: d = 1.48–1.55 (all Large). |
| `table15_effect_size_throughput.csv` | Table 15 | Cohen's d for throughput — homogeneous: d = 1.05–1.15; heterogeneous: d = 1.10–1.30 (all Large). |
| `table16_stats_packet_loss.csv` | Table 16 | Descriptive statistics for packet loss improvement — mean, SD, 95% CI, normality p-value. |
| `table17_stats_response_time.csv` | Table 17 | Descriptive statistics for response time improvement across environments. |
| `table18_stats_throughput.csv` | Table 18 | Descriptive statistics for throughput improvement across environments. |

> 💾 Place all CSV files under `tables/`.

***

### 🐍 Python Code Files

| File | Description |
|------|-------------|
| `DLBQT_Proposed_Algorithm.py` | **Proposed DLBQT algorithm** — full implementation running inside the POX SDN controller. Includes per-server queueing parameter tracking (λ, μ, ρ, W), penalty weight logic (W = 1000 when ρ ≥ 1), and server selection by minimum W with deterministic tie-breaking. |
| `homogeneous_server.py` | **Homogeneous server environment setup** — Mininet topology and server configuration for two servers with identical specifications (Intel i7-10850H, 12 cores, 32 GB RAM each). Includes traffic generation from 16 real-world Facebook data center trace files (1 KB–6.8 MB). |
| `heterogeneous_server.py` | **Heterogeneous server environment setup** — Mininet topology and server configuration for two servers with different capacities (Server 1: 3 cores / 8 GB RAM; Server 2: 1 core / 3 GB RAM). Same traffic generation mechanism with fixed random seed for reproducibility. |

> 📁 Place all Python files under `code/`.

***

## ⚙️ DLBQT Algorithm Pipeline

The DLBQT pipeline (corresponding to the manuscript's methodology — Section 4) operates as follows:

1. **Traffic Arrival** — real-world traffic traces from Facebook data centers (16 files, 1 KB–6.8 MB); hosts request files repeatedly using pseudo-random permutation with fixed seed.
2. **Parameter Computation** — for each server at every routing decision:
   - Arrival rate: λ = (avg. arrivals over last 10 windows) / T_win
   - Service rate: μ = (avg. completions over last 10 windows) / T_win
   - Utilization: ρ = λ / μ
   - Weight: W = 1 / (μ(1 − ρ)) based on M/M/1 queueing model
3. **Overload Protection** — if ρ ≥ 1, weight is set to W = 1000 (penalty), effectively excluding saturated servers.
4. **Dynamic Server Selection** — the server with minimum W is selected for each incoming request.
5. **Performance Measurement** — packet loss (%), response time (s), and throughput (bits/s) recorded at load levels: 1,000 / 100,000 / 1,000,000 requests.
6. **Statistical Analysis** — Cohen's d (paired differences), mean, SD, 95% CI, and normality tests computed using OriginPro 2026.

***

## 📈 Results Summary

### Packet Loss Improvement

| Environment | vs. LCPU | vs. LC | vs. LRAM |
|-------------|----------|--------|----------|
| Homogeneous | **37.5%** | 26.4% | 29.2% |
| Heterogeneous | **36.8%** | 28.2% | **39.2%** |

### Response Time Improvement

| Environment | vs. LCPU | vs. LC | vs. LRAM |
|-------------|----------|--------|----------|
| Homogeneous | **8.61%** | 7.78% | 6.94% |
| Heterogeneous | **11.4%** | 7.75% | 6.93% |

### Throughput Improvement

| Environment | vs. LCPU | vs. LC | vs. LRAM |
|-------------|----------|--------|----------|
| Homogeneous | 4.34% | 1.33% | **6.61%** |
| Heterogeneous | **17.1%** | 8.4% | **18.4%** |

### Effect Sizes (Cohen's d) — All Large (d > 0.8)

| Metric | Homogeneous Range | Heterogeneous Range |
|--------|-------------------|---------------------|
| Packet Loss | 1.32 – 1.43 | 1.40 – 1.60 |
| Response Time | 1.35 – 1.42 | 1.48 – 1.55 |
| Throughput | 1.05 – 1.15 | 1.10 – 1.30 |

***

## 🔗 Comparison Baseline Reference

DLBQT results are compared against three dynamic load-balancing algorithms (LCPU, LRAM, LC) previously proposed in:

> **Reference [1]**  
> Maghrib A. M. Alrammahi, Mohanad Y. Al-hamami, Ali M. Taher,  
> *"Optimizing Server-Side Dynamic Load Balancing in SDN Using Novel Algorithms Based on CPU, RAM, and Connection Metrics"*,  
> **International Journal of Advanced Research in Computer Science**, Vol. 17, No. 1, 2026, p. 21.  
> DOI: [https://doi.org/10.26483/ijarcs.v17i1.7401](https://doi.org/10.26483/ijarcs.v17i1.7401)

This paper is the direct baseline for DLBQT — the same Mininet/POX simulation environment, server configurations, traffic traces, and performance metrics are reused to ensure a fair and consistent comparison.

***

## 🛠️ Experimental Environment

| Parameter | Value |
|-----------|-------|
| Emulator | Mininet (v2.3.0) |
| OS | Ubuntu 22.04 LTS |
| Controller | POX (git snapshot 2023-01-15) |
| Hardware | Intel Core i7-10850H, 32 GB RAM, 512 GB SSD |
| Switch | OpenFlow single-switch topology |
| Servers | 2 servers (homogeneous & heterogeneous setups — see Table 4) |
| Dataset | 16 real-world trace files from Facebook data centers (1 KB–6.8 MB) |
| Load levels | 1,000 / 100,000 / 1,000,000 requests per experiment |
| Runs | 3 runs per configuration (results averaged) |
| Statistical Tool | OriginPro 2026 (OriginLab, Northampton, MA, USA) |
| Metrics | Packet loss (%), response time (s), throughput (bits/s) |

***

## 🚀 How to Use This Repository

1. **Browse `figures/`** — all 17 manuscript figures (Fig. 1–17).
2. **Browse `tables/`** — CSV files for Tables 1–18 (for re-analysis or plotting).
3. **Browse `code/`** — three Python files:
   - `DLBQT_Proposed_Algorithm.py` to study or run the DLBQT controller logic.
   - `homogeneous_server.py` and `heterogeneous_server.py` to replicate the simulation environments.
4. **Reproduce results** — run the code files inside a Mininet/POX environment on Ubuntu 22.04 with the dataset from reference [2]:
   > A. Iqbal (2021). *Oddlab datasets — cache folder*. GitHub. [https://github.com/aymeniq/Oddlab/tree/main/Datasets/cac](https://github.com/aymeniq/Oddlab/tree/main/Datasets/cac)

***

## 📖 Citation

If you use the DLBQT algorithm, code, or results in your research, please cite:

And the baseline algorithms paper:

> Maghrib A. M. Alrammahi, Mohanad Y. Al-hamami, Ali M. Taher,  
> *"Optimizing Server-Side Dynamic Load Balancing in SDN Using Novel Algorithms Based on CPU, RAM, and Connection Metrics"*,  
> **International Journal of Advanced Research in Computer Science**, Vol. 17, No. 1, 2026, p. 21.  
> DOI: [https://doi.org/10.26483/ijarcs.v17i1.7401](https://doi.org/10.26483/ijarcs.v17i1.7401)

***

## 📬 Contact

**Maghrib Abidalreda Maky Alrammahi**  
Information Technology Research and Development Centre (ITRDC)  
University of Kufa, Najaf 54001, Iraq  
📧 [maghrib.alramahi@uokufa.edu.iq](mailto:maghrib.alramahi@uokufa.edu.iq)  
🔗 ORCID: [https://orcid.org/0009-0001-5154-357X](https://orcid.org/0009-0001-5154-357X)

***

## 📜 License

This project is licensed under the **CC BY 4.0 License** — see [https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/) for details.
