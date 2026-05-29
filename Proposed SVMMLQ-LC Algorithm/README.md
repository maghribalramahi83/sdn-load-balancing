# SVMMLQ-LC: SVM-Based Multi-Level Queue with Least-Connection Load Balancing for SDN

> **Repository:** `Proposed-SVMMLQ-LC-Algorithm`  
> **Author:** Maghrib Abidalreda Maky Alrammahi  
> **Institution:** University of Kufa — ITRDC, Najaf, Iraq  
> **Status:** Under Review (2026)

---

## 📌 Overview

This repository contains the **complete asset package** for the proposed **SVMMLQ‑LC** hybrid SDN load-balancing model, including all manuscript figures, preprocessed datasets, and Python source code used in the experimental evaluation.

**SVMMLQ‑LC** is a six-stage hybrid model that integrates:

- 🖧 Centralized SDN control using the **POX controller** in a **Mininet** emulation environment.
- 🔬 **K‑Means clustering** (k = 2, Elbow Method) for unsupervised traffic grouping into two priority classes.
- 🤖 **SVM-based online classification** (RBF kernel) achieving **98.75% test accuracy**.
- 📋 **Two-level Multi-Level Queue (MLQ)** scheduler with a **threshold-based starvation prevention** rule (T = 3).
- ⚖️ **Least-Connection (LC)** dynamic server selection to minimize active-connection imbalance across the server pool.
- 📊 Statistical validation using **two-way ANOVA**, **eta-squared effect size (η²)**, and **95% confidence intervals** via **OriginPro 2026**.

---

## 📂 Repository Contents (All Files in One Folder)

All files are placed directly inside the `Proposed-SVMMLQ-LC-Algorithm/` folder:


---

## 🖼️ Figures — Detailed Description (10 Files)

### Architectural & Methodology Figures

| # | Filename | Paper Figure | Description |
|---|----------|--------------|-------------|
| 1 | `fig01_SDN-Topology.jpg` | Figure 1 | **SDN Topology and Deployment of the SVMMLQ‑LC Controller** — Three-plane SDN architecture (Application Plane: HTTP files; Control Plane: SDN Controller with proposed SVMMLQ‑LC model; Data Plane: Data Center with OpenFlow Switch and Web Server Pool). |
| 2 | `fig02_Proposed-of-Network-Topology.jpg` | Figure 3 | **Proposed Mininet Single‑Switch Network Topology** — Three client hosts (10.0.0.4–6) connected to Open Virtual Switch (OVS1), forwarding to three HTTP servers (10.0.0.1–3). SDN Controller at 10.0.1.1 manages flows via OpenFlow v1.0. |
| 3 | `fig03_Proposed-SVMMLQ-LC-Stages.jpg` | Figure 2 | **Proposed SVMMLQ‑LC Workflow — Six Stages** — (1) Traffic generation in Mininet + Wireshark, (2) Preprocessing (Median Cleaning, Feature Selection, MinMax Normalization), (3) K‑Means clustering, (4) SVM training and online classification, (5) MLQ scheduling with starvation control, (6) Least-Connection server selection. |
| 4 | `fig04_Data-points-before-clustering-in-K-means.jpg` | Figure 5a | **Data Points Before K‑Means Clustering** — Scatter plot of 4,000 normalized flow records (Feature 1 vs. Feature 2) before cluster assignment, all in single color (blue). |
| 5 | `fig05_Data-points-after-clustering-in-K-means.jpg` | Figure 5b | **Data Points After K‑Means Clustering (k=2)** — Class 0 (high priority, purple) and Class 1 (low priority, yellow) with two red centroids. |
| 6 | `fig06_proposed-Flowchart.jpg` | Figure 6 | **Flowchart of Two‑Level MLQ Scheduler (T=3)** — Initialize & Push → Pop & Decision (Counter ≥ 3 AND Queue[1] not empty?) → Process & Control (serve Class 1 and reset, or serve Class 0). |
| 7 | `fig07_Confusion-Matrix-SVM.jpg` | — | **Confusion Matrix of SVM** — [[664, 13], [0, 369]]. Precision: 96.59%, Recall: 100%, F1: 98.26%, Accuracy: 98.75%. |
| 8 | `fig08_Result-of-Mean-Average-Time-s.jpg` | Figure 7 | **Mean / Average Time (s)** — SVMMLQ‑LC vs. Random, RR, WRR, LC across 300–45k requests. Best: 0.00751 s at 300 requests. |
| 9 | `fig09_Result-of-STD-Average-Response-Time-s.jpg` | Figure 8 | **STD / Average Response Time (s)** — SVMMLQ‑LC: 0.00147–0.008 s vs. baselines: 0.012–0.017 s. |
| 10 | `fig10_Result-of-CV-Degree-of-Load-Balancing.jpg` | Figure 9 | **CV / Degree of Load Balancing (%)** — SVMMLQ‑LC: 19.60–35.9% vs. baselines: 52–67%. |

