import pandas as pd
data = pd.Series([80, 85, 78, 90, 88], index = ['B1','B2','B3','B4','B5'])
print(data)
print("Average pass rate is:", data.mean())
print("Highest pass rate is:", data.max())
print("Pass rate of last is:", data.iloc[4])
print("Pass rate of B3 is:", data.loc['B3'])
print("Pass rate differences from average:\n", data - data.mean())