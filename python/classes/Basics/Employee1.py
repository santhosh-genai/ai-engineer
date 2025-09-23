class Employee:
    def __init__(self, name, id):
        self.name = name
        self.id = id
class Tester(Employee):
    def __init__(self, name, id):
        super().__init__(name, id)
    def run_test(self):
        print(f"Tester Name: {self.name}, ID: {self.id}", "is running tests.")

emp1 = Tester("John Doe", 101)
emp1.run_test()
emp2 = Tester("Jane Smith", 102)
emp2.run_test()
