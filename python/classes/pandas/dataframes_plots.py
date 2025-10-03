import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = {'Module':['AI', 'ML', 'Python', 'DataStructures'], 'Teamsize':[135, 125, 125, 115] }
df = pd.DataFrame(data)
print(df)

df.plot.pie(y='Teamsize', labels=df['Module'], autopct=lambda x: int(x * sum(df['Teamsize']) / 100), startangle=90, figsize=(10, 6), title='Module-wise Team Size Distribution')
plt.legend(title='Modules', loc='upper right', bbox_to_anchor=(1.4, 1.1))
plt.show()
