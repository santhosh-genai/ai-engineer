'''Program 2 — SVM Regression
Use Case: Predict Defect Resolution Time

Predict how many days it takes to resolve a defect.

Features:
   - Severity
   - Complexity
   - Developer Experience
Target:
   - Resolution Days'''

import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Step 1: Dataset
data = {
    'Severity':[1,2,3,4,5,2,3,4],
    'Complexity':[2,4,6,8,9,5,7,8],
    'Dev_Experience':[8,6,5,3,2,7,4,3],
    'Fix_Days':[1,2,4,6,8,3,5,7]
}

df = pd.DataFrame(data)

X = df[['Severity','Complexity','Dev_Experience']]
y = df['Fix_Days']

# Step 2: Train-test split
X_train,X_test,y_train,y_test = train_test_split(
    X,y,test_size=0.25,random_state=42
)

# Step 3: Train SVM Regressor
model = SVR(kernel='linear')

model.fit(X_train,y_train)

# Step 4: Prediction
pred = model.predict(X_test)

print("MSE:", mean_squared_error(y_test,pred))