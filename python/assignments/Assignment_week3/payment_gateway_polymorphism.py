class CreditCardPayment:
    def process_payment(self, amount):
        print(f"Processing credit card payment of ${amount:.2f}")

class PayPalPayment(CreditCardPayment):
    def process_payment(self, amount):
        print(f"Processing PayPal payment of ${amount:.2f}")

class BankTransferPayment(PayPalPayment):
    def process_payment(self, amount):
        print(f"Processing bank transfer payment of ${amount:.2f}")

def make_payment(payment_method, amount):
    payment_method.process_payment(amount)

credit_card = CreditCardPayment()
paypal = PayPalPayment()       
bank_transfer = BankTransferPayment()

make_payment(credit_card, 100.00)  # Outputs: Processing credit card payment of $100.00
make_payment(paypal, 150.00)       # Outputs: Processing PayPal payment of $150.00
make_payment(bank_transfer, 200.00) # Outputs: Processing bank transfer payment of $

