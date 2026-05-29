"""
Using of KMeans and Calulate Number of data points in cluster 0 and 1
"""

from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.pyplot as plt

path = "E:\\MinMaxScaler.csv"
dataset = pd.read_csv(path, header=None)
X = dataset.iloc[:, 0:8].values
print(X.shape)
kmeans = KMeans(n_clusters= 2,init='k-means++',random_state=33)

kmeans.fit(X)
print('KMeansModel centers are : ' , kmeans.cluster_centers_)
print('KMeansModel labels are : ' , kmeans.labels_)
result = kmeans.labels_

# compute an average silhouette score for each point
#score = silhouette_score(X, kmeans.predict(X))
score = silhouette_score(X, result)

# lets see what that score it
print("Score=:",score)
print("Result = :",result)

counts = np.bincount(kmeans.labels_)
print('Number of data points in cluster 0: ', counts[0])
print('Number of data points in cluster 1: ', counts[1])

# Plot the counts as a bar chart
#fig = plt.figure(dpi=300)
plt.bar([0, 1], counts, tick_label=['Cluster 0', 'Cluster 1'])
plt.title('Number of data points in each cluster',fontsize=12, fontweight='bold')
plt.xlabel('Clusters',fontsize=12, fontweight='bold')
plt.ylabel('Count',fontsize=12, fontweight='bold')
for i, v in enumerate(counts):
    plt.text(i-0.1, v+10, str(v), color='black', fontsize=10, fontweight='bold')
plt.show()