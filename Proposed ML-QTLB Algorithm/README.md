# ML-QTLB: Hybrid Machine Learning and Queueing-Theory 
# Load Balancing Model for SDN

---

## 📌 Overview

This folder contains the complete implementation of the **ML-QTLB** model,
including datasets, Python code, trained models, architectural diagrams,
and result figures.

**ML-QTLB** integrates:
- Fuzzy C-Means (FCM) unsupervised clustering
- Random Forest (RF) supervised classification (Accuracy = 95.3%)
- M/M/1 Queueing Theory (QT) for optimal server selection
- Aging-based Starvation Prevention mechanism

---

## 📂 Folder Contents

### 🏗️ Architectural & Methodology Diagrams (3 Figures)

| File | Description | DPI |
|------|-------------|-----|
| `Figure_1_Overall_Architecture.png` | **Overall Architecture of the Proposed ML-QTLB Framework** — high-level block diagram showing the integration of the ML pipeline (FCM + RF), the QT scheduler (M/M/1 + aging-based starvation prevention), and the POX SDN controller within the Mininet testbed | 300 |
| `Figure_2_Network_Topology.png` | **Proposed Network Topology** — single-switch Mininet topology with three clients (C1, C2, C3), three servers (S1, S2, S3), one OVS switch (OpenFlow 1.0), and the POX controller | 300 |
| `Figure_3_Stages_of_Proposed_Model.png` | **Stages of the Proposed Model** — flowchart of the five sequential stages: (1) Traffic Generation & Wireshark Capture, (2) Preprocessing (cleaning, feature selection 15→8, normalization), (3) FCM Clustering (K=2), (4) RF Classification, (5) QT Scheduling with Aging Threshold | 300 |

---

### 🖼️ Implementation & Analysis Figures (6 Figures)

| File | Description | DPI |
|------|-------------|-----|
| `Figure_4_Wireshark_Capturing.png` | Screenshot of Wireshark capturing live traffic flows between clients (C1, C2, C3) and servers (S1, S2, S3) in the Mininet environment on Linux | — |
| `Figure_5_Generation_Requests.png` | Visualization of the traffic generation process showing the number and size of requests transmitted between clients and servers in the Mininet environment | — |
| `Figure_6_Correlation_Matrix_13Features.png` | Correlation matrix heatmap for the dataset with 13 features, used to identify redundant features before feature selection | 300 |
| `Figure_7_Silhouette_Analysis_K10.png` | Silhouette score analysis for K = 2 to 10 clusters, confirming that the optimal number of clusters is K = 2 (score ≈ 0.53) | 300 |
| `Figure_8_Confusion_Matrix_RFC.png` | Confusion Matrix of Random Forest Classifier (RFC) showing classification results for Class 1 (Low-priority) and Class 2 (High-priority) traffic | 300 |
| `Figure_9_ML_QTLB_Run_Proposed_Algorithm.png` | Screenshot/diagram of the proposed ML-QTLB algorithm running on the POX controller within the Mininet SDN testbed | — |

---

### 📈 Results Figures (4 Performance Metric Plots)

The following figures visualize ML-QTLB's performance against the
baseline algorithms across the four evaluated performance metrics.

| File | Description | DPI |
|------|-------------|-----|
| `Figure_10_Result_Average_Response_Time.png` | **Average Response Time (s)** — comparative chart of ML-QTLB vs. classical algorithms (RR, Random, WRR, LC) across four traffic load levels (300, 3,000, 15,000, 45,000 requests). ML-QTLB achieves up to **55.91% reduction** | 300 |
| `Figure_11_Result_Degree_of_Load_Balancing.png` | **Degree of Load Balancing (%)** — comparative chart showing ML-QTLB vs. classical algorithms (RR, Random, WRR, LC) across the same four traffic loads. ML-QTLB achieves up to **56.38% improvement** | 300 |
| `Figure_12_Result_Waiting_Time.png` | **Waiting Time (s)** — comparative chart of ML-QTLB vs. server-metric-based algorithms (LRAM, LCPU, LCPURAM, LC, LCLCPURAM) at 8,000 and 40,000 requests. ML-QTLB achieves up to **94.66% reduction** | 300 |
| `Figure_13_Result_Service_Time.png` | **Service Time (s)** — comparative chart of ML-QTLB vs. server-metric-based algorithms (LRAM, LCPU, LCPURAM, LC, LCLCPURAM) at 8,000 and 40,000 requests. ML-QTLB achieves up to **94.65% reduction** | 300 |

---

### 📊 Datasets (4 CSV Files)

