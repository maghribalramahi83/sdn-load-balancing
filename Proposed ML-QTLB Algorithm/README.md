ML-QTLB: A Hybrid Machine Learning and Queueing-Theory Model for Server-Side Load Balancing in SDN
Authors: Maghrib Abidalreda Maky Alrammahi¹*, Mohanad Yahya Al-hamami¹, Ali Mohammed Taher²

¹ Information Technology Research and Development Centre (ITRDC), University of Kufa, Najaf, Iraq
² Faculty of Basic Education, Department of Mathematics, University of Kufa, Najaf, Iraq
* Corresponding author: maghrib.alramahi@uokufa.edu.iq

📌 Overview
This repository contains the complete implementation of the ML-QTLB model, including datasets, Python source code, architectural diagrams, implementation figures, statistical validation material, and performance evaluation results.

ML-QTLB is a hybrid load balancing framework for Software-Defined Networking (SDN) that integrates:

Fuzzy C-Means (FCM) for unsupervised traffic clustering

Random Forest (RF) for supervised real-time traffic classification

M/M/1 Queueing Theory (QT) for optimal server selection (minimum expected system time)

Aging-based starvation prevention for fairness-aware scheduling

The framework was implemented and evaluated in a Mininet-based SDN testbed using POX as the controller, Open vSwitch (OVS) with OpenFlow v1.0 as the data plane, and Wireshark on Linux for traffic capture and dataset construction. The final dataset contains 25,000 flow records collected from controlled traffic generated between 3 clients and 3 servers using files ranging from 1 MB to 75 MB.

✨ Key Features
Hybrid ML + Queueing-Theory load balancing framework (five sequential stages)

Real traffic dataset captured from a Mininet SDN environment with Wireshark

Three-stage preprocessing: cleaning (mean imputation), feature selection (15 → 8), Min-Max normalization [0, 1]

FCM clustering with K = 2, validated by Silhouette analysis (peak score ≈ 0.53)

RF traffic classifier with 99.88% accuracy vs. 79.4% for the SVM baseline

M/M/1-based server selection using 
𝜆
𝑘
λ 
k
​
 , 
𝜇
𝑘
μ 
k
​
 , 
𝜌
𝑘
ρ 
k
​
 , and 
𝑊
𝑘
W 
k
​
 ; overloaded servers (
𝜌
𝑘
≥
1
ρ 
k
​
 ≥1) are excluded by setting 
𝑊
𝑘
=
∞
W 
k
​
 =∞

