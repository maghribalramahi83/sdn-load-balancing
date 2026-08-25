# SVMMLQ-LC: Intelligent SDN Load Balancing with SVM, Multi-Level Queue Scheduling, and Least-Connection Selection

> **Repository:** `sdn-load-balancing`  
> **Project Folder:** `Proposed SVMMLQ-LC Algorithm`  
> **Status:** Revised manuscript under review (2026)

## Authors

1. **Maghrib Abidalreda Maky Alrammahi**\*  
2. **Faris Sattar Hadi**  
3. **Abbas Nasir AlTaee**

\*Corresponding author.

---

## Overview

This repository provides the reproducibility materials for the revised manuscript:

> **SVMMLQ-LC: An Intelligent Machine Learning-Based Load-Balancing Framework with Multi-Level Queue Scheduling and Least-Connection Selection for Software-Defined Networking**

The repository includes the four experimental datasets, six Python scripts for the proposed model, four baseline load-balancing implementations, thirteen manuscript figures, and supporting materials associated with the revised study.

The proposed **SVMMLQ-LC** framework integrates:

- Software-Defined Networking (SDN) control using a POX controller in a Mininet emulation environment.
- K-Means clustering for data-driven traffic grouping.
- Support Vector Machine (SVM) classification with an RBF kernel.
- A two-level Multi-Level Queue (MLQ) mechanism for priority-aware packet scheduling.
- A threshold-based scheduling rule with \(T = 3\) to reduce lower-priority queue starvation.
- Least-Connection (LC) server selection for dynamic server assignment.
- Comparative evaluation against Random, Round Robin, Weighted Round Robin, and Least-Connection baseline algorithms.

---

## Repository Structure

```text
Proposed SVMMLQ-LC Algorithm/
│
├── README.md
│
├── datasets/
│   ├── README.md
│   ├── My-Dataset-Cleaning-Data.csv
│   ├── My-Dataset-Feature-Selection.csv
│   ├── My-Dataset-MinMaxScaler.csv
│   └── My-Dataset-K-Means.csv
│
├── codes/
│   ├── README.md
│   ├── Pearson-Correlation.py
│   ├── Elbow-method-for-calculate-K-means-and-wirh-n-clusters-12-Loop.py
│   ├── Calculate-of-K-means-with-2-cluster.py
│   ├── SVM-with-validation-set-manually.py
│   ├── Multi-Level-Queue-scheduling-code.py
│   └── SVMMLQ-LC-Model.py
│
├── Baseline Algorithms/
│   ├── README.md
│   ├── R-Algorithm.py
│   ├── RR-Algorithm.py
│   ├── WRR-Algorithm.py
│   └── LC-Algorithm.py
│
└── figures/
    ├── README.md
    ├── Figure 1
    ├── Figure 2
    ├── ...
    └── Figure 13
```

> File and folder names may be adapted to match the exact names used in this repository.

---

## Proposed SVMMLQ-LC Workflow

The proposed framework follows a six-stage workflow.

### Stage 1: SDN Traffic Generation and Packet Capture

Traffic is generated in a Mininet-based SDN topology containing client hosts, HTTP servers, an Open vSwitch, and a POX controller. HTTP file requests with different file sizes are generated and captured using Wireshark.

### Stage 2: Data Preprocessing

The captured flow-level dataset is processed through:

- Median-based cleaning of missing or noisy numerical data.
- Pearson correlation analysis and feature selection.
- Min-Max normalization of the selected numerical features.

### Stage 3: K-Means Traffic Grouping

K-Means clustering is applied to the normalized feature set. The Elbow Method is used to examine candidate cluster numbers, while the final workflow uses two traffic classes to support the two-level priority queue design.

### Stage 4: SVM Training and Online Classification

An SVM classifier with an RBF kernel is trained using the K-Means traffic labels. The trained classifier predicts the traffic class of new flows before they enter the queue-scheduling stage.

### Stage 5: Threshold-Based MLQ Scheduling

The scheduling mechanism uses two queues:

```text
Queue0: High-priority traffic
Queue1: Low-priority traffic
```

A threshold value of \(T = 3\) is used to periodically serve Queue1 when it is non-empty, thereby reducing starvation of lower-priority traffic.

### Stage 6: Least-Connection Server Selection

After scheduling, the Least-Connection policy selects the available server with the fewest active connections for the processed flow.

