import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

data = pd.read_csv('C:\\Users\\2276038\\Desktop\\learning\\ai-engineer\\python\\assignments\\Assignment_week21\\sales_data.csv')    
X = data[['Advertising_Spend']]  # Input feature - Independent variable (input)
Y = data['Total Amount']    # Target variable - Dependent variable (output)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, Y_train)
Y_pred = model.predict(X_test)
print("mse:", mean_squared_error(Y_test, Y_pred))
print("rmse:", np.sqrt(mean_squared_error(Y_test, Y_pred)))
print("r2:", r2_score(Y_test, Y_pred))

plt.scatter(X_test, Y_test, color='blue', label='Actual Values')
plt.scatter(X_test, Y_pred, color='red', label='Predicted Values')
plt.plot(X_test, Y_pred, color='green', label='Regression Line')
plt.xlabel('Advertising Spend')
plt.ylabel('Total Amount (Sales)')
plt.title('Simple Linear Regression: Actual vs Predicted Values')
plt.legend()
plt.show()

PolynomialFeatures = PolynomialFeatures(degree=2)
X_poly = PolynomialFeatures.fit_transform(X_train)

poly_model = LinearRegression()

poly_model.fit(X_poly, Y_train)

X_test_poly = PolynomialFeatures.fit_transform(X_test)
Y_poly_pred = poly_model.predict(X_test_poly)

print("Polynomial Regression")
print("mse:", mean_squared_error(Y_test, Y_poly_pred))
print("rmse:", np.sqrt(mean_squared_error(Y_test, Y_poly_pred)))
print("r2:", r2_score(Y_test, Y_poly_pred))
plt.scatter(X_test, Y_test, color='blue', label='Actual Values')
plt.scatter(X_test, Y_poly_pred, color='red', label='Predicted Values')
plt.plot(X_test, Y_poly_pred, color='green', label='Polynomial Regression Line')
plt.xlabel('Advertising Spend') 
plt.ylabel('Total Amount (Sales)')  
plt.title('Polynomial Regression: Actual vs Predicted Values')
plt.legend()
plt.show()