All datasets contain **25,000 records** captured from a Mininet-based
SDN testbed using Wireshark on Linux.
Traffic files transmitted: **1 MB, 10 MB, 25 MB, 50 MB, 75 MB**

| File | Records | Features | Description |
|------|---------|----------|-------------|
| `DS1_15Features.csv` | 25,000 | 15 | **Raw dataset** captured directly from Wireshark. Contains all original flow-level features including IP addresses, ports, packets, bytes, duration, and throughput |
| `DS1_FeatureSelection_8Features.csv` | 25,000 | 8 | **After feature selection.** Reduced from 15 to 8 most informative features: Packets, Bytes, Packets A→B, Bytes A→B, Packets B→A, Bytes B→A, Bits/s A→B, Bits/s B→A |
| `DS1_Normalization.csv` | 25,000 | 8 | **After Min-Max normalization.** All 8 features scaled to range [0, 1] to ensure equal contribution during ML training |
| `DS1_FuzzyCMeans_K2.csv` | 25,000 | 9 | **After FCM clustering (K=2).** Contains 8 normalized features plus the assigned cluster label (1 = Low-priority, 2 = High-priority), used as ground-truth labels for RF training |

#### Dataset Features Description

| No. | Feature | Description |
|-----|---------|-------------|
| 1 | Packets | Total packets exchanged between A and B |
| 2 | Bytes | Total bytes exchanged between A and B |
| 3 | Packets A→B | Packets sent from source to destination |
| 4 | Bytes A→B | Bytes sent from source to destination |
| 5 | Packets B→A | Packets sent from destination to source |
| 6 | Bytes B→A | Bytes sent from destination to source |
| 7 | Bits/s A→B | Average data rate from A to B (bits/s) |
| 8 | Bits/s B→A | Average data rate from B to A (bits/s) |

---

### 🐍 Python Files (2 Scripts)

| File | Description |
|------|-------------|
| `RF_Classifier_with_Validation.py` | **Random Forest Classifier (RFC)** training script with train/validation/test split (38%/38%/24%). Includes hyperparameter configuration (criterion=entropy, n_estimators=80, max_depth=4, min_samples_split=7, random_state=0), evaluation metrics (Accuracy=95.3%, Precision, Recall, F1-Score), confusion matrix plot, and overfitting/underfitting check |
| `ML_QTLB_Proposed_Model.py` | **Full ML-QTLB implementation** running on the POX SDN controller. Integrates RF classifier for real-time traffic classification, M/M/1 Queueing Theory scheduler (λk, μk, ρk, Wk computation), aging-based starvation prevention (threshold T), and OpenFlow-based routing decisions via OVS switch |

---

## 📁 Traffic Generation Files

Five dummy binary files were used to generate controlled
SDN traffic flows in the Mininet emulation environment.
Each file was transmitted between three client nodes
(C1, C2, C3) and three server nodes (S1, S2, S3)
via a Python script on Linux.

| File | Size | Type | Purpose |
|------|------|------|---------|
| `file_1MB.bin`  | 1 MB  | Empty binary | Low traffic load |
| `file_10MB.bin` | 10 MB | Empty binary | Light traffic load |
| `file_25MB.bin` | 25 MB | Empty binary | Medium traffic load |
| `file_50MB.bin` | 50 MB | Empty binary | Heavy traffic load |
| `file_75MB.bin` | 75 MB | Empty binary | Maximum traffic load |

> ⚠️ These files are not included in the repository
> due to GitHub file size limitations (max 25 MB).
> You can generate them locally using the script below.

### Generate Traffic Files Locally

```python
import os

# Generate dummy binary files for SDN traffic generation
sizes = [1, 10, 25, 50, 75]  # sizes in MB

for s in sizes:
    filename = f'file_{s}MB.bin'
    with open(filename, 'wb') as f:
        f.write(b'\0' * s * 1024 * 1024)
    print(f"Created: {filename}  ({s} MB)")

print("All traffic files generated successfully.")
```

These files were transmitted using the following command
in the Mininet environment:

```python
# Send file from client to server
import subprocess
subprocess.run(['scp', 'file_1MB.bin',
                'server@10.0.0.2:/tmp/'])
```

---

## ⚙️ ML-QTLB Pipeline

See `Figure_3_Stages_of_Proposed_Model.png` for the full pipeline flowchart.

**Pipeline stages:**
1. **Traffic Generation & Capture** — Mininet + Wireshark (15 raw features)
2. **Preprocessing** — Cleaning → Feature Selection (15 → 8) → Min-Max Normalization
3. **FCM Clustering** — Unsupervised labeling with K=2 (Silhouette-validated)
4. **RF Classification** — Real-time classification (95.3% accuracy)
5. **QT Scheduling** — M/M/1-based server selection with aging-based starvation prevention

