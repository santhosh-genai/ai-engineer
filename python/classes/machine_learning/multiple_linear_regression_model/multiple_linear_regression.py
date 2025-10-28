import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

data_dict = {
    'X1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'X2': [5, 7, 9, 11, 13, 15, 17, 19, 21, 23],
    'Y': [7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
}
data = pd.DataFrame(data_dict)
X=data[['X1', 'X2']]  # Input features - Independent variables (input)
Y=data['Y']          # Target variable - Dependent variable (output)

# Split the dataset into training and testing sets 
# 80% training data and 20% testing data
# X_train: training data for X1 and X2
# X_test: testing data for X1 and X2
# Y_train: training data for Y
# Y_test: testing data for Y
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)   

model = LinearRegression()
model.fit(X_train, Y_train)

print("intercept: B0", model.intercept_)
print("coefficients: B1, B2", model.coef_)

Y_pred = model.predict(X_test)
print("Predicted values:", Y_pred)
print("Actual values:", Y_test.values)
print("MSE:", mean_squared_error(Y_test, Y_pred))
print("RMSE:", np.sqrt(mean_squared_error(Y_test, Y_pred)))
print("R2:", r2_score(Y_test, Y_pred))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(X_test['X1'], X_test['X2'], Y_test, color='blue', label='Actual Values')
x1_range = np.linspace(X['X1'].min(), X['X1'].max(), 10)
x2_range = np.linspace(X['X2'].min(), X['X2'].max(), 10)
x1_range, x2_range = np.meshgrid(x1_range, x2_range)
# Predict Y values for the grid to create the regression plane 
# reshape to match the grid shape
y_range = model.predict(np.c_[x1_range.ravel(), x2_range.ravel()]).reshape(x1_range.shape)
ax.plot_surface(x1_range, x2_range, y_range, color='red', alpha=0.5, label='Regression Plane')

ax.set_xlabel('X1')
ax.set_ylabel('X2')
ax.set_zlabel('Y')
ax.set_title('Multiple Linear Regression: Actual vs Predicted Values')
ax.legend()
plt.show()