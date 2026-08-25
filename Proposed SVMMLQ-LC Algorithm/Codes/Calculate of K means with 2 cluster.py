"""
Copyright (c) 2026
Maghrib Abidalreda Maky Alrammahi
Email: maghrib.alramahi@uokufa.edu.iq

This code is part of the SVNMLQ-LC research project and was prepared solely by
Maghrib Abidalreda Maky Alrammahi.

Any use of this code, in whole or in part, in research, academic publication,
software development, reproduction, or derivative work should acknowledge the
author by citing the published ML-QTLB paper and referencing the official
project GitHub repository.

Official GitHub repository:
https://github.com/maghribalramahi83/sdn-load-balancing
""" 

"""
K-Means clustering:
1) Data points before clustering
2) Data points after clustering

Output format:
- Times New Roman
- 10 pt body text
- 300 DPI
- Two separate PNG images
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ==========================================
# 1) Figure style required by the editor
# ==========================================

mpl.rcParams["font.family"] = "Times New Roman"
mpl.rcParams["font.size"] = 10

# ==========================================
# 2) Input and output paths
# ==========================================

file_path = (
    r"D:\My papers\Paper 8 - SVMMLQLC - 29-5-2026 Sent to Journal Européen des Systèmes الفرنسيه"
    r"\Github\My Dataset - k Mena.csv"
)

output_before = (
    r"D:\My papers\Paper 8 - SVMMLQLC - 29-5-2026 Sent to Journal Européen des Systèmes الفرنسيه"
    r"\Github\KMeans_Before_Clustering_TNR10pt_300dpi.png"
)

output_after = (
    r"D:\My papers\Paper 8 - SVMMLQLC - 29-5-2026 Sent to Journal Européen des Systèmes الفرنسيه"
    r"\Github\KMeans_After_Clustering_TNR10pt_300dpi.png"
)

# ==========================================
# 3) Load data and train K-Means
# ==========================================

dataset = pd.read_csv(file_path, header=None)

# K-Means training using the first eight normalized features
X = dataset.iloc[:, 0:8].values

# Plot uses the first two features only
X_plot = X[:, 0:2]

print("Dataset shape:", X.shape)

kmeans = KMeans(
    n_clusters=2,
    init="k-means++",
    random_state=33,
    n_init="auto"
)

labels = kmeans.fit_predict(X)
centers = kmeans.cluster_centers_

# Centroids converted to the two displayed features
centers_plot = centers[:, 0:2]

score = silhouette_score(X, labels)
counts = np.bincount(labels, minlength=2)

print("K-Means centers:\n", centers)
print("K-Means labels:\n", labels)
print("Silhouette score:", score)
print("Number of data points in cluster 0:", counts[0])
print("Number of data points in cluster 1:", counts[1])

# ==========================================
# 4) Figure before clustering
# ==========================================

fig1, ax1 = plt.subplots(figsize=(6.5, 4.8), dpi=300)

ax1.scatter(
    X_plot[:, 0],
    X_plot[:, 1],
    s=18,
    c="blue",
    alpha=0.55,
    edgecolors="none"
)

ax1.set_xlabel(
    "Feature 1",
    fontsize=10,
    fontweight="bold",
    fontfamily="Times New Roman"
)

ax1.set_ylabel(
    "Feature 2",
    fontsize=10,
    fontweight="bold",
    fontfamily="Times New Roman"
)

ax1.set_title(
    "Data Points Before K-Means Clustering",
    fontsize=12,
    fontweight="bold",
    fontfamily="Times New Roman"
)

ax1.tick_params(axis="both", labelsize=10)
ax1.grid(False)

plt.tight_layout()

fig1.savefig(
    output_before,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# 5) Figure after K-Means clustering
# ==========================================

fig2, ax2 = plt.subplots(figsize=(6.5, 4.8), dpi=300)

cluster_colors = ["#4C1D6F", "#FDE047"]
cluster_names = ["Cluster 0", "Cluster 1"]

for cluster_id in range(2):
    mask = labels == cluster_id

    ax2.scatter(
        X_plot[mask, 0],
        X_plot[mask, 1],
        s=18,
        c=cluster_colors[cluster_id],
        alpha=0.65,
        edgecolors="none",
        label=f"{cluster_names[cluster_id]} (n={counts[cluster_id]})"
    )

# Centroids
ax2.scatter(
    centers_plot[:, 0],
    centers_plot[:, 1],
    s=150,
    c="red",
    marker="o",
    edgecolors="black",
    linewidths=0.8,
    label="Centroids",
    zorder=5
)

ax2.set_xlabel(
    "Feature 1",
    fontsize=10,
    fontweight="bold",
    fontfamily="Times New Roman"
)

ax2.set_ylabel(
    "Feature 2",
    fontsize=10,
    fontweight="bold",
    fontfamily="Times New Roman"
)

ax2.set_title(
    "Data Points After K-Means Clustering",
    fontsize=12,
    fontweight="bold",
    fontfamily="Times New Roman"
)

ax2.tick_params(axis="both", labelsize=10)

legend = ax2.legend(
    loc="upper left",
    frameon=True,
    prop={
        "family": "Times New Roman",
        "size": 10
    }
)

ax2.grid(False)

plt.tight_layout()

fig2.savefig(
    output_after,
    dpi=300,
    bbox_inches="tight"
)

plt.show()