---

## 📊 Datasets — Detailed Description (4 CSV Files)

| # | Filename | Stage | Records | Features | Description |
|---|----------|-------|---------|----------|-------------|
| 1 | `My-Dataset-Cleaning-Data.csv` | Stage 2.1 | 4,000 | 15 | Raw dataset after **median-based imputation**. Missing/noisy values replaced with median. Original 15 features: Packets, Bytes, Packets A→B, Bytes A→B, Packets B→A, Bytes B→A, Bits/s A→B, Bits/s B→A, Duration, Max/Min/Mean Packet Size, Inter-Arrival Time, Flow Start/End Time. |
| 2 | `My-Dataset-Feature-Selection.csv` | Stage 2.2 | 4,000 | 8 | After **correlation-matrix feature selection**. 8 features retained: Packets, Bytes, Packets A→B, Bytes A→B, Packets B→A, Bytes B→A, Bits/s A→B, Bits/s B→A. |
| 3 | `My-Dataset-MinMaxScaler.csv` | Stage 2.3 | 4,000 | 8 | After **MinMax normalization [0,1]**. All 8 features scaled: x_norm = (x − x_min)/(x_max − x_min). Input for K‑Means and SVM. |
| 4 | `My-Dataset-K-Means.csv` | Stage 3 | 4,000 | 9 | With **K‑Means labels (k=2)**. Class 0 = high priority (low volume), Class 1 = low priority (high volume). Used as ground truth for SVM training. |

---

## 🐍 Python Code — Detailed Description (5 Scripts)

| # | Filename | Stage | Input | Output | Description |
|---|----------|-------|-------|--------|-------------|
| 1 | `Elbow-method-for-calculate-K-means-and-with-n-clusters-12-Loop.py` | 3.1 | `My-Dataset-MinMaxScaler.csv` | Elbow plot | Runs K‑Means for k=2 to 12. Plots inertia vs. k. Elbow at k=2 confirms two-cluster structure. |
| 2 | `Calculate-of-K-means-with-2-cluster.py` | 3.2 | `My-Dataset-MinMaxScaler.csv` | `My-Dataset-K-Means.csv` + plots | Applies K‑Means (k=2). Assigns Class 0/1 labels. Generates before/after scatter plots. |
| 3 | `SVM-with-validation-set-manually.py` | 4 | `My-Dataset-K-Means.csv` | Trained SVM + metrics | Trains SVM (RBF, C=1, gamma='auto'). 3-way split: train/val/test. Reports: Train 98.66%, Val 98.74%, Test 98.75%. Confusion matrix + Precision/Recall/F1. |
| 4 | `Multi-Level-Queue-scheduling-code.py` | 5 | Classified flows | Queue log | Implements MLQ (Queue[0]=Class 0, Queue[1]=Class 1, T=3). Logic: Pop from Q0, increment counter; if Counter≥3 AND Q1 not empty → serve Q1 + reset; else serve Q0. |
| 5 | `SVMMLQ-LC-Model.py` | 6 | `My-Dataset-K-Means.csv` + server states | Metrics table | **Full SVMMLQ‑LC pipeline**. Integrates SVM → MLQ → LC server selection. Outputs: Max-Time, Min-Time, Mean, STD, CV for all 5 algorithms × 4 traffic levels. |

---

## ⚙️ Full Six-Stage Pipeline
┌────────────────────────────────────────────────────────┐
│ OFFLINE PHASE (Training) │
│ │
│ Stage 1: Traffic Generation & Capture │
│ Mininet + POX → 5 HTTP files (1–75 MB) │
│ Wireshark → 4,000 records × 15 features │
│ ↓ │
│ Stage 2: Preprocessing │
│ Median imputation → Feature selection (8) │
│ → MinMax normalization │
│ ↓ │
│ Stage 3: K‑Means Clustering │
│ Elbow → k=2 → Class 0 / Class 1 │
│ ↓ │
│ Stage 4: SVM Training │
│ RBF kernel → 98.75% accuracy │
└────────────────────────────────────────────────────────┘
↓
┌────────────────────────────────────────────────────────┐
│ ONLINE PHASE (Real-Time) │
│ │
│ Stage 4: SVM Classification │
│ New flow → Class 0 or 1 │
│ ↓ │
│ Stage 5: MLQ Scheduling │
│ Queue (High), Queue (Low), T=3 │
│ ↓ │
│ Stage 6: LC Server Selection │
│ Select server with min connections │
└────────────────────────────────────────────────────────┘


