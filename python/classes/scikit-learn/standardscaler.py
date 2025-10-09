from sklearn.preprocessing import StandardScaler
import numpy as np

data = np.array([[1, 2], [3, 4], [5, 6]])
scaler = StandardScaler()

trained_scaler = scaler.fit_transform(data)
print("Original Data:\n", data)
print("Standardized Normal Distribution Data:\n", trained_scaler)

trained_scaler1 = scaler.fit(data)
print("Trained Scaler - fit:", trained_scaler1)

trained_scaler2 = scaler.transform(data)
print("Transformed Data:\n", trained_scaler2)
