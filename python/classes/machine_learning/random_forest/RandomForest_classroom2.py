# Program 2: Simple Random Forest Regression

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Small dataset
data = {
    'Area': [1000,1500,1800,2400,3000,3500],
    'Bedrooms': [2,3,3,4,5,5],
    'Price': [50,75,85,120,150,180]
}

df = pd.DataFrame(data)

X = df[['Area','Bedrooms']]
y = df['Price']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# Model
model = RandomForestRegressor(n_estimators=20, random_state=42)
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

print("MSE:", mean_squared_error(y_test, y_pred))
