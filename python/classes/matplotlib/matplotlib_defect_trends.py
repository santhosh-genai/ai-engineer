import matplotlib.pyplot as plt

Weeks = [1, 2, 3, 4, 5, 6]
Defects = [5, 8, 6, 10, 7, 4]

plt.plot(Weeks, Defects, marker='>', linestyle=':', color='orange')
plt.grid(True)
plt.title('Defect Trends Over Time')
plt.xlabel('Week Number')
plt.ylabel('Number of Defects')

plt.savefig('defect_trends.png')  # Save the plot as a PNG file
plt.show()
