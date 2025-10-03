import matplotlib.pyplot as plt

test_results = {'Passed': 95, 'Failed': 50, 'Skipped': 2}

bars = plt.bar(test_results.keys(), test_results.values(), width=0.4,
         edgecolor='black', color=['green', 'red', 'yellow'])
plt.legend(bars, test_results.keys(), loc='upper right')

plt.title('Test Execution Results')

plt.xlabel('Test Status')
plt.ylabel('Number of Test Cases')

plt.show()
