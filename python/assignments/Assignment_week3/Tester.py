import numpy as np
class ManualTester:
    @staticmethod
    def analyze(data):
        print("first 5 test execution times:", data[:5])

class AutomatedTester:
    @staticmethod
    def analyze(data):
        print("Fastest test execution time:", data.min())
    
class PerformanceTester:
    @staticmethod
    def analyze(data):
        print("95th percentile execution time:", np.percentile(data, 95))

def show_analysis(tester, data):
    tester.analyze(data)

execution_times = np.array([10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80])

if __name__ == "__main__":
    manual = ManualTester()
    automated = AutomatedTester()
    performance = PerformanceTester()
    
    print("Manual Testing Analysis:")
    show_analysis(manual, execution_times)
    
    print("\nAutomated Testing Analysis:")
    show_analysis(automated, execution_times)
    
    print("\nPerformance Testing Analysis:")
    show_analysis(performance, execution_times)
