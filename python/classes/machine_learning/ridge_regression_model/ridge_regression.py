import numpy as np
from sklearn.linear_model import Ridge


# feature matrix: three samples, two features each
x = np.array([[1, 1], [1, 2], [1, 3]])
y = np.array([1, 2, 2])

model = Ridge(alpha=1.0, fit_intercept=False)
model.fit(x, y)

print("Model Coefficients:", model.coef_)

try:
    x_input = float(input("Enter an input value for x: "))
    x_arr = np.array([[1, x_input]])
    y_pred = model.predict(x_arr)
    print(f"Predicted output for input {x_input}: {y_pred}")

except ValueError:
    print("Invalid input. Please enter a numeric value.")
except Exception as e:
    print("Prediction error:", e)

