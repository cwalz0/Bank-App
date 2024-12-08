import typing


class Account:
    """
    A bank account.

    Attributes:
        name (str): The name of the account holder.
        balance (float): The balance of the account.
    """

    def __init__(self, name: str, balance: float = 0.0) -> None:
        """
        Initialize an Account instance.

        Args:
            name (str): The account holder's name.
            balance (float, optional): The initial balance. Defaults to 0.0.
        """
        self.__account_name: str = name
        self.__account_balance: float = balance
        self.set_balance(balance)

    def deposit(self, amount: float) -> bool:
        """
        Deposit an amount into the account.

        Args:
            amount (float): The amount to deposit.

        Returns:
            bool: True if deposit is successful, False otherwise.
        """
        if amount > 0:
            self.__account_balance += amount
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        """
        Withdraw an amount from the account.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            bool: True if withdrawal is successful, False otherwise.
        """
        if amount > 0 and amount <= self.get_balance():
            self.__account_balance -= amount
            return True
        return False

    def get_name(self) -> str:
        """Returns the name of the account holder."""
        return self.__account_name

    def get_balance(self) -> float:
        """Returns the balance of the account."""
        return self.__account_balance

    def set_balance(self, value: float) -> None:
        """
        Set the account balance.

        Args:
            value (float): The new balance value. Must be non-negative.
        """
        if value >= 0:
            self.__account_balance = value
        else:
            self.__account_balance = 0

    def set_name(self, value: str) -> None:
        """
        Set the account holder's name.

        Args:
            value (str): The new name of the account holder.
        """
        self.__account_name = value

    def __str__(self) -> str:
        """String representation of the account."""
        return f"Account name = {self.get_name()}, Account balance = {self.get_balance():.2f}"


class SavingsAccount(Account):
    """
    Represents a savings account that applies interest every 5 deposits.

    Attributes:
        MINIMUM (float): The minimum balance required for the account.
        RATE (float): The interest rate applied on the balance.
    """

    MINIMUM: float = 100.0
    RATE: float = 0.02

    def __init__(self, name: str) -> None:
        """
        Initialize a SavingsAccount instance.

        Args:
            name (str): The account holder's name.
        """
        super().__init__(name, self.MINIMUM)
        self.__deposit_count: int = 0

    def apply_interest(self) -> None:
        """Applies interest to the account balance."""
        self.set_balance(self.get_balance() + (self.get_balance() * self.RATE))

    def deposit(self, amount: float) -> bool:
        """
        Deposit an amount into the savings account and apply interest after every 5 deposits.

        Args:
            amount (float): The amount to deposit.

        Returns:
            bool: True if deposit is successful, False otherwise.
        """
        if amount > 0:
            self.__deposit_count += 1
            super().deposit(amount)
            if self.__deposit_count % 5 == 0:
                self.apply_interest()
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        """
        Withdraw an amount from the savings account.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            bool: True if withdrawal is successful, False otherwise.
        """
        if amount > 0 and (self.get_balance() - amount) >= self.MINIMUM:
            return super().withdraw(amount)
        return False

    def set_balance(self, value: float) -> None:
        """
        Sets the savings account balance.

        Args:
            value (float): The new balance value.
        """
        if value < self.MINIMUM:
            self.__account_balance = self.MINIMUM
        else:
            super().set_balance(value)

    def get_deposit_counter(self) -> int:
        """
        Returns the number of deposits made to the account.

        Returns:
            int: The deposit counter.
        """
        return self.__deposit_count

    def __str__(self) -> str:
        """Savings account info."""
        return f"SAVING ACCOUNT: Account name = {self.get_name()}, Account balance = {self.get_balance():.2f}"
