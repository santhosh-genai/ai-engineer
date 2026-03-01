# Program 1: Manual Gini Calculation

import numpy as np

# Example: 6 Pass, 4 Fail
p_pass = 6/10
p_fail = 4/10

gini = 1 - (p_pass**2 + p_fail**2)

print("Gini Index:", round(gini, 3))