Aging-based anti-starvation mechanism with threshold T = 3.0 s (bounded latency, Jain's Fairness Index > 0.99)

Statistical validation of all improvements (Mean PI%, SD, 95% CI, box plots)

Comparative evaluation against:

Classical algorithms: RR, Random, WRR, LC

Server-metric-based algorithms: LRAM, LCPU, LCPURAM, LC, LCLCPURAM

📂 Repository Contents
🏗️ Architectural & Methodology Figures
File	Paper Figure	Description
Figure_1_Overall_Architecture.png	Fig. 1	Overall architecture of the proposed ML-QTLB framework (ML module, QT scheduler, SDN controller)
Figure_2_Network_Topology.png	Fig. 2	Single-switch Mininet topology: 3 clients (10.0.0.4–10.0.0.6), 3 web servers (10.0.0.1–10.0.0.3), 1 OVS, 1 POX controller (10.0.1.1)
Figure_3_Stages_of_Proposed_Model.png	Fig. 3	Five sequential stages of the ML-QTLB model, from traffic generation to QT scheduling
🖼️ Implementation & Analysis Figures
File	Paper Figure	Description
Figure_4_Wireshark_Capturing.png	Supplementary	Wireshark capturing traffic in the Mininet SDN environment
Figure_5_Generation_Requests.png	Supplementary	Traffic generation process between clients and servers
Figure_6_Correlation_Matrix_13Features.png	Supplementary	Correlation matrix heatmap used to support feature selection
Figure_7_Silhouette_Analysis_K10.png	Fig. 4	Silhouette score analysis for K = 2 to 10 (optimal K = 2, score ≈ 0.53)
Figure_8_Confusion_Matrix_RFC.png	Supplementary	Confusion matrix of the RF classifier (99.88% accuracy)
Figure_9_ML_QTLB_Run_Proposed_Algorithm.png	Supplementary	ML-QTLB algorithm running in POX within the Mininet testbed
📈 Performance Result Figures
File	Paper Figure	Description
Figure_10_Result_Average_Response_Time.png	Fig. 5	Average Response Time comparison vs. classical algorithms
Figure_11_Result_Degree_of_Load_Balancing.png	Fig. 6	Degree of Load Balancing comparison vs. classical algorithms
Figure_12_Result_Waiting_Time.png	Fig. 7	Waiting Time comparison vs. server-metric-based algorithms
Figure_13_Result_Service_Time.png	Fig. 8	Service Time comparison vs. server-metric-based algorithms
🛡️ Starvation-Prevention & Fairness Figures
File	Paper Figure	Description
Figure_14_P99_With_vs_Without_Aging.png	Fig. 9	Class-1 P99 tail latency with vs. without aging (80/20 traffic mix)
Figure_15_JFI_With_vs_Without_Aging.png	Fig. 10	Jain's Fairness Index with vs. without aging (80/20 traffic mix)
Figure_16_Class1_Tail_Latency_Loads.png	Fig. 11	Class-1 tail latency across request loads (with vs. without aging)
Figure_17_P99_vs_Threshold_T.png	Fig. 12	P99 tail latency vs. aging threshold T at 40,000 requests
Figure_18_JFI_vs_Threshold_T.png	Fig. 13	Jain's Fairness Index vs. aging threshold T at 40,000 requests
📊 Statistical Validation Figures (Box Plots)
File	Paper Figure	Description
Figure_19_Boxplot_ResponseTime_PI.png	Fig. 14	Distribution of Response Time PI% across load levels (N = 4)
Figure_20_Boxplot_LoadBalancing_PI.png	Fig. 15	Distribution of Degree of Load Balancing PI% (N = 4)
Figure_21_Boxplot_WaitingTime_PI.png	Fig. 16	Distribution of Waiting Time PI% (N = 2)
Figure_22_Boxplot_ServiceTime_PI.png	Fig. 17	Distribution of Service Time PI% (N = 2)
📊 Datasets
All datasets contain 25,000 records captured from the Mininet-based SDN testbed using Wireshark on Linux.

Traffic files used for generation: 1 MB, 10 MB, 25 MB, 50 MB, and 75 MB

File	Records	Features	Description
DS1_15Features.csv	25,000	15	Raw Wireshark-captured dataset with original traffic features
DS1_FeatureSelection_8Features.csv	25,000	8	Dataset after feature selection (15 → 8)
DS1_Normalization.csv	25,000	8	Dataset after Min-Max normalization to [0, 1]
DS1_FuzzyCMeans_K2.csv	25,000	9	Dataset after FCM clustering with K = 2, including the cluster label
Raw Dataset Features (15 features — Table 8 in the paper)
No.	Feature	Description	Retained
1	S	Number of requests	✗
2	Address A	Source IP address	✗
3	Port A	Source port number	✗
4	Address B	Destination IP address	✗
5	Port B	Destination port number	✗
6	Packets	Total packets exchanged (A↔B)	✓
7	Bytes	Total bytes exchanged (A↔B)	✓
8	Packets A→B	Packets sent from source to destination	✓
9	Bytes A→B	Bytes sent from source to destination	✓
10	Packets B→A	Packets sent from destination to source	✓
11	Bytes B→A	Bytes sent from destination to source	✓
12	Rel Start	Relative session start time (s)	✗
13	Duration	Session duration (s)	✗
14	Bits/s A→B	Average data rate from A to B (bits/s)	✓
15	Bits/s B→A	Average data rate from B to A (bits/s)	✓
The 8 retained features capture traffic volume, direction, and throughput — the characteristics most relevant to queueing behaviour and load balancing decisions. IP addresses, port numbers, and session timing are excluded because they do not contribute to load characterization.

Traffic Clusters (FCM, K = 2)
Cluster	Traffic Type	Bytes	Packets	Bits/s A→B	Bits/s B→A	Scheduling Priority
Cluster 1	Light / low-load	Low	Low	Low	Low	Low priority (subject to aging)
Cluster 2	Heavy / high-load	High	High	High	High	High priority
🐍 Python Files
File	Description
Generate Traffic Files Locally.py	Generates the five dummy binary traffic files (1–75 MB)
Mininet Topology.py	Exact Mininet topology (3 clients, 3 servers, 1 OVS, 1 POX controller)
Cleaning Data.py	Data cleaning with mean-based imputation (no records discarded)
Calculate of Data Scaling.py	Min-Max normalization to the range [0, 1]
Calculate of Silhouette analysis.py	Silhouette analysis for K = 2 to 10
Calculate of FCM_Silhouette.py	FCM clustering with K = 2 and cluster labelling
RF_Classifier_with_Validation.py	RF training/validation (train / validation / test split, metrics, confusion matrix) and SVM comparison
ML_QTLB_RF_QT_Controller.py	Full ML-QTLB POX controller: RF classification + M/M/1 QT scheduling + aging-based starvation prevention
ML_QTLB_Client_Metrics.py	Client-side script computing RT, WT, ST, and Degree of LB
⚖️ Baseline Algorithm Implementations
File	Algorithm	Type	Selection Criterion
RR Algorithm.py	Round Robin	Classical	Sequential rotation (no parameters)
Random Algorithm.py	Random	Classical	Random server selection
WRR Algorithm.py	Weighted Round Robin	Classical	Weight-based rotation (equal weights, w = 2)
LC Algorithm.py	Least Connection	Classical	Minimum active connections
LRAM Algorithm.py	Least RAM	Server-Metric	Minimum real-time RAM utilization (%)
LCPU Algorithm.py	Least CPU	Server-Metric	Minimum real-time CPU utilization (%)
LCPURAM Algorithm.py	Least CPU + RAM	Server-Metric	Minimum combined CPU + RAM utilization
LCLCPURAM Algorithm.py	LC + CPU + RAM	Server-Metric	Minimum combined connections + CPU + RAM
📁 Traffic Generation Files
Five dummy binary files were used to generate controlled traffic in the Mininet SDN environment.

File	Size	Type	Purpose
file_1MB.bin	1 MB	Binary	Low traffic load
file_10MB.bin	10 MB	Binary	Light traffic load
file_25MB.bin	25 MB	Binary	Medium traffic load
file_50MB.bin	50 MB	Binary	Heavy traffic load
file_75MB.bin	75 MB	Binary	Maximum traffic load
⚠️ These binary files are not included in the repository because of GitHub size limitations. Regenerate them locally with the script below.

Generate Traffic Files Locally
python
sizes = [1, 10, 25, 50, 75]

for s in sizes:
    filename = f'file_{s}MB.bin'
    with open(filename, 'wb') as f:
        f.write(b'\0' * s * 1024 * 1024)
    print(f"Created: {filename} ({s} MB)")

print("All traffic files generated successfully.")
Example Traffic Transfer Command
python
import subprocess
subprocess.run(['scp', 'file_1MB.bin', 'server@10.0.0.1:/tmp/'])
⚙️ ML-QTLB Pipeline
The ML-QTLB framework operates in five sequential stages:

Traffic Generation & Dataset Construction
Input: Mininet topology on Linux → Output: raw dataset (25,000 × 15).
Controlled traffic (1–75 MB files) is transmitted between C1–C3 and S1–S3 and captured with Wireshark.

Preprocessing
Input: 25,000 × 15 → Output: 25,000 × 8 normalized.
Mean-based cleaning, feature selection (15 → 8), Min-Max normalization to [0, 1].

FCM Clustering
Input: 25,000 × 8 → Output: cluster labels.
K = 2 selected by Silhouette analysis (K ∈ {2, …, 10}, best score ≈ 0.53).

RF Classification
Input: labelled dataset → Output: trained RF model (99.88% accuracy).
RF is trained on FCM-derived labels and deployed in the POX controller for real-time classification.

QT Scheduling with Aging
Input: traffic class, real-time λ and μ per server → Output: selected server.
M/M/1-based selection of the minimum 
𝑊
𝑘
W 
k
​
 , with aging-based promotion of long-waiting low-priority flows.

Real-Time Decision Logic (per request)
Extract the 8 features from the incoming request.

Classify with RF → Class 1 (low priority) or Class 2 (high priority).

Compute 
𝜆
𝑘
,
𝜇
𝑘
,
𝜌
𝑘
,
𝑊
𝑘
λ 
k
​
 ,μ 
k
​
 ,ρ 
k
​
 ,W 
k
​
  for all servers from live POX counters.

Promote any pending Class-1 request whose accumulated waiting time ≥ T = 3.0 s.

Select 
𝑆
∗
=
arg
⁡
min
⁡
𝑊
𝑘
S 
∗
 =argminW 
k
​
  among eligible servers, prioritizing promoted requests.

Install/update the flow rule in OVS via OpenFlow to route the request to 
𝑆
∗
S 
∗
 .

🛠️ Experimental Environment
Parameter	Value
Emulator	Mininet
OS	Ubuntu 20.04.4 LTS (64-bit)
Python	3.8
Controller	POX (single controller, 10.0.1.1)
Switch	1 × OVS (OpenFlow v1.0)
Topology	Single-switch topology
Clients	3 — C1, C2, C3 (10.0.0.4–10.0.0.6)
Servers	3 — S1, S2, S3 (10.0.0.1–10.0.0.3), homogeneous web servers
Per-server resources	Intel Core i7-3625QM, 8 cores, 8 GB RAM
CPU	Intel Core i7-3625QM 2.2 GHz × 8
RAM	8 GB
Graphics	AMD/Intel 4000
Storage	512 GB SSD
Flow rules	idle_timeout = 10 s, hard_timeout = 30 s
🤖 Model Configuration, Pre-trained Model & Documentation
RF Hyperparameters and Data Split
Parameter	Value
criterion	entropy
n_estimators	80
max_depth	4
min_samples_split	7
random_state	0
Test set	24% (test_size = 0.24, random_state = 42)
Train / Validation	remaining 76%, split 50/50 (val_size = 0.50, random_state = 42)
RF accuracy	99.88%
SVM baseline accuracy	79.4%
File	Description
rf_model.pkl	Pre-trained RF model — load directly without retraining
hyperparameters_and_seeds.md	All hyperparameters, random seeds, and software environment
Load Pre-trained Model
python
import joblib
model = joblib.load('rf_model.pkl')
prediction = model.predict([features])
🚀 How to Run
Requirements
bash
pip install pandas numpy scikit-learn matplotlib seaborn joblib scikit-fuzzy
Step 1: Preprocess Data
bash
python "Cleaning Data.py"
python "Calculate of Data Scaling.py"
python "Calculate of Silhouette analysis.py"
python "Calculate of FCM_Silhouette.py"
Step 2: Train RF Classifier (or use the pre-trained model)
bash
python "RF_Classifier_with_Validation.py"
# Output: rf_model.pkl
Step 3: Start Mininet Topology
bash
sudo python "Mininet Topology.py"
Step 4: Run POX Controller (ML-QTLB)
bash
cd ~/pox
./pox.py log.level --DEBUG ext.ML_QTLB_RF_QT_Controller
Step 5: Run Client Metrics Script
bash
python "ML_QTLB_Client_Metrics.py"
# Outputs: Average RT, WT, ST, Degree of LB
Step 6: Run Baseline Algorithms (for comparison)
bash
# Example: Round Robin
./pox.py log.level --DEBUG ext.RR_Algorithm

# Example: Least Connection
./pox.py log.level --DEBUG ext.LC_Algorithm
Each algorithm is tested in an independent Mininet session to avoid cross-experiment interference.

📈 Results Summary
Average Response Time (s) vs. Classical Algorithms — Table 12
No. of Requests	RR	Random	WRR	LC	ML-QTLB
300	0.01417	0.01372	0.01349	0.01497	0.0066
3,000	0.01452	0.01457	0.01443	0.01463	0.0084
15,000	0.01666	0.01473	0.01450	0.01485	0.0109
45,000	0.01745	0.01458	0.01454	0.01466	0.0123
Mean PI (%)	39.91	33.97	33.28	35.30	—
Degree of Load Balancing vs. Classical Algorithms — Table 13
No. of Requests	RR	Random	WRR	LC	ML-QTLB
300	56.6609	59.1226	52.1173	56.6124	81.50
3,000	57.7261	59.4615	58.7473	58.0368	75.40
15,000	64.0122	58.7697	58.3562	58.0673	69.44
45,000	66.7630	58.6936	58.4549	58.4451	68.35
Mean PI (%)	21.33	24.82	30.16	27.60	—
Waiting Time (s) vs. Server-Metric-Based Algorithms — Table 14
No. of Requests	LRAM	LCPU	LCPURAM	LC	LCLCPURAM	ML-QTLB
8,000	0.158	0.0730	0.0738	0.0738	0.0741	0.00843
40,000	0.160	0.0755	0.0747	0.0742	0.0726	0.01021
Mean PI (%)	94.14	87.46	87.46	87.41	87.28	—
Service Time (s) vs. Server-Metric-Based Algorithms — Table 15
No. of Requests	LRAM	LCPU	LCPURAM	LC	LCLCPURAM	ML-QTLB
8,000	0.020	0.0164	0.0079	0.0079	0.0084	0.00107
40,000	0.021	0.0083	0.0085	0.0083	0.0085	0.00129
Mean PI (%)	94.26	88.97	85.64	85.46	86.04	—
Overall Improvement Summary — Table 16
Metric	vs. RR	vs. Random	vs. WRR	vs. LC	vs. LRAM	vs. LCPU	vs. LCPURAM	vs. LCLCPURAM
Average Response Time (Mean PI %)	39.91	33.79	33.28	35.30	—	—	—	—
Degree of Load Balancing (Mean PI %)	21.33	24.82	30.16	27.60	—	—	—	—
Waiting Time (Mean PI %)	—	—	—	87.41	94.14	87.46	87.46	87.28
Service Time (Mean PI %)	—	—	—	85.46	94.26	88.97	85.64	86.04
🛡️ Starvation Prevention and Fairness
A calibrated M/M/1 event-driven simulation was performed using testbed parameters (T = 3.0 s; waiting-time distributions calibrated to the measured 0.00843 s and 0.01021 s at 8,000 and 40,000 requests). An 80% Class-2 / 20% Class-1 traffic mix is used as a stress test to maximize starvation pressure.

Class-1 P99 and Fairness, With vs. Without Aging — Table 17
Requests	P99 Without Aging (s)	P99 With Aging (s)	JFI Without Aging	JFI With Aging
300	0.034	0.027	0.912	0.996
1,000	0.048	0.027	0.924	0.999
8,000	0.185	0.037	0.650	0.992
40,000	0.939	0.045	0.539	0.995
Class-1 Tail Latency, With vs. Without Aging (T = 3.0 s) — Table 18
Requests	Aging	Mean (s)	P95 (s)	P99 (s)	Max (s)	JFI
300	Without	0.00679	0.01688	0.01861	0.01892	0.992
300	With	0.00529	0.01467	0.03032	0.03151	1.000
1,000	Without	0.00855	0.02316	0.03277	0.03447	0.965
1,000	With	0.00668	0.02181	0.03009	0.04103	0.994
8,000	Without	0.04531	0.12964	0.19739	0.38270	0.646
8,000	With	0.00796	0.02562	0.04133	0.07240	0.994
40,000	Without	0.21209	0.62980	0.96803	1.83031	0.538
40,000	With	0.00912	0.02807	0.04561	0.08655	0.997
Aging Threshold Sensitivity at 40,000 Requests — Table 19
Threshold T	Mean (s)	P99 (s)	JFI
1.0 s (0.33×T)	0.00936	0.04546	0.9954
2.0 s (0.67×T)	0.00935	0.04517	0.9954
3.0 s (default T*)	0.00938	0.04576	0.9955
6.0 s (2×T)	0.00942	0.04494	0.9950
15.0 s (5×T)	0.00952	0.04490	0.9936
No Aging (∞)	0.20993	0.97325	0.5386
Performance is robust to reasonable perturbations of T (P99 varies by < 0.001 s, JFI by < 0.002), whereas disabling aging degrades tail latency by more than 20× and fairness by about 46%.

📐 Statistical Validation
Percentage improvement (PI%) is computed per load level and aggregated as a mean across all levels.

For metrics where lower is better (RT, WT, ST):

𝑃
𝐼
%
=
𝐵
𝑎
𝑠
𝑒
𝑙
𝑖
𝑛
𝑒
−
𝑃
𝑟
𝑜
𝑝
𝑜
𝑠
𝑒
𝑑
𝐵
𝑎
𝑠
𝑒
𝑙
𝑖
𝑛
𝑒
×
100
PI%= 
Baseline
Baseline−Proposed
​
 ×100
For metrics where higher is better (Degree of LB):

𝑃
𝐼
%
=
𝑃
𝑟
𝑜
𝑝
𝑜
𝑠
𝑒
𝑑
−
𝐵
𝑎
𝑠
𝑒
𝑙
𝑖
𝑛
𝑒
𝐵
𝑎
𝑠
𝑒
𝑙
𝑖
𝑛
𝑒
×
100
PI%= 
Baseline
Proposed−Baseline
​
 ×100
Overall mean improvement across N load levels:

𝑃
𝐼
%
‾
=
1
𝑁
∑
𝑖
=
1
𝑁
𝑃
𝐼
%
(
𝐿
𝑖
)
PI%
​
 = 
N
1
​
  
i=1
∑
N
​
 PI%(L 
i
​
 )
Average Response Time PI% — Table 20 (N = 4)
Algorithm	Mean PI%	SD	95% CI	Min PI%	Max PI%
RR	39.91	10.40	[23.37, 56.45]	29.51	53.42
Random	33.96	16.24	[8.12, 59.81]	15.64	51.89
WRR	33.28	16.12	[7.63, 58.92]	15.42	51.07
LC	35.30	17.53	[7.40, 63.19]	16.10	55.91
Degree of Load Balancing PI% — Table 21 (N = 4)
Algorithm	Mean PI%	SD	95% CI	Min PI%	Max PI%
RR	21.34	19.31	[-9.38, 52.05]	2.38	43.86
Random	24.81	9.81	[9.19, 40.42]	16.42	37.85
WRR	30.17	18.17	[1.25, 59.08]	16.91	56.38
LC	27.61	12.25	[8.11, 47.11]	16.98	43.97
Waiting Time PI% — Table 22 (N = 2)
Algorithm	Mean PI%	SD	95% CI	Min PI%	Max PI%
LRAM	94.14	0.74	[87.53, 100.75]	93.62	94.66
LCPU	87.47	1.39	[74.95, 99.98]	86.48	88.45
LCPURAM	87.46	1.60	[73.10, 100.00]	86.33	88.59
LC	87.42	1.66	[72.49, 100.00]	86.24	88.59
LCLCPURAM	87.24	1.83	[70.78, 100.00]	85.94	88.53
Service Time PI% — Table 23 (N = 2)
Algorithm	Mean PI%	SD	95% CI	Min PI%	Max PI%
LRAM	94.26	0.56	[89.24, 99.27]	93.86	94.65
LCPU	88.97	6.38	[31.67, 100.00]	84.46	93.48
LCPURAM	85.64	1.16	[75.22, 96.06]	84.82	86.46
LC	85.46	1.41	[72.75, 98.17]	84.46	86.46
LCLCPURAM	86.04	1.73	[70.54, 100.00]	84.82	87.26
🧠 Mathematical Model
For each server 
𝑆
𝑘
S 
k
​
 , 
𝑘
∈
{
1
,
2
,
3
}
k∈{1,2,3}, the controller computes online from POX counters:

Arrival rate: 
𝜆
𝑘
=
arrived requests
elapsed time
λ 
k
​
 = 
elapsed time
arrived requests
​
  (requests/s)

Service rate: 
𝜇
𝑘
=
completed requests
elapsed time
μ 
k
​
 = 
elapsed time
completed requests
​
  (requests/s)

Utilization: 
𝜌
𝑘
=
𝜆
𝑘
𝜇
𝑘
ρ 
k
​
 = 
μ 
k
​
 
λ 
k
​
 
​
  (dimensionless, stability requires 
𝜌
𝑘
<
1
ρ 
k
​
 <1)

Expected system time: 
𝑊
𝑘
=
1
/
𝜇
𝑘
1
−
𝜌
𝑘
W 
k
​
 = 
1−ρ 
k
​
 
1/μ 
k
​
 
​
 , for 
𝜌
𝑘
<
1
ρ 
k
​
 <1; otherwise 
𝑊
𝑘
=
∞
W 
k
​
 =∞

The selected server is:

𝑆
∗
=
arg
⁡
min
⁡
𝑘
𝑊
𝑘
S 
∗
 =arg 
k
min
​
 W 
k
​
 
Starvation prevention: a low-priority request 
𝑟
r is promoted to high priority when its accumulated waiting time satisfies 
𝑊
𝑟
≥
𝑇
W 
r
​
 ≥T, with 
𝑇
=
3.0
T=3.0 s. Note that 
𝜆
𝑘
λ 
k
​
  and 
𝜇
𝑘
μ 
k
​
  are measured live at the controller and are independent of the Wireshark dataset and the FCM/RF pipeline, which are used only for traffic-class identification.

⚠️ Limitations
Single-switch topology — three clients and three servers; results may differ in multi-switch, multi-controller deployments.

M/M/1 approximation — Poisson arrivals and exponential service times are assumed; 
𝑊
𝑘
W 
k
​
  is used as a relative ranking criterion rather than an exact predictor.

Fixed aging threshold — T is set empirically; the optimal value may vary with traffic pattern and topology.

Binary traffic classification — only light/heavy classes; finer granularity may be needed in production.

Static classifier — the RF model is trained offline and does not adapt to concept drift.

📖 Citation
If you use this repository in your research, please cite:

text
@article{alrammahi2026mlqtlb,
  author  = {Alrammahi, Maghrib Abidalreda Maky and Al-hamami, Mohanad Yahya and Taher, Ali Mohammed},
  title   = {ML-QTLB: A Hybrid Machine Learning and Queueing-Theory Model for Server-Side Load Balancing in SDN},
  journal = {International Journal of Intelligent Engineering and Systems},
  year    = {2026}
}
Related prior work by the authors:

M. A. M. Alrammahi and W. S. Bhaya, "Performance Analysis for Load Balancing Algorithms using POX Controller in SDN," ICDSIC 2022, pp. 175–180. DOI: 10.1109/ICDSIC56987.2022.10076081

M. A. M. Alrammahi, "Optimizing Server-Side Dynamic Load Balancing in SDN Using Novel Algorithms Based on CPU, RAM, and Connection Metrics," IJARCS, vol. 17, no. 1, pp. 21–27, 2026. DOI: 10.26483/ijarcs.v17i1.7401

📬 Contact
Maghrib Abidalreda Maky Alrammahi
University of Kufa — ITRDC, Najaf, Iraq
Email: maghrib.alramahi@uokufa.edu.iq

📜 License
This project is released under the MIT License.
