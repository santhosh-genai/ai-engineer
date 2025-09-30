class Employee:
    def __init__(self, name, emp_id, position):
        self.name = name
        self.emp_id = emp_id
        self.position = position

    def display_info(self):
        print(f"Name: {self.name}, ID: {self.emp_id}, Position: {self.position}")

class Manager(Employee):
    def __init__(self, name, emp_id, position, team_size):
        super().__init__(name, emp_id, position) # Call base class constructor
        self.team_size = team_size 

    def display_info(self): 
        super().display_info() # Call base class method
        print(f"Team Size: {self.team_size}")

class Developer(Employee):
    def __init__(self, name, emp_id, position, programming_language):
        super().__init__(name, emp_id, position) # Call base class constructor
        self.programming_language = programming_language
        
    def display_info(self): 
        super().display_info() # Call base class method
        print(f"Programming Language: {self.programming_language}")

if __name__ == "__main__":
    mobj = Manager("Alice", 101, "Project Manager", 10)
    dobj = Developer("Bob", 102, "Software Developer", "Python")
    mobj.display_info()  # Displays Manager info
    dobj.display_info()  # Displays Developer info