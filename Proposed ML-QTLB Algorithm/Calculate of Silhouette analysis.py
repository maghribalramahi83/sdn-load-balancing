"""
Copyright (c) 2026
Maghrib Abidalreda Maky Alrammahi
Email: maghrib.alramahi@uokufa.edu.iq

This code is part of the ML-QTLB research project and was prepared solely by
Maghrib Abidalreda Maky Alrammahi.

Any use of this code, in whole or in part, in research, academic publication,
software development, reproduction, or derivative work should acknowledge the
author by citing the published ML-QTLB paper and referencing the official
project GitHub repository.

Official GitHub repository:
https://github.com/maghribalramahi83/sdn-load-balancing
"""

"""
 method his name : Silhouette analysis:
"""
import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.pyplot as plt

path = "E:\\MinMaxScaler.csv"
dataset = pd.read_csv(path, header=None)
X = dataset.iloc[:, 0:8].values
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
from sklearn.cluster import KMeans
import numpy as np

# assume data is a numpy array of shape (n_samples, n_features)
kmeans = KMeans(n_clusters=2)
kmeans.fit(X)
labelskmeans = kmeans.labels_
score = silhouette_score(X, labelskmeans)
print("Score of kmeans=:",score* 100, "%")


from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np

# Compute silhouette scores for different values of k
silhouette_scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k)
    labels = kmeans.fit_predict(X)
    silhouette_scores.append(silhouette_score(X, labels))

# Plot silhouette scores for different values of k
plt.plot(range(2, 11), silhouette_scores, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette score')
plt.show()

# Print the optimal number of clusters
optimal_k = np.argmax(silhouette_scores) + 2
print("Optimal number of clusters:", optimal_k)

#--------------------------------------------------------------