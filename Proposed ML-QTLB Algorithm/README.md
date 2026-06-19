# ML-QTLB: Hybrid Machine Learning and Queueing-Theory Load Balancing Model for SDN

---

## 📌 Overview

This repository contains the complete implementation of the **ML-QTLB** model,
including datasets, Python source code, architectural diagrams, implementation figures,
and performance evaluation results.

**ML-QTLB** is a hybrid load balancing framework for **Software-Defined Networking (SDN)** that integrates:

- **Fuzzy C-Means (FCM)** for unsupervised traffic clustering
- **Random Forest (RF)** for supervised real-time traffic classification
- **M/M/1 Queueing Theory (QT)** for optimal server selection
- **Aging-based starvation prevention** for fairness-aware scheduling

The framework was implemented and evaluated in a **Mininet-based SDN testbed**
using **POX** as the controller, **OVS** as the OpenFlow switch, and
**Wireshark** on Linux for traffic capture and dataset construction. The final dataset contains
**25,000 records** collected from controlled traffic generated between **3 clients**
and **3 servers** using files ranging from **1 MB to 75 MB**.

---

## ✨ Key Features

- Hybrid ML + Queueing-Theory load balancing framework
- Real traffic dataset captured from a Mininet SDN environment
- Five-stage processing pipeline from traffic generation to routing decision
- FCM clustering with **K = 2** validated using silhouette analysis
- RF traffic classifier with **95.3% accuracy**
- M/M/1-based server selection using \( \lambda_k \), \( \mu_k \), \( \rho_k \), and \( W_k \)
- Aging-based anti-starvation mechanism for low-priority flows
- Comparative evaluation against:
  - Classical algorithms: **RR, Random, WRR, LC**
  - Server-metric-based algorithms: **LRAM, LCPU, LCPURAM, LC, LCLCPURAM**

---

## 📂 Repository Contents

### 🏗️ Architectural & Methodology Figures

| File | Description | DPI |
|------|-------------|-----|
| `Figure_1_Overall_Architecture.png` | Overall architecture of the proposed ML-QTLB framework showing the integration of the ML module, QT scheduler, and SDN controller |
| `Figure_2_Network_Topology.png` | Proposed Mininet topology with 3 clients, 3 servers, 1 OVS switch, and 1 POX controller |
| `Figure_3_Stages_of_Proposed_Model.png` | Five sequential stages of the ML-QTLB model from traffic generation to QT scheduling |

### 🖼️ Implementation & Analysis Figures

| File | Description |
|------|-------------|
| `Figure_4_Wireshark_Capturing.png` | Wireshark capturing traffic in the Mininet SDN environment |
| `Figure_5_Generation_Requests.png` | Traffic generation process between clients and servers |
| `Figure_6_Correlation_Matrix_13Features.png` | Correlation matrix heatmap for feature analysis |
| `Figure_7_Silhouette_Analysis_K10.png` | Silhouette score analysis for selecting the optimal number of clusters |
| `Figure_8_Confusion_Matrix_RFC.png` | Confusion matrix of the RF classifier |
| `Figure_9_ML_QTLB_Run_Proposed_Algorithm.png` | Screenshot or diagram of the ML-QTLB algorithm running in POX within Mininet |

### 📈 Performance Result Figures

| File | Description |
|------|-------------|
| `Figure_10_Result_Average_Response_Time.png` | Average Response Time comparison |
| `Figure_11_Result_Degree_of_Load_Balancing.png` | Degree of Load Balancing comparison |
| `Figure_12_Result_Waiting_Time.png` | Waiting Time comparison |
| `Figure_13_Result_Service_Time.png` | Service Time comparison |

---

## 📊 Datasets

All datasets contain **25,000 records** captured from the Mininet-based SDN testbed
using Wireshark on Linux.

Traffic files used for generation:
**1 MB, 10 MB, 25 MB, 50 MB, and 75 MB**

