import numpy as np
id = np.array([10, 15, 20, 25, 30, 35, 40, 45])

# Indexing & Shaping
# Access the first, last, and 3rd element of the array.
# Print the shape of the array.

print("first element of array is:", id[0])
print("last element of array is:", id[-1])
print("third element to the end of array is:", id[2])
print("shape of array is:", id.shape)

print("execution times of the first 3 tests:", id[:3])
print("Print every alternate test time.", id[::2])
    
print("2D array\n", id.reshape(2, 4))
print("3D array\n", id.reshape(2, 2, 2))

secondid = np.array([50, 55, 60, 65])
allid = np.concatenate((id, secondid))
print("All test times:\n", allid)

print(np.split(allid, 3))