import pandas as pd
import numpy as np

data = {'DefectID': ['D1', 'D2', 'D3', 'D4', 'D5'],
        'Module': ['Login', 'Login', 'Payment', 'Reports', 'Reports'],
        'Severity': ['High', 'Low', 'Medium', 'High', 'Low'],
        'Status': ['Open', 'Closed', 'Open', 'Closed', 'Open']}

df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)
print("\nDataFrame with open Defects:")
print(df[df['Status']=='Open'])
print("\nDataFrame with High Severity Defects:")
print(df[df['Severity']=='High'])
print("\nCount of Defects by Status:")
print(df.groupby('Status')['DefectID'].count())
