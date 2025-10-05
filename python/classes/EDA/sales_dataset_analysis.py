import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


data = pd.read_csv('c:/Users/2276038/Desktop/Learning/python/classes/EDA/SalesDataset.csv')

P25 = data['Total Amount'].quantile(0.25)
P50 = data['Total Amount'].quantile(0.50)
P75 = data['Total Amount'].quantile(0.75)   
print("\nPercentiles of Total Amount:")
print(f'25th Percentile: {P25}')
print(f'50th Percentile: {P50}')
print(f'75th Percentile: {P75}')
print("*************************")

ammount_var = data['Total Amount'].var()
Quantity_var = data['Quantity'].var()
print("variance of Total Amount and Quantity: ")
print(f'Variance of Total Amount: {ammount_var}')
print(f'Variance of Quantity: {Quantity_var}')
print("*************************")

cor_age_amount =data['Age'].corr(data['Total Amount'])
cor_quantity_amount =data['Quantity'].corr(data['Total Amount'])
cor_price_amount =data['Price per Unit'].corr(data['Total Amount'])
all_cor = data[['Age', 'Quantity', 'Price per Unit', 'Total Amount']].corr()

print("Correlation Data: ")
print(f'Correlation between Age and Total Amount: {cor_age_amount}')
print(f'Correlation between Quantity and Total Amount: {cor_quantity_amount}')
print(f'Correlation between Price and Total Amount: {cor_price_amount}')
print(f'\nOverall Correlation Matrix:\n{all_cor}')

print("Correlation between Series:")
data = pd.Series([20, 30, 40])
data1 = pd.Series([2000, 3000, 4000])
data2 = pd.Series([300, 200, 100])

correlation1 = data.corr(data1) 
correlation2 = data.corr(data2) 

print(correlation1)
print(correlation2)

# data = {
#     'Pulserate': [20, 90, 70, 60, np.nan],
#     'Hours': [85, 95, 75, 65, 70],
#     'Duration': [1, np.nan, 2, 3, 2],
#     'Sleep': [10, 12, np.nan, 8, 8]
# }

# Create a Series with the percentile values
# percentiles_data = pd.Series([P25, P50, P75], index=['25th Percentile', '50th Percentile', '75th Percentile'])

# plt.figure(figsize=(8, 5))
# plt.pie(percentiles_data.values, labels=percentiles_data.index, autopct='%1.1f%%', startangle=90)
# plt.title('Percentile Distribution of Total Amount')
# plt.show()
