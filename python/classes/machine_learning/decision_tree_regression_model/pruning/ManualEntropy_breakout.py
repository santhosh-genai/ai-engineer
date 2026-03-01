# Breakout: Information Gain Calculation

import pandas as pd
import numpy as np

# Dataset
data = {
    'Study': ['Low','Low','High','High','High','Low'],
    'Pass': ['No','No','Yes','Yes','Yes','Yes']
}

df = pd.DataFrame(data)

# Step 1: Parent Entropy
parent_counts = df['Pass'].value_counts(normalize=True)
parent_entropy = -sum(parent_counts * np.log2(parent_counts))

print("Parent Entropy:", round(parent_entropy,3))

# Step 2: Entropy after split
weighted_entropy = 0

for value in df['Study'].unique():
    subset = df[df['Study'] == value]
    counts = subset['Pass'].value_counts(normalize=True)
    entropy = -sum(counts * np.log2(counts))
    weight = len(subset) / len(df)
    weighted_entropy += weight * entropy

print("Weighted Entropy:", round(weighted_entropy,3))

# Step 3: Information Gain
info_gain = parent_entropy - weighted_entropy

print("Information Gain:", round(info_gain,3))

