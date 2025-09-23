marks = [78, 85, 62, 90, 55, 88]
print("highest marks:", max(marks))
print("lowest marks:", min(marks))
print("average:", sum(marks)/len(marks))
print("Distinction marks:")
for mark in marks:
    if mark >= 75:
        print(mark)
marks.append(95)
print("marks after adding 95:", marks)
marks.remove(55)
print("marks after removing 55:", marks)
marks.sort()
print("updated marks:", marks)