| File | Records | Features | Description |
|------|---------|----------|-------------|
| `DS1_15Features.csv` | 25,000 | 15 | Raw Wireshark-captured dataset with original traffic features |
| `DS1_FeatureSelection_8Features.csv` | 25,000 | 8 | Dataset after feature selection |
| `DS1_Normalization.csv` | 25,000 | 8 | Dataset after Min-Max normalization |
| `DS1_FuzzyCMeans_K2.csv` | 25,000 | 9 | Dataset after FCM clustering with K = 2 including cluster label |

### Dataset Features Description

| No. | Feature | Description |
|-----|---------|-------------|
| 1 | Packets | Total packets exchanged between A and B |
| 2 | Bytes | Total bytes exchanged between A and B |
| 3 | Packets A→B | Packets sent from source to destination |
| 4 | Bytes A→B | Bytes sent from source to destination |
| 5 | Packets B→A | Packets sent from destination to source |
| 6 | Bytes B→A | Bytes sent from destination to source |
| 7 | Bits/s A→B | Average data rate from A to B |
| 8 | Bits/s B→A | Average data rate from B to A |

---

## 🐍 Python Files

| File | Description |
|------|-------------|
| `RF_Classifier_with_Validation.py` | Random Forest training and validation script with train/validation/test split, metrics, and confusion matrix |
| `ML_QTLB_Proposed_Model.py` | Full ML-QTLB implementation for the POX controller including RF classification, QT scheduling, and starvation prevention |

---

## 📁 Traffic Generation Files

Five dummy binary files were used to generate controlled traffic in the Mininet SDN environment.

| File | Size | Type | Purpose |
|------|------|------|---------|
| `file_1MB.bin` | 1 MB | Binary | Low traffic load |
| `file_10MB.bin` | 10 MB | Binary | Light traffic load |
| `file_25MB.bin` | 25 MB | Binary | Medium traffic load |
| `file_50MB.bin` | 50 MB | Binary | Heavy traffic load |
| `file_75MB.bin` | 75 MB | Binary | Maximum traffic load |

> ⚠️ These binary files are not included in the repository because of GitHub size limitations.

### Generate Traffic Files Locally

```python
import os

sizes =[2]

for s in sizes:
    filename = f'file_{s}MB.bin'
    with open(filename, 'wb') as f:
        f.write(b'\0' * s * 1024 * 1024)
    print(f"Created: {filename} ({s} MB)")

print("All traffic files generated successfully.")
```

### Example Traffic Transfer Command

```python
import subprocess
subprocess.run(['scp', 'file_1MB.bin', 'server@10.0.0.2:/tmp/'])
```

---

## ⚙️ ML-QTLB Pipeline

The ML-QTLB framework operates in five sequential stages:

1. **Traffic Generation & Capture**  
   Controlled traffic is generated in Mininet and captured using Wireshark.

2. **Preprocessing**  
   Data cleaning, feature selection, and Min-Max normalization are applied.

3. **FCM Clustering**  
   Traffic flows are grouped into two clusters using Fuzzy C-Means.

4. **RF Classification**  
   Random Forest is trained on FCM-derived labels for real-time classification.

5. **QT Scheduling with Aging**  
   M/M/1-based scheduling selects the optimal server while preventing starvation.

---

## 🛠️ Experimental Environment

| Parameter | Value |
|-----------|-------|
| Emulator | Mininet |
| OS | Ubuntu 20.04.4 LTS |
| Controller | POX |
| Switch | OVS (OpenFlow 1.0) |
| Topology | Single-switch topology |
| Clients | 3 — C1, C2, C3 |
| Servers | 3 — S1, S2, S3 |
| CPU | Intel Core i7-3625QM 2.2 GHz |
| RAM | 8 GB |
| Storage | 512 GB SSD |

---

## 🚀 How to Run

### Requirements

```bash
pip install pandas numpy scikit-learn matplotlib seaborn joblib fcmeans
```

### Step 1: Train the RF Classifier

```bash
python RF_Classifier_with_Validation.py
```

### Step 2: Run ML-QTLB on the POX Controller

```bash
python pox.py log.level --DEBUG ML_QTLB_Proposed_Model \
       --ip=10.0.0.1 \
       --servers=10.0.0.2,10.0.0.3,10.0.0.4
```

---

## 📈 Results Summary

### Average Response Time vs Classical Algorithms

