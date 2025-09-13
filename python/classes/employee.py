# 1. Ask the user for their age.
# 2. Ask the user for their years of IT experience.
# 3. If the age is greater than or equal to 22 and experience is greater than or equal to 2 → print
# "Access Granted".
# 4. Otherwise → print "Access Denied".

age = int(input("Enter your age: "))
experience = int(input("Enter your years of IT experience: "))

if age >= 22 and experience >= 2:
    print("Access Granted")
else:
    print("Access Denied")
