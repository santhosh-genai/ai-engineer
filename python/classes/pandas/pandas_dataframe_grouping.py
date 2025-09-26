import numpy as np
import pandas as pd

data = {'TestCase': ['TC1', 'TC2', 'TC3', 'TC4', 'TC5', 'TC6'],
        'Module': ['Login', 'Login', 'Payment', 'Payment', 'Reports', 'Reports'],
        'Status': ['Pass', 'Fail', 'Pass', 'Pass', 'Fail', 'Pass'],
        'ExecutionTime': [10, 15, 20, 25, 30, 35]}
df = pd.DataFrame(data)

print("Original DataFrame:")
print(df)
groupstatusdf = df.groupby('Status')['TestCase'].count()
print("\nGrouped DataFrame (Count of Test Cases):")
print(groupstatusdf)

groupmoduledf = df.groupby('Module')['ExecutionTime'].mean()
print("\nGrouped DataFrame (Mean Execution Time by Module):")
print(groupmoduledf)