---

## 📈 Experimental Results Summary

### Mean / Average Time (s)

| Algorithm | 300 | 3,000 | 15,000 | 45,000 |
|-----------|-----|-------|--------|--------|
| Random | 0.02330 | 0.02465 | 0.02498 | 0.02498 |
| RR | 0.02498 | 0.02465 | 0.02612 | 0.02645 |
| WRR | 0.02645 | 0.02465 | 0.02498 | 0.02465 |
| LC | 0.02645 | 0.02465 | 0.02498 | 0.02508 |
| **SVMMLQ‑LC** | **0.00751** | **0.01278** | **0.01466** | **0.01498** |

### STD / Average Response Time (s)

| Algorithm | 300 | 3,000 | 15,000 | 45,000 |
|-----------|-----|-------|--------|--------|
| Random | 0.01331 | 0.01331 | 0.01331 | 0.01331 |
| RR | 0.01331 | 0.01331 | 0.01497 | 0.01745 |
| WRR | 0.01497 | 0.01331 | 0.01331 | 0.01331 |
| LC | 0.01497 | 0.01331 | 0.01331 | 0.01331 |
| **SVMMLQ‑LC** | **0.00147** | **0.00440** | **0.00618** | **0.00782** |

### CV / Degree of Load Balancing (%)

| Algorithm | 300 | 3,000 | 15,000 | 45,000 |
|-----------|-----|-------|--------|--------|
| Random | 59.5 | 59.5 | 59.5 | 59.5 |
| RR | 52.2 | 57.7 | 63.9 | 66.8 |
| WRR | 56.7 | 57.7 | 57.7 | 57.7 |
| LC | 57.8 | 59.5 | 57.7 | 59.5 |
| **SVMMLQ‑LC** | **19.60** | **27.4** | **31.1** | **35.9** |

### Two-Way ANOVA

| Metric | Factor | F | p | η² | Sig? |
|--------|--------|---|---|-------|------|
| Mean Time | Traffic Level | 6.28 | 0.021 | 0.162 | ✅ |
| Mean Time | Algorithm | 6.25 | 0.008 | 0.322 | ✅ |
| STD Time | Traffic Level | 6.28 | 0.021 | 0.162 | ✅ |
| STD Time | Algorithm | 6.25 | 0.008 | 0.322 | ✅ |
| CV | Traffic Level | 0.70 | 0.414 | 0.024 | ❌ |
| CV | Algorithm | 4.10 | 0.032 | 0.284 | ✅ |

---

## 🛠️ Experimental Environment

| Parameter | Value |
|-----------|-------|
| Emulator | Mininet |
| OS | Linux (Ubuntu) |
| Controller | POX (OpenFlow v1.0) |
| Switch | Open vSwitch (OVS1) |
| Clients | 3 hosts: 10.0.0.4–6 |
| Servers | 3 HTTP: 10.0.0.1–3 |
| Controller IP | 10.0.1.1 |
| Traffic Files | 1, 10, 25, 50, 75 MB |
| Request Loads | 300, 3k, 15k, 45k |
| Dataset | 4,000 × 15 → 8 features |
| ML | scikit-learn |
| SVM | RBF, C=1, gamma='auto' |
| K‑Means | k=2 (Elbow Method) |
| MLQ Threshold | T=3 |
| Stats Tool | OriginPro 2026 |

---

## 🚀 How to Use

### Prerequisites

```bash
pip install scikit-learn numpy pandas matplotlib
```

### Run in Order

```bash
python "Elbow-method-for-calculate-K-means-and-with-n-clusters-12-Loop.py"
python "Calculate-of-K-means-with-2-cluster.py"
python "SVM-with-validation-set-manually.py"
python "Multi-Level-Queue-scheduling-code.py"
python "SVMMLQ-LC-Model.py"
```

### Load Example

```python
import pandas as pd
df = pd.read_csv("My-Dataset-MinMaxScaler.csv")
print(df.shape)  # (4000, 8)
```

---

## 📖 Citation

If you use this work, please cite:

> **[5] Baseline:**  
> Maghrib A. M. Alrammahi, "Comparative Analysis of Random, Round Robin, Weighted Round Robin, and Least Connection Load Balancing Algorithms in SDN", IJACSA, 2022.

---

## 📬 Contact

**Maghrib Abidalreda Maky Alrammahi**  
University of Kufa — ITRDC, Najaf, Iraq  
📧 maghrib.alramahi@uokufa.edu.iq

---

## 📜 License

MIT License

---
