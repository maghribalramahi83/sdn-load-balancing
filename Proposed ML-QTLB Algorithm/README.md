# ML-QTLB: Hybrid Machine Learning and Queueing-Theory 
# Load Balancing Model for SDN

---

## 📌 Overview

This folder contains the complete implementation of the **ML-QTLB** model,
including datasets, Python code, trained models, and result figures.

**ML-QTLB** integrates:
- Fuzzy C-Means (FCM) unsupervised clustering
- Random Forest (RF) supervised classification (Accuracy = 95.3%)
- M/M/1 Queueing Theory (QT) for optimal server selection
- Aging-based Starvation Prevention mechanism

---

## 📂 Folder Contents

### 🖼️ Images (6 Figures)

| File | Description | DPI |
|------|-------------|-----|
| `Confusion_Matrix_RFC.png` | Confusion Matrix of Random Forest Classifier (RFC) showing classification results for Class 1 (Low-priority) and Class 2 (High-priority) traffic | 300 |
| `Correlation_Matrix_13Features.png` | Correlation matrix heatmap for the dataset with 13 features, used to identify redundant features before feature selection | 300 |
| `Generation_Requests.png` | Visualization of the traffic generation process showing the number and size of requests transmitted between clients and servers in the Mininet environment | — |
| `ML_QTLB_Run_Proposed_Algorithm.png` | Screenshot or diagram of the proposed ML-QTLB algorithm running on the POX controller within the Mininet SDN testbed | — |
| `Silhouette_Analysis_K10.png` | Silhouette score analysis for K = 2 to 10 clusters, confirming that the optimal number of clusters is K = 2 (score ≈ 0.53) | 300 |
| `Wireshark_Capturing.png` | Screenshot of Wireshark capturing live traffic flows between clients (C1, C2, C3) and servers (S1, S2, S3) in the Mininet environment on Linux | — |

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

## ⚙️ ML-QTLB Pipeline


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
Alrammahi, M.A.M. and W.S. Bhaya. Performance Analysis for Load Balancing Algorithms using POX Controller in SDN. in 2022 International Conference on Data Science and Intelligent Computing (ICDSIC). 2022. IEEE.

### vs Classical Algorithms [2022]

| No. of Requests | RR | Random | WRR | LC | **ML-QTLB** |
|----------------|-----|--------|-----|----|------------|
| 300 | 0.01417 | 0.01372 | 0.01349 | 0.01497 | **0.0066** |
| 3,000 | 0.01452 | 0.01457 | 0.01443 | 0.01463 | **0.0084** |
| 15,000 | 0.01666 | 0.01473 | 0.01450 | 0.01485 | **0.0109** |
| 45,000 | 0.01745 | 0.01458 | 0.01454 | 0.01466 | **0.0123** |
| **Improvement (%)** | **53.42** | **51.90** | **51.07** | **55.91** | — |

Alrammahi, M.A.M., OPTIMIZING SERVER-SIDE DYNAMIC LOAD BALANCING IN SDN USING NOVEL ALGORITHMS BASED ON CPU, RAM, AND CONNECTION METRICS. international journal of advanced research in computer science, 2026. 17(1): p. 21–27.
DOI: http://dx.doi.org/10.26483/ijarcs.v17i1.7401 
### vs Server-Metric Algorithms [2026]

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

---

## 🛠️ Experimental Environment

| Parameter | Value |
|-----------|-------|
| Emulator | Mininet |
| OS | Linux Ubuntu 20.04.4 LTS |
| Controller | POX |
| Switch | OVS (OpenFlow 1.0) |
| Topology | Single Switch |
| Clients | 3 — C1, C2, C3 |
| Servers | 3 — S1, S2, S3 |
| CPU | Intel Core i7-3625QM 2.2GHz |
| RAM | 8 GB |
| HDD | 512 GB SSD |

---

## 📖 Citation

---

## 📬 Contact

**Maghrib Abidalreda Maky Alrammahi**
University of Kufa — ITRDC, Najaf, Iraq
📧 maghrib.alramahi@uokufa.edu.iq

---

## 📜 License
MIT License
