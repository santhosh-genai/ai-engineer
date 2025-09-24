import numpy as np

class TestReport:
    def __init__(self, execution_times):
        self.execution_times = execution_times
        
    def average_time(self):
        mean = np.mean(self.execution_times)
        return mean

    def max_time(self):
        maximum = np.max(self.execution_times)
        return maximum
    
class RegressionReport(TestReport):
    def __init__(self, execution_times):
        super().__init__(execution_times)
        
    def slow_test(self, threshold):
        slow_tests = self.execution_times[self.execution_times > threshold]
        return slow_tests
     
tests = np.array([10, 15, 20, 25, 30, 35, 40, 45])
obj = RegressionReport(tests)
print("Average execution time:", obj.average_time())
print("Maximum execution time:", obj.max_time())
print("Tests slower than 25:", obj.slow_test(25))