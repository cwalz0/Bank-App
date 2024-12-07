class Account:
    def __init__(self, name, balance=0):
        self.__account_name = name
        self.__account_balance = balance
        self.set_balance(balance)

    def deposit(self, amount):
        if amount > 0:
            self.__account_balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        if amount > 0 and amount <= self.get_balance():
            self.__account_balance -= amount
            return True
        return False
    
    def get_name(self):
        return self.__account_name
    
    def get_balance(self):
        return self.__account_balance
    
    def set_balance(self, value):
        if value >= 0:
            self.__account_balance = value
        else:
            self.__account_balance = 0
    
    def set_name(self, value):
        self.__account_name = value

    def __str__(self):
        return f"Account name = {self.get_name()}, Account balance = {self.get_balance():.2f}"

class SavingAccount(Account):
    MINIMUM = 100
    RATE = 0.02

    def __init__(self, name):
        super().__init__(name, self.MINIMUM)
        self.__deposit_count = 0

    def apply_interest(self):
            self.set_balance(self.get_balance() + (self.get_balance() * self.RATE))

    
    def deposit(self, amount):
        if amount > 0:
            self.__deposit_count += 1
            super().deposit(amount)
            if self.__deposit_count % 5 == 0:
                self.apply_interest()
            return True
        return False

    def withdraw(self, amount):
        if amount > 0 and (self.get_balance() - amount) >= self.MINIMUM:
            return super().withdraw(amount)
        return False
    
    def set_balance(self, value):
        if value < self.MINIMUM:
            self.__account_balance = self.MINIMUM
        else:
            super().set_balance(value)

    def __str__(self):
        return f"SAVING ACCOUNT: Account name = {self.get_name()}, Account balance = {self.get_balance():.2f}"
    
