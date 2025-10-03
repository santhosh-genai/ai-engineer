import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 1 , figsize=(20, 6))  # 2 rows, 1 column

testcase = [12, 15, 20, 18, 22, 30, 25, 16, 19, 28, 24, 14]
axes[0].hist(testcase, bins=5, color='skyblue', edgecolor='black')
axes[0].set_title('Distribution of Test Execution Times')
axes[0].set_xlabel('Duration (seconds)')
axes[0].set_ylabel('Number of Test Cases')


defect = ['High', 'Low', 'Medium'] 
severity = [10, 5, 8]
axes[1].pie(severity,labels=defect,autopct='%1.1f%%',startangle=90)
axes[1].set_title('Defect Severity Distribution')
axes[1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Add spacing between subplots
plt.tight_layout()

plt.show()