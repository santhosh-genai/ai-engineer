class bankaccount:
    def __init__(self, account_holder, balance, account_type):
        self.account_holder = account_holder
        self.balance = balance
        self.account_type = account_type

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
          print(self.account_holder + " has insufficient funds")
        else: 
         self.balance -= amount

    def display_balance(self):
        print(self.account_holder + " balance: " + str(self.balance))
if __name__ == "__main__":
    print(__name__)
    account1 = bankaccount("Santhosh", 10000, "Savings")
    account2 = bankaccount("Kumar", 20000, "Savings")

    account1.deposit(5000)
    account2.withdraw(30000)

    print("account balances:")
    account1.display_balance()
    account2.display_balance()