import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load environment variables
load_dotenv()

CLEANED_CSV = os.getenv('CLEANED_DATASET_PATH')
SCALED_CSV = os.getenv('SCALED_DATASET_PATH')

RANDOM_STATE = 42
TEST_SIZE = 0.2

FEATURE_COLUMNS = [
    'Module_Complexity_Score',
    'Test_Case_Count',
    'Automation_Coverage',
    'Code_Churn',
    'Defects_Previous_Cycle',
    'Execution_Time_Previous'
]

TARGET_TIME = 'Estimated_Execution_Time'
TARGET_DEFECTS = 'Expected_Defect_Count'

df = pd.read_csv(SCALED_CSV)
df_raw = pd.read_csv(CLEANED_CSV)

X = df[FEATURE_COLUMNS].values
y_time = df_raw[TARGET_TIME].values
y_defects = df_raw[TARGET_DEFECTS].values

X_train, X_test, y_train_time, y_test_time = train_test_split(X, y_time, test_size=TEST_SIZE, random_state=RANDOM_STATE)
X_train, X_test, y_train_defects, y_test_defects = train_test_split(X, y_defects, test_size=TEST_SIZE, random_state=RANDOM_STATE)   

time_model = LinearRegression()
time_model.fit(X_train, y_train_time)

defect_model = LinearRegression()
defect_model.fit(X_train, y_train_defects)

y_pred_time = time_model.predict(X_test)
y_pred_defects = defect_model.predict(X_test)

print(X_test)
print(y_pred_time)
print(y_pred_defects)

print("Execution Time Model Coefficients:", time_model.coef_)
print("Execution Time Model Intercept:", time_model.intercept_)


print("Execution Time Model Evaluation:")
print("MSE:", mean_squared_error(y_test_time, y_pred_time))
print("R2:", r2_score(y_test_time, y_pred_time))

print("\nDefect Count Model Evaluation:")
print("MSE:", mean_squared_error(y_test_defects, y_pred_defects))
print("R2:", r2_score(y_test_defects, y_pred_defects))   

fig, axes = plt.subplots(1, 2, figsize=(12, 6)) 
fig.set_facecolor('lightgrey')
plt.suptitle('Linear Regression Model - Test Execution and Defect Count Prediction', fontsize=16)

axes[0].scatter(y_test_time, y_pred_time, color='blue', label='Execution Time Predictions')
axes[0].plot(y_test_time, y_test_time, color='red', linewidth=2, label='Ideal Prediction')
axes[0].grid()
axes[0].set_xlabel('Actual Execution Time')
axes[0].set_ylabel('Predicted Execution Time')
axes[0].set_title('Predicted Execution Time vs Actual Execution Time')
axes[0].legend()

axes[1].scatter(y_test_defects, y_pred_defects, color='blue', label='Defect Count Predictions')
axes[1].plot(y_test_defects, y_test_defects, color='red', linewidth=2, label='Ideal Prediction')
axes[1].grid()
axes[1].set_xlabel('Actual Defect Count')
axes[1].set_ylabel('Predicted Defect Count')
axes[1].set_title('Predicted Defect Count vs Actual Defect Count')
axes[1].legend()

plt.tight_layout()
plt.show()







# # Create and fit scalers with original (raw) data
# time_scaler = StandardScaler()
# defect_scaler = StandardScaler()

# time_scaler.fit(df_raw[TARGET_TIME].values.reshape(-1, 1))
# defect_scaler.fit(df_raw[TARGET_DEFECTS].values.reshape(-1, 1))

# # Transform predictions back to original scale
# original_scale_pred_time = time_scaler.inverse_transform(y_pred_time.reshape(-1, 1))
# original_scale_pred_defects = defect_scaler.inverse_transform(y_pred_defects.reshape(-1, 1))

# # Transform test data back to original scale for comparison
# original_test_time = time_scaler.inverse_transform(y_test_time.reshape(-1, 1))
# original_test_defects = defect_scaler.inverse_transform(y_test_defects.reshape(-1, 1))

# print("Predicted Execution Times (Original Scale):")
# print(original_scale_pred_time)
# print("\nActual Test Execution Times (Original Scale):")
# print(original_test_time)

# print("\nPredicted Defect Counts (Original Scale):")
# print(original_scale_pred_defects)
# print("\nActual Test Defect Counts (Original Scale):")
# print(original_test_defects)