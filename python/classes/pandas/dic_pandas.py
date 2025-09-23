import pandas as pd
testcases = {'Alice': 500, 'Bob': 200, 'Charlie': 300}
exe = pd.Series(testcases)
print(exe)
total = exe.sum()
print(f"Total number of testcases is: {total}")
print(exe.loc['Bob':'Charlie'])
