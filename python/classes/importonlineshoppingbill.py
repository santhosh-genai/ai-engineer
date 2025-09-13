"""Testing import of onlineshoppingbill module and its function calculate_bill"""
import onlineshoppingbill

print(__doc__)
print(__name__)

print("Bill 1:", onlineshoppingbill.calculate_bill(500, 2))
print("Bill 2:", onlineshoppingbill.calculate_bill(500, 2, 0.1))
print("Bill 3:", onlineshoppingbill.calculate_bill(500, 2, discount=50))
print("Bill 4:", onlineshoppingbill.calculate_bill(500, 2, tax=0.08, discount=100))