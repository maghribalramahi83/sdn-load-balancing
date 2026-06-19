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
Random Forest Classifier - RFC
ML-QTLB: Hybrid Machine Learning and Queueing-Theory Load Balancing
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (confusion_matrix, precision_score,
                             recall_score, f1_score, accuracy_score)
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

plt.style.use('classic')

# ══════════════════════════════════════════════
# 1. Load Dataset
# ══════════════════════════════════════════════
dataset = pd.read_csv('Fuzzy CMeans  - K=2.csv')
dataset = pd.read_csv('Fuzzy CMeans  - K=2.csv')

# ── Fix: Remove rows with NaN values ──
print(f"Dataset shape before cleaning: {dataset.shape}")
print(f"NaN values per column:\n{dataset.isnull().sum()}")

dataset = dataset.dropna()  # حذف الصفوف التي تحتوي NaN

print(f"Dataset shape after cleaning: {dataset.shape}")

X = dataset.iloc[:, :-1].values   # 8 features
y = dataset.iloc[:, -1].values    # FCM cluster label
# Dataset: 25,000 records × 8 features + 1 label column
# Features: Packets, Bytes, Pkts A→B, Bytes A→B,
#           Pkts B→A, Bytes B→A, Bits/s A→B, Bits/s B→A
# Label: FCM Cluster (1=Low-priority, 2=High-priority)

X = dataset.iloc[:, :-1].values   # 8 features
y = dataset.iloc[:, -1].values    # FCM cluster label

# ══════════════════════════════════════════════
# 2. Dataset Splitting
# Train=38%, Validation=38%, Test=24%
# ══════════════════════════════════════════════
X_train_val, X_test, y_train_val, y_test = train_test_split(
    X, y,
    test_size=0.24,       # Test = 24%
    random_state=42)

val_size = 0.50           # 50% of remaining = 38% of total
X_train, X_val, y_train, y_val = train_test_split(
    X_train_val, y_train_val,
    test_size=val_size,
    random_state=42)

print(f"Training   samples: {len(X_train)}  ({len(X_train)/len(X)*100:.0f}%)")
print(f"Validation samples: {len(X_val)}    ({len(X_val)/len(X)*100:.0f}%)")
print(f"Test       samples: {len(X_test)}   ({len(X_test)/len(X)*100:.0f}%)")

# ══════════════════════════════════════════════
# 3. Random Forest Classifier
#    Hyperparameters (ML-QTLB settings)
# ══════════════════════════════════════════════
clf = RandomForestClassifier(
    criterion        = 'entropy',   # Information Gain
    n_estimators     = 80,          # Number of trees
    max_depth        = 4,           # Tree depth
    min_samples_split= 7,           # Min samples to split
    random_state     = 0            # Reproducibility
)
clf.fit(X_train, y_train)

# ══════════════════════════════════════════════
# 4. Predictions
# ══════════════════════════════════════════════
y_pred = clf.predict(X_test)

# ══════════════════════════════════════════════
# 5. Evaluation Metrics
# ══════════════════════════════════════════════
cm        = confusion_matrix(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall    = recall_score(y_test, y_pred, average='weighted')
f1        = f1_score(y_test, y_pred, average='weighted')
accuracy  = accuracy_score(y_test, y_pred)

train_acc = clf.score(X_train, y_train)
val_acc   = clf.score(X_val,   y_val)
test_acc  = clf.score(X_test,  y_test)

print('\n══════ ML-QTLB - RFC Results ══════')
print(f'Confusion Matrix:\n{cm}')
print(f'Precision : {precision * 100:.2f} %')
print(f'Recall    : {recall    * 100:.2f} %')
print(f'F1 Score  : {f1        * 100:.2f} %')
print(f'Accuracy  : {accuracy  * 100:.2f} %')
print('────────────────────────────────────')
print(f'Training   Accuracy: {train_acc * 100:.2f} %')
print(f'Validation Accuracy: {val_acc   * 100:.2f} %')
print(f'Test       Accuracy: {test_acc  * 100:.2f} %')

# ══════════════════════════════════════════════
# 6. Overfitting / Underfitting Check
# ══════════════════════════════════════════════
print('\n── Model Performance Check ──')
if val_acc > train_acc and val_acc > test_acc:
    print("Model is Underfitting")
elif abs(train_acc - val_acc) < 0.05 and abs(train_acc - test_acc) < 0.05:
    print("Model is Performing Normally (Good Fit)")
elif train_acc > val_acc and train_acc > test_acc:
    print("Model is Overfitting")
else:
    print("Model Performance is Acceptable")

# ══════════════════════════════════════════════
# 7. Confusion Matrix Plot
# ══════════════════════════════════════════════
fig, ax = plt.subplots(dpi=300)
sns.heatmap(cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=['Low-Priority (C1)', 'High-Priority (C2)'],
            yticklabels=['Low-Priority (C1)', 'High-Priority (C2)'],
            ax=ax)
ax.set_title('Confusion Matrix – Random Forest Classifier (ML-QTLB)',
             fontsize=11, fontweight='bold')
ax.set_xlabel('Predicted Label', fontsize=10, fontweight='bold')
ax.set_ylabel('True Label',      fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('Confusion_Matrix_RFC_MLQTLB.png', dpi=300)
plt.show()

# ══════════════════════════════════════════════
# 8. Evaluation Metrics Bar Chart
# ══════════════════════════════════════════════
values = [precision, recall, f1, accuracy]
labels = ['Precision', 'Recall', 'F1 Score', 'Accuracy']
colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0']

fig, ax = plt.subplots(dpi=300)
bars = ax.bar(labels, values, color=colors, width=0.35)

ax.set_ylim([0, 1.15])
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
ax.set_title('Evaluation Metrics – Random Forest Classifier (ML-QTLB)',
             fontsize=11, fontweight='bold')
ax.set_xlabel('Metric', fontsize=10, fontweight='bold')
ax.set_ylabel('Value (%)', fontsize=10, fontweight='bold')
ax.tick_params(axis='both', labelsize=10)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2,
            height + 0.01,
            f'{height*100:.2f}%',
            ha='center', va='bottom',
            fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('Metrics_RFC_MLQTLB.png', dpi=300)
plt.show()

# ================================================================
# Save Trained RF Model
# Copyright (c) 2026 Maghrib Abidalreda Maky Alrammahi
# ================================================================
import joblib

# Save the trained Random Forest model to a .pkl file
joblib.dump(clf, 'rf_model.pkl')
print("Trained RF model saved successfully as: rf_model.pkl")
print(f"Model parameters: {clf.get_params()}")