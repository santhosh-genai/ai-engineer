import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('c:/Users/2276038/Desktop/Learning/python/classes/pandas/data.csv')
print(df)
fig, axes = plt.subplots(2, 2, figsize=(12, 6))  # 2 rows, 2 columns
fig.set_facecolor('lightgrey')


df.plot.bar(x='Day', y=['Week1', 'Week2', 'Week3', 'Week4'], color=['lightblue', 'lightgreen', 'lightyellow', 'lightcoral'], edgecolor='black', ax=axes[0, 0])
axes[0, 0].set_title('Test Execution Over Days')
axes[0, 0].set_xlabel('Days')
axes[0, 0].set_ylabel('Number of Test Cases')
axes[0, 0].legend(title='Test Status', loc='upper left', bbox_to_anchor=(1.05, 1))

df.plot.line(x='Day', y=['Week1', 'Week2', 'Week3', 'Week4'], color=['lightblue', 'lightgreen', 'lightyellow', 'lightcoral'], marker='o', ax=axes[0, 1])
axes[0, 1].set_title('Test Execution Trend Over Days')
axes[0, 1].set_xlabel('Days')
axes[0, 1].set_ylabel('Number of Test Cases')
axes[0, 1].legend(title='Test Status', loc='upper left', bbox_to_anchor=(1.05, 1))
plt.grid(True)

df.plot.hist(y=['Week1', 'Week2', 'Week3', 'Week4'], bins=5, alpha=0.7, edgecolor='black', ax=axes[1, 0])
axes[1, 0].set_title('Distribution of Test Executions')
axes[1, 0].set_xlabel('Number of Test Cases')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].legend(title='Weekly Frequency', loc='upper left', bbox_to_anchor=(1.05, 1))

plt.tight_layout()

plt.show()