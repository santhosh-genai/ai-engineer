import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder  
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

df = pd.read_csv('C:\\Users\\2276038\\Desktop\\learning\\ai-engineer\\python\\classes\\machine_learning\\logistic_regression_model\\sales_data.csv')

# Encode the 'CardType' categorical variable
le = LabelEncoder()
df['cardType_encoded'] = le.fit_transform(df['CardType'])

# keep X as a 2-D DataFrame so sklearn receives shape (n_samples, n_features)
x = df[['Total Amount']]
y = df['cardType_encoded']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = LogisticRegression(class_weight='balanced') # using balanced class weights to handle any class imbalance

# fit expects a 1-D target array; ravel to avoid DataConversionWarning
model.fit(x_train, y_train.values.ravel())
y_pred = model.predict(x_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred, zero_division=0)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:\n", conf_matrix)
print("Classification Report:\n", class_report)

# Calculate threshold for decision boundary
threshold = -model.intercept_[0] / model.coef_[0][0] 
print("Threshold for Total Amount:", threshold)

try:
    user_input = float(input("Enter a Total Amount to predict Card Type: "))
    x_input = np.array([[user_input]])
    new_data = pd.DataFrame(x_input, columns=['Total Amount'])
    predicted_class = model.predict(new_data)[0]

    # Decode the predicted class back to original label
    predicted_label = le.inverse_transform([predicted_class])
    print(f"Predicted Card Type for Total Amount {user_input}: {predicted_label}")

except Exception as e:
    print("Prediction error:", e)