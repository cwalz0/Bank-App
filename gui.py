from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QFormLayout, QHBoxLayout, QVBoxLayout, 
    QPushButton, QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt
from logic import check_account, add_user, get_user_details, set_account_details
from accounts import Account, SavingsAccount
import typing


class LoginWindow(QWidget):
    """
    The main login window of the Bank App.
    Allows users to log in or register a new account.
    """
    def __init__(self) -> None:
        """
        Start the LoginWindow.
        """
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(600, 400)

        user_label = QLabel("Username:")
        self.user_input: QLineEdit = QLineEdit()
        
        password_label = QLabel("Password:")
        self.__password_input: QLineEdit = QLineEdit()
        self.__password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_form_layout = QFormLayout()
        login_form_layout.addRow(user_label, self.user_input)
        login_form_layout.addRow(password_label, self.__password_input)

        button_layout = QHBoxLayout()
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.validate_login)
        submit_button.setFixedWidth(175)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.create_user)
        register_button.setFixedWidth(175)

        button_layout.addWidget(register_button)
        button_layout.addWidget(submit_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(login_form_layout)
        self.main_layout.addLayout(button_layout)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

    def validate_login(self) -> None:
        """
        Validate user credentials and open the dashboard if successful.
        """
        user: str = self.user_input.text().strip().lower()
        password: str = self.__password_input.text().strip()

        if check_account(user, password):
            self.open_dashboard(user)
        else:
            QMessageBox.information(self, "Login Failed", "Incorrect Username or password")
            self.user_input.clear()
            self.__password_input.clear()

    def open_dashboard(self, user: str) -> None:
        """
        Open the dashboard window after successful login.

        Args:
            user: The username of the logged-in user.
        """
        self.open_dashboard = DashboardWindow(user)
        self.open_dashboard.show()
        self.close()

    def create_user(self) -> None:
        """
        Create a new user account with the provided username and password.
        """
        user: str = self.user_input.text().strip().lower()
        password: str = self.__password_input.text().strip()

        if not user or not password:
            QMessageBox.warning(self, "Input Error", "Both User and password fields are required.")
            return

        try:
            add_user(user, password)
            QMessageBox.information(self, "Success", "User account created successfully!")
        except ValueError as e:
            QMessageBox.warning(self, "Registration Error", str(e))


class DashboardWindow(QWidget):
    """
    The main dashboard window for a logged-in user.
    Displays account details and provides actions like deposit, withdraw, 
    and creating a savings account.
    """
    def __init__(self, username: str) -> None:
        """
        Initialize the DashboardWindow.

        Args:
            username: The username of the logged-in user.
        """
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.resize(600, 400)

        account, deposit_counter, savings_balance = get_user_details(username)
        self.account = account
        self.deposit_counter = deposit_counter
        self.username = username

        self.savings_account: SavingsAccount | None = None
        if savings_balance > 0:
            self.savings_account = SavingsAccount(username)
            self.savings_account.set_balance(savings_balance)


        self.title_label = QLabel(f"Welcome {username}")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")

        self.account_label = QLabel("Account Balance")
        self.account_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.account_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.account_balance_label = QLabel(f"${self.account.get_balance():.2f}")
        self.account_balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.savings_label = QLabel("Savings Balance")
        self.savings_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.savings_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.savings_balance_label = QLabel("N/A" if not self.savings_account else f"${self.savings_account.get_balance():.2f}")
        self.savings_balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        balances_layout = QVBoxLayout()
        balances_layout.addWidget(self.account_label)
        balances_layout.addWidget(self.account_balance_label)

        savings_layout = QVBoxLayout()
        savings_layout.addWidget(self.savings_label)
        savings_layout.addWidget(self.savings_balance_label)

        account_savings_layout = QHBoxLayout()
        account_savings_layout.addLayout(balances_layout)
        account_savings_layout.addLayout(savings_layout)
        account_savings_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.deposit_button = QPushButton("Deposit")
        self.deposit_button.clicked.connect(self.deposit_to_main)
        self.withdraw_button = QPushButton("Withdraw")
        self.withdraw_button.clicked.connect(self.withdraw_from_main)

        self.deposit_savings_button = QPushButton("Deposit to Savings")
        self.deposit_savings_button.clicked.connect(self.deposit_to_savings)
        self.withdraw_savings_button = QPushButton("Withdraw from Savings")
        self.withdraw_savings_button.clicked.connect(self.withdraw_from_savings)

        buttons_layout = QVBoxLayout()
        buttons_adjust_layout = QHBoxLayout()
        buttons_account_layout = QVBoxLayout()
        buttons_savings_layout = QVBoxLayout()

        buttons_account_layout.addWidget(self.deposit_button)
        buttons_account_layout.addWidget(self.withdraw_button)
        buttons_savings_layout.addWidget(self.deposit_savings_button)
        buttons_savings_layout.addWidget(self.withdraw_savings_button)

        buttons_adjust_layout.addLayout(buttons_account_layout)
        buttons_adjust_layout.addLayout(buttons_savings_layout)
        buttons_adjust_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.addLayout(buttons_adjust_layout)

        self.create_savings_button = QPushButton("Create Savings Account")
        self.create_savings_button.clicked.connect(self.create_savings_account)
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)

        buttons_layout.addWidget(self.create_savings_button)
        buttons_layout.addWidget(self.logout_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(account_savings_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    def update_account_info(self) -> None:
        """
        Update the account and savings balances and save them.
        """
        self.account_balance_label.setText(f"${self.account.get_balance():.2f}")
        self.savings_balance_label.setText(
            "N/A" if not self.savings_account else f"${self.savings_account.get_balance():.2f}"
        )
        set_account_details(self.username, self.account, self.deposit_counter, self.savings_account or SavingsAccount(self.username))

    def deposit_to_main(self) -> None:
        """
        Deposit funds to the main account.
        """
        amount, ok = QInputDialog.getDouble(self, "Deposit", "Enter amount to deposit:", value=0, min=0)
        if ok and self.account.deposit(amount):
            self.deposit_counter += 1
            self.update_account_info()
        else:
            QMessageBox.warning(self, "Error", "Deposit failed.")

    def withdraw_from_main(self) -> None:
        """
        Withdraw funds from the main account.
        """
        amount, ok = QInputDialog.getDouble(self, "Withdraw", "Enter amount to withdraw:", value=0, min=0)
        if ok and self.account.withdraw(amount):
            self.update_account_info()
        else:
            QMessageBox.warning(self, "Error", "Insufficient funds.")

    def deposit_to_savings(self) -> None:
        """
        Deposit funds into the savings account.
        """
        if not self.savings_account:
            QMessageBox.warning(self, "Error", "You do not have a savings account!")
            return

        amount, ok = QInputDialog.getDouble(self, "Deposit to Savings", "Enter amount to deposit:", value=0, min=0)
        if ok and self.savings_account.deposit(amount):
            self.update_account_info()
        else:
            QMessageBox.warning(self, "Error", "Deposit to savings failed.")

    def withdraw_from_savings(self) -> None:
        """
        Withdraw funds from the savings account.
        """
        if not self.savings_account:
            QMessageBox.warning(self, "Error", "You do not have a savings account!")
            return

        amount, ok = QInputDialog.getDouble(self, "Withdraw from Savings", "Enter amount to withdraw:", value=0, min=0)
        if ok and self.savings_account.withdraw(amount):
            self.update_account_info()
        else:
            QMessageBox.warning(self, "Error", "Insufficient funds.")

    def create_savings_account(self) -> None:
        """
        Create a new savings account.
        """
        if self.savings_account:
            QMessageBox.warning(self, "Error", "Savings account already exists!")
            return

        initial_balance, ok = QInputDialog.getDouble(
            self, "Create Savings Account", "Enter initial balance (minimum $100):", value=100, min=100
        )
        if ok:
            self.savings_account = SavingsAccount(self.account.get_name())
            self.savings_account.set_balance(initial_balance)
            self.update_account_info()

    def logout(self) -> None:
        """
        Log the user out and go to the login window.
        """
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()