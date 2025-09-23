class Person:
    def __init__(self, name):
        self.name = name

class Employee(Person):
    def __init__ (self, name, id):
        super().__init__(name)
        self.id = id

class Manager(Employee):
    def __init__ (self, name, id, size):
        super().__init__(name, id)
        self.size = size

    def show_details(self):
        print("Employee Name:", self.name, "Employee ID:", self.id, "Team Size:", self.size)

emp1 = Manager("Alice", 1001, 20)
emp1.show_details()

emp2 = Manager("Bob", 1002, 30)
emp2.show_details()