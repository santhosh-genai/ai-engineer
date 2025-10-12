import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Readme:
# This script demonstrates a simple linear regression model to predict employee salaries based on years of experience.
# train → fit → predict → evaluate

data = pd.read_csv('c:/Users/2276038/Desktop/Learning/python/classes/machine_learning/linear_regression_model/salary.csv')
x = data[['YearsExperience']] # Input feature - Independent variable (input)
y = data['Salary'] # Target variable - Dependent variable (output)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=20)

print("x_train:\n", x_train) # Training data (80% of the dataset - Experience))
print("x_test:\n", x_test) # Testing data (20% of the dataset - Experience)
print("y_train:\n", y_train) # Training data (80% of the dataset - Salary)
print("y_test:\n", y_test) # Testing data (20% of the dataset - Salary)

 # Create a linear regression model
model = LinearRegression()

# Finds the best-fitting line
    # Salary=a+b×YearsExperience - linear equation of a line
    # a = intercept (starting salary when experience = 0) - 25751.16
    # b = slope (how much salary increases per year of experience) - 10088.34
model.fit(x_train, y_train) 


#Output the model parameters -
    # slope: [10088.3449763] - every 1 extra year of experience, the model predicts an increase of ₹10,088.34 in salary
    # intercept: 25751.163017632447 - For 0 years of experience, the model predicts salary ₹25,751.16.
print("Model coefficients (slope):", model.coef_)
print("Model intercept:", model.intercept_)


# Trained model uses the learned relationship to predict salaries for the unseen test data (x_test Experience)
    # x_test: years of experience for which we want to predict salaries [5.1, 2.2, 1.3, 4.0, 10.5, 4.9]
    # Predicted values: [58033.86694179 , 77201.72239675 , 63078.03942994 , 113519.76431143 , 36848.34249156 , 71148.71541097]
y_pred = model.predict(x_test)
print("x_test:\n", x_test)
print("Predicted values:\n", y_pred)

# Evaluate the model
print("MSE:", mean_squared_error(y_test, y_pred))
print("R2:", r2_score(y_test, y_pred))


plt.scatter(x['YearsExperience'], y, color='blue', label='Actual Data')
plt.plot(x_test, y_pred, color='red', label='Predicted Data', linewidth=2, marker='o')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.title('Actual vs Predicted Salary')
plt.legend()
plt.show()