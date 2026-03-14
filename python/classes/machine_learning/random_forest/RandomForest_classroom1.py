# Program 1: Simple Random Forest Classification
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Small dataset
data = {
    'Hours_Studied': [1,2,3,4,5,6,7,8],
    'Pass': [0,0,0,1,1,1,1,1]
}

df = pd.DataFrame(data)

X = df[['Hours_Studied']]
y = df['Pass']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

# Random Forest Model
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
