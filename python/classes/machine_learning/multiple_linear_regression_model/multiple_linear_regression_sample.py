import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

data_dict = {
     'x1': [1, 2, 3],
    'x2': [2, 1, 4],
    'Output': [6, 8, 14]
}
data = pd.DataFrame(data_dict)
x = data[['x1', 'x2']]  # Input features - Independent variables (input)
y = data['Output']      # Target variable - Dependent variable (output)

x_train = x
x_test = x
y_train = y 
y_test = y

model = LinearRegression()
model.fit(x_train, y_train)
print("intercept B0:", model.intercept_)
print("coefficients B1, B2:", model.coef_)
print("Model equation: y = B0 + B1*x1 + B2*x2", f"= {model.intercept_} + {model.coef_[0]}*x1 + {model.coef_[1]}*x2")

y_pred = model.predict(x_test)
print("Predicted values:", y_pred)
print("Actual values:", y_test.values)
print("MSE:", mean_squared_error(y_test, y_pred))
print("R2:", r2_score(y_test, y_pred))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x_test['x1'], x_test['x2'], y_test, color='blue', label='Actual Values')
x1_range = np.linspace(x['x1'].min(), x['x1'].max(), 10)
x2_range = np.linspace(x['x2'].min(), x['x2'].max(), 10)

x1_range, x2_range = np.meshgrid(x1_range, x2_range)

y_range = model.predict(np.c_[x1_range.ravel(), x2_range.ravel()]).reshape(x1_range.shape)
ax.plot_surface(x1_range, x2_range, y_range, color='red', alpha=0.5, label='Regression Plane')  
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('Output')
ax.set_title('Multiple Linear Regression: Actual vs Predicted Values')
ax.legend()
plt.show()