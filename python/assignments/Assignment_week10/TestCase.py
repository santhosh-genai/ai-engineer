class TestCase:
    def __init__(self, test_id, test_name, module, status):
        self.test_id = test_id
        self.test_name = test_name
        self.module = module
        self.status = status

    def execute_test(self, result):
        if result:
            self.status = "Passed"
        else:
            self.status = "Failed"
    
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

