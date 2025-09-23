import numpy as np
import pandas as pd
data = np.array([12,13,14,15,16])
s = pd.Series(data)
print(s)
print(s.iloc[2:4])
