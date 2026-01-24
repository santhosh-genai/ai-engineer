import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# ============================================================================
# MODEL INTERPRETATION: LOGISTIC REGRESSION FOR PURCHASE PREDICTION
# ============================================================================
# 
# Question 1: Why is Logistic Regression suitable for this problem?
# ────────────────────────────────────────────────────────────────────────
# Logistic Regression is ideal for binary classification (Purchased: Yes/No) because:
#
#   a) Binary Output: The target variable (Purchased) has exactly 2 classes (0=Not Purchased, 1=Purchased)
#      Logistic Regression outputs probabilities (0-1) that map naturally to binary outcomes.
#
#   b) Interpretability: Unlike black-box models, logistic regression provides interpretable
#      coefficients showing how Age and Salary influence purchase probability.
#      Example: If coef[Age]=0.05, each additional year increases log-odds of purchase by 0.05.
#
#   c) Probability Estimates: LogisticRegression.predict_proba() gives confidence scores.
#      This allows setting custom decision thresholds (e.g., predict "Purchased" only if P > 0.7)
#      useful for balancing precision/recall trade-offs.
#
#   d) Computational Efficiency: Fast to train and predict, suitable for real-time inference.
#
#   e) Class Imbalance Handling: class_weight='balanced' automatically adjusts for unequal class sizes,
#      preventing the model from biasing toward the majority class.
#
# ============================================================================
# 
# Question 2: What does Precision indicate in a business context?
# ────────────────────────────────────────────────────────────────────────
# Precision = TP / (TP + FP)
# "Of all customers we predicted as 'Will Purchase', how many actually purchased?"
#
# Business Interpretation:
#   - HIGH Precision (e.g., 0.85): When we predict "Purchase", we're correct 85% of the time.
#     → Cost of False Positives is HIGH (e.g., wasteful targeted marketing to non-buyers)
#     → Minimize: Wrong predictions consume marketing budget with no ROI
#
#   - Use Case: Email campaigns, paid advertising, personalized offers
#     → Target only high-confidence leads to reduce wasted ad spend
#
#   - Example: If precision=0.9 and we send 100 targeted emails, ~90 convert and ~10 don't.
#     → Precision prevents wasting marketing resources on unlikely buyers.
#
# ============================================================================
#
# Question 3: What does Recall indicate in a business context?
# ────────────────────────────────────────────────────────────────────────
# Recall = TP / (TP + FN)
# "Of all customers who actually purchased, how many did we correctly identify?"
#
# Business Interpretation:
#   - HIGH Recall (e.g., 0.90): We capture 90% of all potential buyers.
#     → Cost of False Negatives is HIGH (e.g., missed sales opportunities)
#     → Minimize: Overlooking a buyer is lost revenue
#
#   - Use Case: Lead identification, customer retention, fraud detection
#     → Catch as many potential buyers as possible, even if some predictions are wrong
#
#   - Example: If recall=0.92 and there are 1000 actual buyers, we identify ~920 of them.
#     → Low recall means leaving 80 potential customers unseen = missed opportunities.
#
# ============================================================================
#
# Question 4: If Precision is high but Recall is low, what does it mean?
# ────────────────────────────────────────────────────────────────────────
# Example: Precision=0.95, Recall=0.40
#
# Interpretation:
#   - HIGH Precision (0.95): When we predict "Purchase", almost always correct (95% of the time)
#   - LOW Recall (0.40): We only find 40% of actual buyers (miss 60%)
#
# What This Means:
#   → Model is VERY CONSERVATIVE: Only predicts "Purchase" for high-confidence cases
#   → We make few predictions, but predictions are highly reliable
#   → Confusion Matrix: Low TP, High TN, Low FP, High FN
#
# Business Impact:
#   - ✓ Advantages: 
#       • No wasted marketing budget (almost everyone we target buys)
#       • High efficiency, cost-effective campaigns
#   
#   - ✗ Disadvantages:
#       • Miss 60% of potential buyers = significant lost revenue
#       • Competitor targets the ignored customers
#       • Underutilized marketing capacity
#
# When This Trade-Off Matters:
#   ✓ Use HIGH Precision, LOW Recall when:
#       - Marketing budget is VERY LIMITED
#       - Each wrong prediction is extremely costly
#       - Example: Luxury product targeting (high-value, low-volume sales)
#
#   ✗ Avoid when:
#       - Revenue opportunity is primary (need to maximize customer reach)
#       - Budget can sustain some false positives
#       - Example: Free trial signups, mass market campaigns
#
# How to Improve:
#   - Lower prediction threshold (default=0.5 → try 0.3)
#   - Retrain with class weights adjusted
#   - Add more/better features (e.g., purchase history, browsing behavior)
#   - Use F1 Score (harmonic mean of precision & recall) to balance both
#
# ============================================================================


df = pd.read_csv('C:\\Users\\2276038\\Desktop\\learning\\ai-engineer\\python\\assignments\\Assignment_week22\\Social_Network_Ads.csv')
print("Dataset loaded successfully.")

# o First few rows
# o Dataset shape
# o Summary statistics

print(df.head())
print(df.shape)
print(df.describe())


#missing values
print("Missing values in each column:\n", df.isnull().sum())

X = df[['Age', 'EstimatedSalary']]
y = df['Purchased']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(class_weight='balanced')
model.fit(x_train, y_train)

# Class labels for test data
# Probabilities for test data

y_pred = model.predict(x_test)
y_prob = model.predict_proba(x_test)[:, 1]
print("Predicted class labels for test data:", y_pred)
print("Predicted probabilities for test data:", y_prob)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred, zero_division=0)
print("Accuracy:", accuracy)
print("Precision:", precision)  
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:\n", conf_matrix)
print("Classification Report:\n", class_report)

#  True Positives
#  True Negatives
#  False Positives
#  False Negatives
print("True Positives (TP):", conf_matrix[1, 1])
print("True Negatives (TN):", conf_matrix[0, 0])    
print("False Positives (FP):", conf_matrix[0, 1])
print("False Negatives (FN):", conf_matrix[1, 0])


# visualization - Plot the Confusion Matrix using Matplotlib
plt.figure(figsize=(6, 4))
plt.matshow(conf_matrix, cmap=plt.cm.Blues, fignum=1)
plt.title('Confusion Matrix', pad=20)
plt.colorbar()
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.xticks([0, 1], ['Not Purchased', 'Purchased'])
plt.yticks([0, 1], ['Not Purchased', 'Purchased'])
for (i, j), value in np.ndenumerate(conf_matrix):
    plt.text(j, i, value, ha='center', va='center', color='red')
plt.show()

try:
    age_input = float(input("Enter Age: "))
    salary_input = float(input("Enter Estimated Salary: "))
    x_input = np.array([[age_input, salary_input]])
    new_data = pd.DataFrame(x_input, columns=['Age', 'EstimatedSalary'])
    predicted_class = model.predict(new_data)[0]
    predicted_prob = model.predict_proba(new_data)[0][1]
    print(f"Predicted Purchase Decision for Age {age_input} and Estimated Salary {salary_input}: {predicted_class} (Probability of Purchase: {predicted_prob:.2f})")
except Exception as e:
    print("Prediction error:", e)