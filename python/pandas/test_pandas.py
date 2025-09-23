import pandas as pd
data = { 'Name': ['Alice','Bob','Charlie'], 'Age':[25,30,35] }
s = pd.Series([1,2,3,4,5], index=['a','b','c','d','e'])
df = pd.DataFrame(data)
print('✅ pandas is working!')
# print(df)
print(s['a'])