class TestCase:
    def __init__(self, test_id, test_name, module, status):
        self.test_id = test_id
        self.test_name = test_name
        self.module = module
        self.status = status

    def execute_test(self, result):
        self.status = result
    
    def display_test_case(self):
        print(f"Test ID: {self.test_id}")
        print(f"Test Name: {self.test_name}")
        print(f"Module: {self.module}")
        print(f"Status: {self.status}")

    def to_csv_row(self):
        return f"{self.test_id},{self.test_name},{self.module},{self.status}"

class AutomatedTestCase(TestCase):
    def __init__(self, test_id, test_name, module, status, automation_tool):
        super().__init__(test_id, test_name, module, status)
        self.automation_tool = automation_tool

    def display_test_case(self):
        super().display_test_case()
        print(f"Automation Tool: {self.automation_tool}")
    
    def to_csv_row(self):
        return f"{super().to_csv_row()},{self.automation_tool}"

class TestSuite:
    def __init__(self, suite_name):
        self.suite_name = suite_name
        self.test_cases = []

    def add_test_case(self, test_case):
        self.test_cases.append(test_case)
    
    def run_all_tests(self):
        for testcase in self.test_cases:
            result = input(f"Enter result for test '{testcase.test_name}' (Pass/Fail): ").strip().lower()
            testcase.execute_test(result)

    def save_results_to_csv(self, filename):
        with open(filename, 'w') as file:
            file.write("Test ID,Test Name,Module,Status,Automation Tool\n")
            for testcase in self.test_cases:
                file.write(testcase.to_csv_row() + "\n")

    def summary_report(self):
        total = len(self.test_cases)
        passed = sum(1 for tc in self.test_cases if tc.status.lower() == 'pass')
        failed = sum(1 for tc in self.test_cases if tc.status.lower() == 'fail')
        not_executed = sum(1 for tc in self.test_cases if tc.status.lower() not in ['pass', 'fail'])
        
        print(f"Total Tests: {total}")
        print(f"Passed Tests: {passed}")
        print(f"Failed Tests: {failed}")
        print(f"Not Executed Tests: {not_executed}")

# Example usage:
if __name__ == "__main__":
    suite = TestSuite("Sample Test Suite")
#     2 manual test cases
# o 2 automated test cases

    tc1 = TestCase(1, "Login Test", "Authentication", "Not Executed")
    tc2 = AutomatedTestCase(2, "Payment Test", "E-Commerce", "Not Executed", "Cypress")
    tc3 = AutomatedTestCase(3, "Signup Test", "Authentication", "Not Executed", "Selenium")
    tc4 = TestCase(4, "Profile Update Test", "User Management", "Not Executed")

    suite.add_test_case(tc1)
    suite.add_test_case(tc2)
    suite.add_test_case(tc3)
    
    suite.run_all_tests()
    suite.save_results_to_csv("test_results.csv")
    suite.summary_report()
        