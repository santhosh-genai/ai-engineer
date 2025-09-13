class student:
    def __init__(self,name,grade,department):
        self.name = name
        self.grade = grade
        self.department = department

    def print_info(self):
        print(self.name,self.grade,self.department)
        
    def upgrade_grade(self, new_grade):
        self.grade = new_grade

student1 = student("Santhosh","A","CSE")
student2 = student("Kumar","B","CSE")
student3 = student("Ravi","A","CSE")

students = [student1, student2, student3]
for stud in students:
    stud.print_info()

student1.upgrade_grade("A+")
student1.print_info() 
