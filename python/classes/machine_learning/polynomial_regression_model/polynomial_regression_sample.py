import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

x = np.array([-3, -2, -1, 0, 1, 2, 3]).reshape(-1, 1)
y = np.array([-20, -8, -2, 0, 2, 8, 20])

poly_features = PolynomialFeatures(degree=3)
x_poly = poly_features.fit_transform(x)

model = LinearRegression()
model.fit(x_poly, y)

y_pred = model.predict(x_poly)

print("Predicted values:", y_pred)
print("Actual values:", y)

plt.scatter(x, y, color='blue', label='Actual Values')
plt.scatter(x, y_pred, color='red', label='Predicted Values')
plt.plot(x, y_pred, color='green', label='Polynomial Regression Line')
plt.xlabel('Input Feature (x)') 
plt.ylabel('Target Variable (y)')
plt.title('Polynomial Regression: Actual vs Predicted Values')
plt.legend()
plt.show()