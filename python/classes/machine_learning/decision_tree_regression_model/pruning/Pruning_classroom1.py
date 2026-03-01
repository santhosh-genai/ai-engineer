# Program 1: Pre-Pruning Example

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Small dataset
data = {
    'Score': [40,45,50,55,60,65,70,75,80,85],
    'Pass': [0,0,0,0,1,1,1,1,1,1]
}

df = pd.DataFrame(data)

X = df[['Score']]
y = df['Pass']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# Deep Tree (No pruning)
deep_tree = DecisionTreeClassifier(random_state=42)
deep_tree.fit(X_train, y_train)

# Pruned Tree
pruned_tree = DecisionTreeClassifier(max_depth=2, random_state=42)
pruned_tree.fit(X_train, y_train)

print("Deep Tree Accuracy:", accuracy_score(y_test, deep_tree.predict(X_test)))
print("Pruned Tree Accuracy:", accuracy_score(y_test, pruned_tree.predict(X_test)))
