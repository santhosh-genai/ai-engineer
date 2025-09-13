class person: # Class definition
    def __init__(self,name): # Constructor definition
        self.name=name # Attribute assignment 
    def display(self): # Method definition
        print("Name:", self.name) 
p1=person("Alice") # Object creation
p1.display() # Method call 
p2=person("Bob") # Object creation
p2.display() # Method call