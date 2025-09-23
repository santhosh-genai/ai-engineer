import pandas as pd
data = pd.Series([5, 8, 3, 6, 10, 2, 7], index = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
print(data)
print("Maximum defect count is:", data.max())
print("Minimum defect count is:", data.min())
print("Defect count on Thu:", data.iloc[4])
print("Defect count on Wed:", data.loc['Wed'])
print("Total defects in the week:", data.sum())