---

## Materials Included

| Material | Quantity | Description |
|---|---:|---|
| Experimental datasets | 4 | Flow-level datasets produced during cleaning, feature selection, Min-Max scaling, and K-Means labeling stages |
| Proposed-model Python scripts | 6 | Scripts for correlation analysis, K-Means analysis, Elbow Method, SVM evaluation, MLQ scheduling, and the integrated SVMMLQ-LC model |
| Baseline algorithms | 4 | Random, Round Robin, Weighted Round Robin, and Least-Connection implementations |
| Manuscript figures | 13 | Final figures covering topology, methodology, clustering, scheduling, performance evaluation, and threshold-sensitivity analysis |
| Manuscript tables | 16 | Tables reported in the revised manuscript, including experimental configuration, datasets, comparisons, results, and statistical analysis |

---

## Datasets

The `datasets/` folder contains four CSV files representing successive stages of data preparation.

| Dataset | Records | Features | Description |
|---|---:|---:|---|
| `My-Dataset-Cleaning-Data.csv` | 4,000 | 15 | Flow-level dataset after median-based cleaning of numerical fields |
| `My-Dataset-Feature-Selection.csv` | 4,000 | 8 | Dataset after correlation-based feature selection |
| `My-Dataset-MinMaxScaler.csv` | 4,000 | 8 | Selected features normalized to the range \([0,1]\) |
| `My-Dataset-K-Means.csv` | 4,000 | 9 | Normalized feature set with K-Means cluster labels |

The eight final learning features are:

```text
Packets
Bytes
Packets A to B
Bytes A to B
Packets B to A
Bytes B to A
Bits/s A to B
Bits/s B to A
```

---

## Proposed-Model Code

The `codes/` folder contains six Python scripts.

| Script | Purpose |
|---|---|
| `Pearson-Correlation.py` | Computes and visualizes Pearson correlations among numerical flow-level features |
| `Elbow-method-for-calculate-K-means-and-wirh-n-clusters-12-Loop.py` | Evaluates K-Means inertia and silhouette scores for candidate values of \(k\) |
| `Calculate-of-K-means-with-2-cluster.py` | Applies K-Means clustering with two clusters and visualizes flow groups |
| `SVM-with-validation-set-manually.py` | Trains and evaluates the SVM classifier using clustered traffic labels |
| `Multi-Level-Queue-scheduling-code.py` | Implements the threshold-based two-level MLQ scheduling mechanism |
| `SVMMLQ-LC-Model.py` | Integrates SVM classification, MLQ scheduling, and Least-Connection selection in the POX/OpenFlow controller workflow |

Detailed descriptions and script-specific execution notes are available in `codes/README.md`.

---

## Baseline Algorithms

The `Baseline Algorithms/` folder contains four conventional load-balancing algorithms used for controlled comparison with SVMMLQ-LC.

| Script | Algorithm | Server-Selection Policy |
|---|---|---|
| `R-Algorithm.py` | Random | Selects an available live server randomly |
| `RR-Algorithm.py` | Round Robin | Assigns flows sequentially in cyclic server order |
| `WRR-Algorithm.py` | Weighted Round Robin | Assigns flows according to a predefined server-weight pattern |
| `LC-Algorithm.py` | Least Connection | Selects the server with the fewest active connections |

The baseline implementations are executed under the same controlled Mininet–POX environment, server pool, traffic-generation procedure, and evaluation conditions used for the proposed model.

> The baseline source files retain their original source and copyright notices where applicable.

---

## Figures and Tables

### Figures

The `figures/` folder contains all final figures used in the revised manuscript.

| Group | Figure Numbers | Content |
|---|---|---|
| SDN architecture and workflow | Figures 1–3 | SDN topology, six-stage SVMMLQ-LC workflow, and traffic-generation topology |
| Data preparation and learning | Figures 4–6 | Pearson correlation analysis, Elbow Method, and K-Means clustering results |
| Scheduling mechanism | Figure 7 | Threshold-based two-level MLQ scheduling flowchart |
| Performance evaluation | Figures 8–10 | Comparative performance outcomes for the proposed model and baseline algorithms |
| Threshold sensitivity | Figures 11–13 | Sensitivity analysis of waiting time and Jain’s fairness index under different threshold values |

### Tables

The revised manuscript includes **16 tables** documenting:

