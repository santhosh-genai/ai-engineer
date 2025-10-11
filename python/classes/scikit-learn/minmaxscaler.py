from sklearn.preprocessing import MinMaxScaler
import numpy as np

data = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])

scaler = MinMaxScaler()
trained_scaler = scaler.fit_transform(data)

print("Original Data:\n", data)
print("Scaled Data:\n", trained_scaler)
