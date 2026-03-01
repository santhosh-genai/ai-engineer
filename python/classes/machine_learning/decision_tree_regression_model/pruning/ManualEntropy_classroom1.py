#Show how entropy is calculated mathematically.
# Program 1: Manual Entropy Calculation

import numpy as np

# Example: 6 Pass, 4 Fail
total = 10
p_pass = 6/10
p_fail = 4/10

entropy = - (p_pass * np.log2(p_pass) +
             p_fail * np.log2(p_fail))

print("Entropy:", round(entropy, 3))