- Related-work comparisons.
- Dataset feature definitions.
- Experimental platform and hardware configuration.
- Data preprocessing and feature selection.
- K-Means and SVM evaluation results.
- Baseline and proposed-method comparisons.
- Performance results at multiple traffic loads.
- Statistical analysis and effect-size reporting.
- Threshold-sensitivity outcomes.

The complete tables are available in the revised manuscript.

---

## Experimental Environment

| Parameter | Configuration |
|---|---|
| SDN emulator | Mininet |
| Operating system | Ubuntu Linux 20.04.4 LTS |
| SDN controller | POX |
| OpenFlow version | OpenFlow v1.0 |
| Data-plane switch | Open vSwitch (OVS) |
| Topology | One OpenFlow switch, three client hosts, and three HTTP servers |
| Client addresses | 10.0.0.4, 10.0.0.5, and 10.0.0.6 |
| Server addresses | 10.0.0.1, 10.0.0.2, and 10.0.0.3 |
| Controller address | 10.0.1.1 |
| HTTP file sizes | 1 MB, 10 MB, 25 MB, 50 MB, and 75 MB |
| Dataset size | 4,000 flow records |
| Selected features | 8 numerical flow-level features |
| K-Means configuration | Two clusters |
| SVM configuration | RBF kernel |
| MLQ threshold | \(T = 3\) |
| Statistical analysis | OriginPro 2026 |

---

## Main Evaluation Conditions

The proposed framework and baseline algorithms were evaluated under four traffic loads:

```text
300 requests
3,000 requests
15,000 requests
45,000 requests
```

The evaluation includes time-based metrics, load-distribution measures, fairness analysis, and threshold-sensitivity analysis. The revised manuscript presents the full numerical outcomes and interpretation.

---

## Requirements

### Python Dependencies

Install the required Python packages:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn
```

### SDN Environment

For controller-level execution, the following environment is required:

```text
Mininet
POX controller
Open vSwitch
OpenFlow 1.0
Python
```

Some scripts contain local file paths. Update the input and output paths to match your local directory structure before execution.

---

## Suggested Execution Order

### Offline Data-Analysis Phase

```bash
python "Pearson-Correlation.py"
python "Elbow-method-for-calculate-K-means-and-wirh-n-clusters-12-Loop.py"
python "Calculate-of-K-means-with-2-cluster.py"
python "SVM-with-validation-set-manually.py"
```

### Scheduling and Controller Phase

```bash
python "Multi-Level-Queue-scheduling-code.py"
```

The integrated `SVMMLQ-LC-Model.py` and the baseline algorithms require a configured POX/OpenFlow/Mininet environment.

---

## Reproducibility Notes

- Update all dataset and output paths before running the scripts.
- The clustering and classifier outputs may vary if the input data, random seeds, package versions, or preprocessing choices are changed.
- The controller-level results depend on the Mininet topology, server configuration, traffic-generation settings, and POX/OpenFlow setup.
- Baseline algorithms should be run using the same topology and test conditions as the proposed framework for fair comparison.
- The figures, datasets, source code, baseline algorithms, and manuscript tables correspond to the revised version of the study.

---

## Citation

If you use, adapt, or refer to the repository materials, please cite:

```text
M. A. M. Alrammahi, “SVMMLQ-LC: Proposed Algorithm – Datasets, Source Code, Baseline Algorithms, and Experimental Figures,” GitHub repository, 2026. Available:
https://github.com/maghribalramahi83/sdn-load-balancing/tree/main/Proposed%20SVMMLQ-LC%20Algorithm
```

For the baseline study, please also cite:

```text
M. A. M. Alrammahi and W. S. Bhaya, “Performance Analysis for Load Balancing Algorithms using POX Controller in SDN,” in 2022 International Conference on Data Science and Intelligent Computing (ICDSIC), 2022, pp. 175–180. https://doi.org/10.1109/ICDSIC56987.2022.10076081
```

---

## Corresponding Author

**Maghrib Abidalreda Maky Alrammahi**  
On behalf of Faris Sattar Hadi and Abbas Nasir AlTaee  
University of Kufa — ITRDC, Najaf, Iraq  
Email: [maghrib.alramahi@uokufa.edu.iq](mailto:maghrib.alramahi@uokufa.edu.iq)

## 📜 License

MIT License

---
