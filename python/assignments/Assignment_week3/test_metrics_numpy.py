import numpy as np

# Create a 5x50 matrix of random execution times
# 5 test cycles with 50 tests each, values ranging from 5 to 50 milliseconds
execution_times = np.random.randint(5, 51, size=(5, 50))
print("Execution Times:\n", execution_times)

# Basic Statistical Analysis
#--------------------------
# Calculate mean execution time for each cycle (axis=1 means row-wise)
avg_times = np.mean(execution_times, axis=1)
print("\nAverage Execution Times for each cycle:", avg_times)

# Find the maximum execution time across all tests and cycles
max_times = np.max(execution_times)
print("Maximum Execution Times:", max_times)

# Calculate standard deviation for each cycle to measure time variability
standard_devs = np.std(execution_times, axis=1)
print("Standard Deviation of Execution Times for each cycle:", standard_devs)

# Array Slicing Examples
#---------------------
# Extract first 10 tests from Cycle 1 (index 0)
print("\nFirst 10 tests from Cycle 1:", execution_times[0][:10])

# Extract last 5 tests from Cycle 5 (index 4)
print("Last 5 tests from Cycle 5:", execution_times[4][-5:])

# Extract every alternate test from Cycle 3 (index 2)
print("Alternate tests from Cycle 3:", execution_times[2][::2])

# Element-wise Operations
#----------------------
# Add execution times of Cycle 1 and 2
print("\nSum of Cycle 1 and 2 times:", execution_times[0] + execution_times[1])

# Multiply execution times of Cycle 1 and 2
print("Product of Cycle 1 and 2 times:", execution_times[0] * execution_times[1])

# Find difference in execution times between Cycle 2 and 3
print("Difference between Cycle 2 and 3 times:", execution_times[1] - execution_times[2])

# Mathematical Transformations
#--------------------------
# Calculate square root - useful for normalizing skewed distributions
sqrt = np.sqrt(execution_times)
print("\nSquare root of execution times (first row):", sqrt[0][:10])

# Calculate cube - emphasizes differences between values
cube = np.power(execution_times, 3)
print("Cube of execution times (first row):", cube[0][:10])

# Natural logarithm - useful for data with exponential growth patterns
log = np.log(execution_times)
print("Natural logarithm of execution times (first row):", log[0][:10])

# Array Copy Demonstrations
#-----------------------
# Shallow copy - creates a view of the original array (shares the same data)
shallow_copy = execution_times.view()
shallow_copy[0][0] = 999  # Modifying shallow copy affects original
print("\nShallow copy after modification:\n", shallow_copy[0][:5])
print("Original array after shallow copy modification:\n", execution_times[0][:5])

# Deep copy - creates a completely independent copy
deep_copy = execution_times.copy()
deep_copy[0][0] = 555  # Modifying deep copy doesn't affect original
print("\nDeep copy after modification:\n", deep_copy[0][:5])
print("Original array remains unchanged:\n", execution_times[0][:5])

# Further demonstrate shallow copy behavior
shallow_copy[0][0] = 1000  # Changes reflect in both arrays
print("\nOriginal array after another shallow copy modification:\n", execution_times[0][:5])

more_than_30_secs = execution_times[1][execution_times[1] > 30]
print("Tests in Cycle 2 taking more than 30 ms:", more_than_30_secs)

every_cycle = execution_times[execution_times > 30]
print("Tests taking more than 30 ms in every cycle:", every_cycle)
