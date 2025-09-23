import numpy as np
onedim = np.array([20, 30, 40, 50, 60])
print("\nSingle Dimensional Array")
print(onedim)
print("Array Dimension is:", onedim.ndim)
print(onedim[2:])
print(onedim[3:5])
print(onedim[-4])
print(onedim[::-1])

twodim = np.array([[10, 20, 30, 40], [60, 70, 80, 90], [100, 110, 120, 130]])
print("\nTwo Dimensional Array")
sum = np.sum(twodim)
sum1 = 0
for row in twodim:
    for col in row:
        sum1 += col
print(twodim)
print("Array Dimension is:", twodim.ndim)
print(twodim[0][1])
print(twodim[1][1])
print(twodim[0][3])
matrix = twodim[1, :]
print("Matrix is:\n", matrix)
matrix = twodim[:2, 1:3]
print("Matrix is:\n", matrix)
print("Sum of two Dimension Array is with built in function:", sum)
print("Sum of two Dimension Array is without built in function:", sum1)

threedim = np.array([[[10, 20, 30], [40, 50, 60]], [[70, 80, 90], [100, 110, 120]]])
print("\nThree Dimensional Array")
print(threedim)
print("Array Dimension is:", threedim.ndim)
print(threedim[0][0][0])
print(threedim[0][1][2])
print(threedim[1][1][2])