import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('C:\\Users\\2276038\\Desktop\\learning\\ai-engineer\\python\\assignments\\Assignment_week21\\sales_data.csv')
X = data[['Advertising_Spend']]  # Input feature - Independent variable (input)
Y = data['Total Amount']    # Target variable - Dependent variable (output)

print(data.describe())
plt.scatter(X, Y)
plt.title('Advertising Spend vs Total Amount (Sales)')
plt.xlabel('Advertising Spend') 
plt.ylabel('Total Amount (Sales)')
plt.title('Scatter Plot: Advertising Spend vs Total Amount (Sales)')
plt.show()