---

## 🚀 How to Run

### Requirements
```bash
pip install pandas numpy scikit-learn matplotlib seaborn joblib fcmeans
```

### Step 1: Train RF Classifier
```bash
python RF_Classifier_with_Validation.py
```

### Step 2: Run ML-QTLB on POX Controller
```bash
python pox.py log.level --DEBUG ML_QTLB_Proposed_Model \
       --ip=10.0.0.1 \
       --servers=10.0.0.2,10.0.0.3,10.0.0.4
```

---

## 📈 Results Summary

### vs Classical Algorithms [2022]

> Alrammahi, M.A.M. and W.S. Bhaya. *Performance Analysis for Load Balancing Algorithms using POX Controller in SDN.* In 2022 International Conference on Data Science and Intelligent Computing (ICDSIC). 2022. IEEE.

| No. of Requests | RR | Random | WRR | LC | **ML-QTLB** |
|----------------|-----|--------|-----|----|------------|
| 300 | 0.01417 | 0.01372 | 0.01349 | 0.01497 | **0.0066** |
| 3,000 | 0.01452 | 0.01457 | 0.01443 | 0.01463 | **0.0084** |
| 15,000 | 0.01666 | 0.01473 | 0.01450 | 0.01485 | **0.0109** |
| 45,000 | 0.01745 | 0.01458 | 0.01454 | 0.01466 | **0.0123** |
| **Improvement (%)** | **53.42** | **51.90** | **51.07** | **55.91** | — |

📊 See: `Figure_10_Result_Average_Response_Time.png` and `Figure_11_Result_Degree_of_Load_Balancing.png`

### vs Server-Metric Algorithms [2026]

> Alrammahi, M.A.M. *Optimizing Server-Side Dynamic Load Balancing in SDN Using Novel Algorithms Based on CPU, RAM, and Connection Metrics.* International Journal of Advanced Research in Computer Science, 2026. 17(1): p. 21–27.
> DOI: [http://dx.doi.org/10.26483/ijarcs.v17i1.7401](http://dx.doi.org/10.26483/ijarcs.v17i1.7401)

| No. of Requests | LRAM | LCPU | LCPURAM | LC | LCLCPURAM | **ML-QTLB** |
|----------------|------|------|---------|----|-----------|------------|
| **Waiting Time (s)** | | | | | | |
| 8,000 | 0.158 | 0.073 | 0.0738 | 0.0738 | 0.0741 | **0.00843** |
| 40,000 | 0.160 | 0.0755 | 0.0747 | 0.0742 | 0.0726 | **0.01021** |
| **Improvement (%)** | **94.66** | **88.45** | **88.58** | **88.58** | **88.62** | — |
| **Service Time (s)** | | | | | | |
| 8,000 | 0.020 | 0.0164 | 0.0079 | 0.0079 | 0.0084 | **0.00107** |
| 40,000 | 0.021 | 0.0083 | 0.0085 | 0.0083 | 0.0085 | **0.00129** |
| **Improvement (%)** | **94.65** | **93.48** | **86.46** | **86.46** | **87.26** | — |

📊 See: `Figure_12_Result_Waiting_Time.png` and `Figure_13_Result_Service_Time.png`

---

## 🛠️ Experimental Environment

| Parameter | Value |
|-----------|-------|
| Emulator | Mininet |
| OS | Linux Ubuntu 20.04.4 LTS |
| Controller | POX |
| Switch | OVS (OpenFlow 1.0) |
| Topology | Single Switch (see `Figure_2_Network_Topology.png`) |
| Clients | 3 — C1, C2, C3 |
| Servers | 3 — S1, S2, S3 |
| CPU | Intel Core i7-3625QM 2.2GHz |
| RAM | 8 GB |
| HDD | 512 GB SSD |

---

## 📖 Citation

If you use this code or dataset in your research, please cite:

```bibtex
@article{alrammahi2026mlqtlb,
  author  = {Alrammahi, Maghrib Abidalreda Maky},
  title   = {ML-QTLB: Hybrid Machine Learning and Queueing-Theory 
             Load Balancing Model for SDN},
  journal = {International Journal of Intelligent Engineering and Systems},
  year    = {2026}
}
```

---

## 📬 Contact

**Maghrib Abidalreda Maky Alrammahi**  
University of Kufa — ITRDC, Najaf, Iraq  
📧 [maghrib.alramahi@uokufa.edu.iq](mailto:maghrib.alramahi@uokufa.edu.iq)

---

## 📜 License
MIT License
