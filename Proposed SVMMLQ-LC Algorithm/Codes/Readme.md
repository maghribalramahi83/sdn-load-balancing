# Source Code for the SVMMLQ-LC Framework

This folder contains the Python source-code files used to implement, analyze, and evaluate the proposed SVMMLQ-LC framework described in the manuscript:

> **SVMMLQ-LC: An Intelligent Machine Learning-Based Load-Balancing Framework with Multi-Level Queue Scheduling and Least-Connection Selection for Software-Defined Networking**

The code supports the main stages of the experimental workflow, including correlation analysis, K-Means clustering, cluster-number selection, SVM validation, multi-level queue scheduling, and the integrated SVMMLQ-LC controller model.

## Code Files

### 1. `Pearson-Correlation.py`

Computes the Pearson correlation matrix for numerical flow-level features and generates the correlation heatmap used for feature-selection analysis.

**Main functions:**

- Reads the cleaned flow-level dataset.
- Computes Pearson correlations among numerical traffic features.
- Generates a correlation heatmap.
- Saves the figure in publication-quality PNG format.

---

### 2. `Elbow-method-for-calculate-K-means-and-wirh-n-clusters-12-Loop.py`

Applies the Elbow Method and silhouette-score analysis to evaluate candidate numbers of K-Means clusters.

**Main functions:**

- Evaluates K-Means models for multiple values of \(k\).
- Calculates inertia values for the Elbow Method.
- Calculates silhouette scores for clustering evaluation.
- Generates Elbow and silhouette-score figures.
- Identifies the candidate number of clusters used in the traffic-grouping stage.

---

### 3. `Calculate-of-K-means-with-2-cluster.py`

Performs K-Means clustering using two clusters on the normalized traffic-feature dataset.

**Main functions:**

- Loads the normalized input features.
- Applies K-Means clustering with two clusters.
- Computes cluster centroids, cluster sizes, and silhouette score.
- Generates visualizations before and after clustering.
- Produces the traffic-flow groups used for subsequent SVM classification.

---

### 4. `SVM-with-validation-set-manually.py`

Trains and evaluates the Support Vector Machine classifier using the clustered traffic labels.

**Main functions:**

- Splits the labeled dataset into training, validation, and testing sets.
- Trains an SVM classifier with an RBF kernel.
- Calculates accuracy, precision, recall, and F1-score.
- Generates a confusion matrix and evaluation-metric plots.
- Evaluates training, validation, and testing performance.

---

### 5. `Multi-Level-Queue-scheduling-code.py`

Implements the threshold-based Multi-Level Queue (MLQ) scheduling mechanism.

**Main functions:**

- Creates two traffic queues representing different service priorities.
- Enqueues packets according to their assigned priority.
- Applies a threshold-based service rule.
- Periodically serves the lower-priority queue to reduce starvation.
- Uses a threshold value of 3 in the reported experimental setup.

---

### 6. `SVMMLQ-LC-Model.py`

Contains the integrated prototype of the proposed SVMMLQ-LC controller-side model.

**Main functions:**

- Integrates SVM-based traffic-priority classification.
- Applies threshold-based MLQ scheduling.
- Implements Least-Connection server selection.
- Defines POX/OpenFlow controller event handlers.
- Demonstrates the sequence of classification, queue scheduling, and server-selection decisions in the SDN environment.

## Requirements

The source code was developed using Python and requires the following main libraries:

```text
pandas
numpy
matplotlib
seaborn
scikit-learn
POX
```

The code was developed and evaluated in a Mininet–POX SDN environment. Some scripts require local input datasets and local output paths to be updated before execution.

## Reproducibility Notes

- Update the dataset paths in each script before execution.
- The K-Means and SVM scripts assume that the input data have been preprocessed and normalized.
- The integrated controller script requires a working POX controller and OpenFlow/Mininet environment.
- Script outputs, including figures and metric values, may vary if the dataset, random seed, software versions, or network-testbed configuration differs from that described in the manuscript.

## Related Materials

Supporting datasets, experimental figures, and additional materials are provided in the corresponding folders of this repository.

## Citation

If you use, adapt, or refer to this code, please cite the associated manuscript and repository:

M. A. M. Alrammahi, “SVMMLQ-LC: Proposed Algorithm – Datasets, Source Code, and Experimental Figures,” GitHub repository, May 2026. Available:  
https://github.com/maghribalramahi83/sdn-load-balancing/tree/main/Proposed%20SVMMLQ-LC%20Algorithm
