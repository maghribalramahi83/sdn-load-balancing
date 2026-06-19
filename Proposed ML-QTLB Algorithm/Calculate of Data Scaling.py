"""
Data Scaling
standardization (using StandardScaler) / mean of 0 and a standard deviation of 1 
normalization (using MinMaxScaler) /  minimum value of 0 and a maximum value of 1
RobustScaler / between -3 and 3
"""
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import pandas as pd

# Load the dataset
df = pd.read_csv('E:\\3.csv')

# Separate features from the target variable
X = df.iloc[:, :8] # elects all rows and only the first 8 columns (0-7).


# Initialize the scalers
scaler_std = StandardScaler()
scaler_minmax = MinMaxScaler()
scaler_robust = RobustScaler()

# Apply the StandardScaler to the data
X_std = scaler_std.fit_transform(X)

# Apply the MinMaxScaler to the data
X_minmax = scaler_minmax.fit_transform(X)

# Apply the RobustScaler to the data
X_robust = scaler_robust.fit_transform(X)
