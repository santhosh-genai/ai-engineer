def calculate_bill(item_cost, quantity, tax=0.05, discount=0):
    total = (item_cost * quantity) + (item_cost * quantity * tax) - discount
    return total
print(calculate_bill(100, 2, discount=10))
