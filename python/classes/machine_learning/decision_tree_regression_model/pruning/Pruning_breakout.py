# Breakout: Selecting Best ccp_alpha

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Dataset
data = {
    'Age': [22,25,28,30,35,40,45,50,55,60],
    'Income': [20,25,30,35,50,60,70,80,90,100],
    'Buy': [0,0,0,1,1,1,1,1,1,1]
}

df = pd.DataFrame(data)

X = df[['Age','Income']]
y = df['Buy']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# Get pruning path
model = DecisionTreeClassifier(random_state=42)
path = model.cost_complexity_pruning_path(X_train, y_train)

alphas = path.ccp_alphas

for alpha in alphas:
    clf = DecisionTreeClassifier(ccp_alpha=alpha, random_state=42)
    clf.fit(X_train, y_train)
    acc = accuracy_score(y_test, clf.predict(X_test))
    print("Alpha:", round(alpha,4), "Accuracy:", round(acc,3))
