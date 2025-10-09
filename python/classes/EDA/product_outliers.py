import pandas as pd

data = pd.read_csv('c:/Users/2276038/Desktop/Learning/python/classes/EDA/SalesDatasetIQR.csv')

data.columns = ['','Date', 'Gender', 'Age', 'Product Category', 'Quantity', 'Price per Unit', 'Total Amount']

Q1 = data['Total Amount'].quantile(0.25)
Q3 = data['Total Amount'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = data[(data['Total Amount'] < lower_bound) | (data['Total Amount'] > upper_bound)]
print("Outliers in Total Amount:")
print(outliers)

outliers.to_csv('c:/Users/2276038/Desktop/Learning/python/classes/EDA/Outliers.csv', index=False)

data.drop(outliers.index, inplace=True)

data.to_csv('c:/Users/2276038/Desktop/Learning/python/classes/EDA/Cleaned_SalesDataset.csv', index=False)

