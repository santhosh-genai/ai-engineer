def calc_salary(basic,hra,da,bonus=500):
    salary = basic + hra + da + bonus
    return salary

salary1 =   calc_salary(50000, 2000, 3000)
print("Salary without bonus:", salary1)
salary2 =   calc_salary(50000, 2000, 3000, 1500)
print("Salary with bonus:", salary2)