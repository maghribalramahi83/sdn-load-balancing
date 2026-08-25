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

# ضبط الخط العام ليكون Times New Roman في كل الشكل
mpl.rcParams["font.family"] = "Times New Roman"
mpl.rcParams["font.size"] = 10

file_path = (
    r"D:\My papers\Paper 8 - SVMMLQLC - 29-5-2026 Sent to Journal Européen des Systèmes الفرنسيه"
    r"\Github\My Dataset - Cleaning Data.xlsx"
)

output_path = (
    r"D:\My papers\Paper 8 - SVMMLQLC - 29-5-2026 Sent to Journal Européen des Systèmes الفرنسيه"
    r"\Github\Pearson Correlation Heatmap TNR10pt 300dpi.png"
)

data = pd.read_excel(file_path)

numeric_features = [
    "Port A", "Port B", "Packets", "Bytes",
    "Packets A to B", "Bytes A to B", "Packets B to A", "Bytes B to A",
    "Rel Start", "Duration", "Bits/s A to B", "Bits/s B to A"
]

correlation_matrix = data[numeric_features].corr(method="pearson")

# عرض 6.5 بوصة = عرض عمود المجلة عند 300 DPI
fig, ax = plt.subplots(figsize=(6.5, 6.5), dpi=300)

image = ax.matshow(
    correlation_matrix,
    cmap="coolwarm",
    vmin=-1,
    vmax=1
)

colorbar = fig.colorbar(
    image,
    ax=ax,
    orientation="horizontal",
    pad=0.12,
    fraction=0.05
)

# العنوان فقط Bold، باقي الـticks عادي
colorbar.set_label(
    "Pearson correlation coefficient",
    fontsize=10,
    fontweight="bold",
    fontfamily="Times New Roman",
    labelpad=8
)
colorbar.ax.tick_params(labelsize=10)
for label in colorbar.ax.get_xticklabels():
    label.set_fontfamily("Times New Roman")

ax.set_xticks(np.arange(len(numeric_features)))
ax.set_yticks(np.arange(len(numeric_features)))

# تسميات الصف/العمود: Regular (بدون bold)
ax.set_xticklabels(
    numeric_features,
    rotation=90,
    fontsize=10,
    fontfamily="Times New Roman"
)
ax.set_yticklabels(
    numeric_features,
    fontsize=10,
    fontfamily="Times New Roman"
)

# عناوين المحاور فقط Bold
ax.set_xlabel(
    "Numerical flow-level features",
    fontsize=10,
    fontweight="bold",
    fontfamily="Times New Roman",
    labelpad=12
)
ax.set_ylabel(
    "Numerical flow-level features",
    fontsize=10,
    fontweight="bold",
    fontfamily="Times New Roman",
    labelpad=12
)

plt.tight_layout()
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.show()