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

df.to_csv('defects.csv', index=False)
print("\nDataFrame saved to 'defects.csv'")

new_data = {'DefectID': ['D6', 'D7'],
            'Module': ['Login', 'Payment'],
            'Severity': ['Low', 'High'],
            'Status': ['Open', 'Closed']}
df2 = pd.DataFrame(new_data)
df2.to_csv('defects.csv', mode='a', index=True, header=False)
print(df2)
print("\nNew DataFrame saved to 'defects.csv'")

df1 = pd.read_csv('defects.csv')
print("\nDataFrame read from 'defects.csv':")
print(df1)