'''
Program 1 — SVM Classification
Use Case: Release Risk Prediction
Predict whether a software release is risky.

Features:
   - Test Coverage
   - Open Defects
   - Automation Coverage

Target:
   - Risk (0 = Safe, 1 = Risky)
'''

import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Step 1: Dataset
data = {
    'Test_Coverage':[90,85,70,60,95,50,80,65],
    'Open_Defects':[2,4,10,15,1,18,5,12],
    'Automation':[80,75,60,50,90,40,70,55],
    'Risk':[0,0,1,1,0,1,0,1]
}

df = pd.DataFrame(data)

X = df[['Test_Coverage','Open_Defects','Automation']]
y = df['Risk']

# Step 2: Train-test split
X_train,X_test,y_train,y_test = train_test_split(
    X,y,test_size=0.25,random_state=42
)

# Step 3: Train SVM classifier
model = SVC(kernel='linear')

model.fit(X_train,y_train)

# Step 4: Prediction
pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test,pred))