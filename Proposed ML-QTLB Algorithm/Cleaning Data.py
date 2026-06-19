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

# Load the data into a Pandas DataFrame
df = pd.read_csv("E:\\wireshark statistical dataset.csv")

# Check for missing values
missing_values = df.isnull().sum()
print("Missing values:")
print(missing_values)

# Handle missing values
# Method 1: Drop missing values
#df = df.dropna()

# Method 2: Fill missing values with the mean of the column
df = df.fillna(df.mean())

# Method 3: Fill missing values with the median of the column
#df = df.fillna(df.median())

# Method 4: Fill missing values with a constant value
#df = df.fillna(0)

# Check for duplicates
duplicates = df.duplicated().sum()
print("Duplicates:")
print(duplicates)

# Handle duplicates
df = df.drop_duplicates()

# Save the cleaned data
df.to_csv("cleaned_data.csv", index=False)