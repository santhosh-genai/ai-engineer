# Breakout: Loan Approval Prediction

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# Step 1: Create dataset
data = {
    'Income': [30,40,50,60,70,80,90,100,35,45,55,65],
    'CreditScore': [600,650,700,720,750,780,800,820,610,660,710,730],
    'Age': [25,30,35,40,45,50,55,60,28,32,38,42],
    'Approved': [0,0,1,1,1,1,1,1,0,0,1,1]
}

df = pd.DataFrame(data)

X = df[['Income','CreditScore','Age']]
y = df['Approved']

# Step 2: Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# Step 3: Decision Tree
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)
dt_pred = dt.predict(X_test)

# Step 4: Random Forest
rf = RandomForestClassifier(n_estimators=20, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)

# Step 5: Compare Accuracy
print("Decision Tree Accuracy:", accuracy_score(y_test, dt_pred))
print("Random Forest Accuracy:", accuracy_score(y_test, rf_pred))

# Step 6: Feature Importance (Random Forest)
importances = pd.Series(rf.feature_importances_, index=X.columns)
print("\nFeature Importance:\n", importances.sort_values(ascending=False))