| No. of Requests | RR | Random | WRR | LC | **ML-QTLB** |
|----------------|-----|--------|-----|----|------------|
| 300 | 0.01417 | 0.01372 | 0.01349 | 0.01497 | **0.0066** |
| 3,000 | 0.01452 | 0.01457 | 0.01443 | 0.01463 | **0.0084** |
| 15,000 | 0.01666 | 0.01473 | 0.01450 | 0.01485 | **0.0109** |
| 45,000 | 0.01745 | 0.01458 | 0.01454 | 0.01466 | **0.0123** |

### Degree of Load Balancing vs Classical Algorithms

| No. of Requests | RR | Random | WRR | LC | **ML-QTLB** |
|----------------|-----|--------|-----|----|------------|
| 300 | 56.6609 | 59.1226 | 52.1173 | 56.6124 | **81.50** |
| 3,000 | 57.7261 | 59.4615 | 58.7473 | 58.0368 | **75.40** |
| 15,000 | 64.0122 | 58.7697 | 58.3562 | 58.0673 | **69.44** |
| 45,000 | 66.7630 | 58.6936 | 58.4549 | 58.4451 | **68.35** |

### Waiting Time vs Server-Metric-Based Algorithms

| No. of Requests | LRAM | LCPU | LCPURAM | LC | LCLCPURAM | **ML-QTLB** |
|----------------|------|------|---------|----|-----------|------------|
| 8,000 | 0.158 | 0.0730 | 0.0738 | 0.0738 | 0.0741 | **0.00843** |
| 40,000 | 0.160 | 0.0755 | 0.0747 | 0.0742 | 0.0726 | **0.01021** |

### Service Time vs Server-Metric-Based Algorithms

| No. of Requests | LRAM | LCPU | LCPURAM | LC | LCLCPURAM | **ML-QTLB** |
|----------------|------|------|---------|----|-----------|------------|
| 8,000 | 0.020 | 0.0164 | 0.0079 | 0.0079 | 0.0084 | **0.00107** |
| 40,000 | 0.021 | 0.0083 | 0.0085 | 0.0083 | 0.0085 | **0.00129** |

---

## 📋 Updated Table 11: Mean Improvement Summary

| Metric | vs. RR | vs. Random | vs. WRR | vs. LC | vs. LRAM | vs. LCPU | vs. LCPURAM | vs. LCLCPURAM |
|--------|--------|------------|---------|--------|----------|----------|-------------|---------------|
| Average Response Time Mean Improvement (%) | 39.91 | 33.97 | 33.27 | 35.30 | — | — | — | — |
| Degree of Load Balancing Mean Improvement (%) | 21.33 | 24.82 | 30.16 | 27.60 | — | — | — | — |
| Waiting Time Mean Improvement (%) | — | — | — | 87.41 | 94.14 | 87.46 | 87.45 | 87.28 |
| Service Time Mean Improvement (%) | — | — | — | 85.46 | 94.25 | 88.97 | 85.64 | 86.04 |

---

## 🧠 Mathematical Model

For each server \( S_k \), the controller computes:

- Arrival rate: \( \lambda_k \)
- Service rate: \( \mu_k \)
- Utilization: \( \rho_k = \frac{\lambda_k}{\mu_k} \)
- Expected system time: \( W_k = \frac{1/\mu_k}{1-\rho_k} \), for \( \rho_k < 1 \)

The selected server is:

\[
S^* = \arg\min W_k
\]

To prevent starvation, a low-priority request is promoted if its waiting time exceeds a threshold \( T \).

---

## 📖 Citation

If you use this repository in your research, please cite:

```bibtex
@article{alrammahi2026mlqtlb,
  author  = {Alrammahi, Maghrib Abidalreda Maky},
  title   = {ML-QTLB: Hybrid Machine Learning and Queueing-Theory Load Balancing Model for SDN},
  journal = {International Journal of Intelligent Engineering and Systems},
  year    = {2026}
}
```

---

## 📬 Contact

**Maghrib Abidalreda Maky Alrammahi**  
University of Kufa — ITRDC, Najaf, Iraq  
Email: `maghrib.alramahi@uokufa.edu.iq`

---

## 📜 License

This project is released under the **MIT License**.

---
