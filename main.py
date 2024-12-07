from accounts import *


def main():
    a1 = Account('John')
    print(a1)                   # Account name = John, Account balance = 0.00
    a1.deposit(-20.50)
    a1.deposit(0)
    a1.deposit(50)
    a1.withdraw(10.5)
    print(a1)                   # Account name = John, Account balance = 39.50

    a2 = Account('Tom', 30)
    print(a2)                   # Account name = Tom, Account balance = 30.00
    print(a2.withdraw(-5))      # False
    print(a2.withdraw(0))       # False
    print(a2.withdraw(30.1))    # False
    print(a2.withdraw(30))      # True
    print(a2.deposit(-5))       # False
    print(a2.deposit(0))        # False

    a3 = Account('Tim', -300)
    print(a3)                   # Account name = Tim, Account balance = 0.00

    s1 = SavingAccount('Jane')
    print(s1)                   # SAVING ACCOUNT: Account name = Jane, Account balance = 100.00
    print(s1.deposit(-20.50))   # False
    print(s1.deposit(0))        # False
    print(s1.deposit(50))       # True
    s1.withdraw(10)
    print(s1)                   # SAVING ACCOUNT: Account name = Jane, Account balance = 140.00
    s1.deposit(50)
    s1.deposit(10.5)
    s1.deposit(5)
    s1.deposit(100)
    print(s1)                   # SAVING ACCOUNT: Account name = Jane, Account balance = 311.61
    print(s1.withdraw(212))     # False
    print(s1)                   # SAVING ACCOUNT: Account name = Jane, Account balance = 311.61
    print(s1.withdraw(211.61))  # True
    print(s1)                   # SAVING ACCOUNT: Account name = Jane, Account balance = 100.00
    s1.deposit(100)
    s1.deposit(100)
    s1.deposit(100)
    s1.deposit(100)
    s1.deposit(100)
    print(s1)                   # SAVING ACCOUNT: Account name = Jane, Account balance = 612.00

    a1.set_balance(0.9)
    print(a1)                   # Account name = John, Account balance = 0.90
    a1.set_balance(-10)
    print(a1)                   # Account name = John, Account balance = 0.00

    s1.set_balance(101)
    print(s1)                   # SAVING ACCOUNT: Account name = Jane, Account balance = 101.00
    s1.set_balance(99.9)
    print(s1)                   # SAVING ACCOUNT: Account name = Jane, Account balance = 100.00


if __name__ == '__main__':
    main()

'''
Overall program output should be:

Account name = John, Account balance = 0.00
Account name = John, Account balance = 39.50
Account name = Tom, Account balance = 30.00
False
False
False
True
False
False
Account name = Tim, Account balance = 0.00
SAVING ACCOUNT: Account name = Jane, Account balance = 100.00
False
False
True
SAVING ACCOUNT: Account name = Jane, Account balance = 140.00
SAVING ACCOUNT: Account name = Jane, Account balance = 311.61
False
SAVING ACCOUNT: Account name = Jane, Account balance = 311.61
True
SAVING ACCOUNT: Account name = Jane, Account balance = 100.00
SAVING ACCOUNT: Account name = Jane, Account balance = 612.00
Account name = John, Account balance = 0.90
Account name = John, Account balance = 0.00
SAVING ACCOUNT: Account name = Jane, Account balance = 101.00
SAVING ACCOUNT: Account name = Jane, Account balance = 100.00
'''