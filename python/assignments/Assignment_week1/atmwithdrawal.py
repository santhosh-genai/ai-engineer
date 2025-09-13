amount = int(input("Enter the amount to withdraw: "))
if amount % 100 == 0:
    print(f"Dispensing {amount}")
else:
    print("Invalid amount")