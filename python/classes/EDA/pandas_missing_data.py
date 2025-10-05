import pandas as pd

df = pd.read_csv('c:/Users/2276038/Desktop/Learning/python/classes/EDA/test_results_missing.csv')
print('Original DataFrame:\n', df)
print('count missing values:\n', df.isnull().sum())

df['Duration'].fillna((df['Duration'].mean()), inplace=True)
df['Status'].fillna('Unknown', inplace=True)
print('\nAfter filling missing values:\n', df)

df.dropna(inplace=True)
print('\nAfter dropping rows with missing values:\n', df)   