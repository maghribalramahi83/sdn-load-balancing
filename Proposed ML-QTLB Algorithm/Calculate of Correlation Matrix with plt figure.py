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
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("E:\\my dataset cleaning data.csv")
features = ["S", "Address A", "Port A", "Address B", "Port B",           "Packets", "Bytes", "Packets A to B", "Bytes A to B", "Packets B to A",            "Bytes B to A", "Rel Start", "Duration", "Bits/s A to B", "Bits/s B to A"]

correlation_matrix = data[features].corr(method="pearson")

fig = plt.figure(dpi=300)
#fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)
cax = ax.matshow(correlation_matrix, cmap='coolwarm')
fig.colorbar(cax)
ticks = np.arange(0, 14, 1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(("S", "Port A", "Port B", "Packets", "Bytes", "Packets A to B", "Bytes A to B", "Packets B to A","Bytes B to A", "Rel Start", "Duration", "Bits/s A to B", "Bits/s B to A", "13"))
ax.set_yticklabels(("S", "Port A", "Port B", "Packets", "Bytes", "Packets A to B", "Bytes A to B", "Packets B to A", "Bytes B to A", "Rel Start", "Duration", "Bits/s A to B", "Bits/s B to A","13"))
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
