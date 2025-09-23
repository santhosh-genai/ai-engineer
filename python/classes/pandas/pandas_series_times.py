import pandas as pd
data = pd.Series([12, 15, 20, 18, 25, 30, 22], index = ['TC1','TC2','TC3','TC4','TC5','TC6','TC7'])
print(data)
print("first three elements:\n",data.head(3))
print("Average of all test times is:", data.mean())
print("Second test time is:", data.iloc[1])
print("execution time of TC3", data.loc['TC3'])