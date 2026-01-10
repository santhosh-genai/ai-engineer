import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

X = np.array([2, 3, 2, 4, 5]).reshape(-1, 1)
Y = np.array([2, 4, 5, 4, 5])

model = LinearRegression()
model.fit(X, Y)
Y_pred = model.predict(X)
print("Predicted values:", Y_pred)
print("Model coefficients (slope):", model.coef_)
print("Model intercept:", model.intercept_)

