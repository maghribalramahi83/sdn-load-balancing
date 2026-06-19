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

import pandas as pd
import skfuzzy as fuzz
from sklearn.metrics import silhouette_score

path = r"E:\MinMaxScaler.csv"
dataset = pd.read_csv(path, header=None)
X = dataset.iloc[:, 0:8].values

print(X.shape)

cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    X.T,
    c=2,
    m=2,
    error=0.005,
    maxiter=1000,
    init=None
)

labels = u.argmax(axis=0)
score = silhouette_score(X, labels)

print("Silhouette Score:", score)