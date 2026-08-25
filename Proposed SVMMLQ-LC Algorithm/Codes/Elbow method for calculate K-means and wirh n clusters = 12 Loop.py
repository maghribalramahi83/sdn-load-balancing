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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# إعداد الخط العام
mpl.rcParams["font.family"] = "Times New Roman"
mpl.rcParams["font.size"] = 10

# مسار ملف CSV الجديد
file_path = (
    r"D:\My papers\Paper 8 - SVMMLQLC - 29-5-2026 Sent to Journal Européen des Systèmes الفرنسيه"
    r"\Github\My Dataset - k Mena.csv"
)

# مسارات الإخراج
output_elbow = (
    r"D:\My papers\Paper 8 - SVMMLQLC - 29-5-2026 Sent to Journal Européen des Systèmes الفرنسيه"
    r"\Github\Elbow_Method_TNR10pt_300dpi.png"
)

output_silhouette_scores = (
    r"D:\My papers\Paper 8 - SVMMLQLC - 29-5-2026 Sent to Journal Européen des Systèmes الفرنسيه"
    r"\Github\Silhouette_Scores_TNR10pt_300dpi.png"
)

# قراءة CSV
dataset = pd.read_csv(file_path, header=None)
X = dataset.iloc[:, 0:8].values

# ===== Elbow Method =====
inertias = []
k_values = range(2, 11)

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=0, n_init="auto")
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

fig, ax = plt.subplots(figsize=(6.5, 4.0), dpi=300)

ax.plot(k_values, inertias, marker='o', color='blue')

for k, inertia in zip(k_values, inertias):
    ax.text(
        k, inertia + 3, f"{inertia:.2f}",
        fontsize=10,
        ha='center',
        va='bottom',
        fontfamily="Times New Roman"
    )

ax.set_xlabel("Number of clusters", fontsize=10, fontweight="bold")
ax.set_ylabel("Inertias", fontsize=10, fontweight="bold")
ax.set_title("Using the Elbow Method", fontsize=12, fontweight="bold")
ax.tick_params(axis='both', labelsize=10)
ax.grid(False)

plt.tight_layout()
plt.savefig(output_elbow, dpi=300, bbox_inches="tight")
plt.show()

# ===== Silhouette Scores (اختياري) =====
silhouette_scores = []

for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=0, n_init="auto")
    labels = kmeans.fit_predict(X)
    s_score = silhouette_score(X, labels)
    silhouette_scores.append(s_score)

optimal_k = np.argmax(silhouette_scores) + 2
print("Optimal number of clusters (by silhouette):", optimal_k)

fig2, ax2 = plt.subplots(figsize=(6.5, 4.0), dpi=300)

ax2.plot(range(2, 11), silhouette_scores, marker='o', color='green')
ax2.set_xlabel("Number of clusters", fontsize=10, fontweight="bold")
ax2.set_ylabel("Silhouette score", fontsize=10, fontweight="bold")
ax2.set_title("Silhouette Scores for Different k", fontsize=12, fontweight="bold")
ax2.tick_params(axis='both', labelsize=10)

plt.tight_layout()
plt.savefig(output_silhouette_scores, dpi=300, bbox_inches="tight")
plt.show()