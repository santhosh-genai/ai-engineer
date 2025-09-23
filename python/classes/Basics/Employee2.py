class Employee:
    def __init__(self,name):
        self.name = name
    
class AutomationSkills:
    def write_script(self):
        print("writing automation scripts.")

class AutomationTester(Employee, AutomationSkills):
    def __init__(self, name):
        super().__init__(name)

    def execute_tests(self):
        print(f"Automation Tester Name: {self.name} is executing tests.")

emp1 = AutomationTester("Charlie")
emp1.write_script()
emp1.execute_tests()
