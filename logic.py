import csv
from accounts import Account, SavingsAccount
import typing


def check_account(user: str, password: str) -> bool:
    """
    Check if a user with the provided username and password exists in the database.

    Args:
        user (str): The username to check.
        password (str): The password associated with the username.

    Returns:
        bool: True if the user exists and the password matches, False otherwise.
    """
    try:
        with open("dont_look/users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["user"] == user and row["password"] == password:
                    return True
    except FileNotFoundError:
        print("Error: users.csv file not found.")
    except KeyError:
        print("Error: Invalid CSV Form.")
    return False


def add_user(user: str, password: str) -> None:
    """
    Add a new user to the database with default account values.

    Args:
        user (str): The username for the new user.
        password (str): The password for the new user.

    Raises:
        ValueError: If the username already exists.
        Exception: For any other issue writing to the file.
    """
    try:
        # Check if the file exists and whether the username already exists
        user_exists = False
        try:
            with open("dont_look/users.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["user"] == user:
                        user_exists = True
                        break
        except FileNotFoundError:
            # If the file doesn't exist, we'll create it later
            pass

        if user_exists:
            raise ValueError(f"Username '{user}' already exists. Please choose a different username.")

        # Add the new user
        with open("dont_look/users.csv", "a", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["user", "password", "balance", "deposit_counter", "savings_balance"],
            )

            # Write the header if the file is empty
            if file.tell() == 0:
                writer.writeheader()

            # Add user with default values
            writer.writerow(
                {
                    "user": user,
                    "password": password,
                    "balance": 0.0,
                    "deposit_counter": 0,
                    "savings_balance": 0.0,
                }
            )

    except ValueError as e:
        print(e)
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise


def get_user_details(user: str):
    """
    Retrieve account details for a user.

    Args:
        user (str): The username of the user to retrieve details for.

    Returns:
            - An Account object for the user.
            - The deposit counter value (int).
            - The savings account balance (float).

    Raises:
        FileNotFoundError: If the CSV file is not found.
        KeyError: If the CSV is malformed.
        ValueError: If the user is not found in the database.
    """
    try:
        with open("dont_look/users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["user"] == user:
                    balance = float(row["balance"])
                    deposit_counter = int(row["deposit_counter"])
                    savings_balance = float(row["savings_balance"])
                    return Account(user, balance), deposit_counter, savings_balance
    except FileNotFoundError:
        print("Error: users.csv file not found.")
    except KeyError:
        print("Error: Invalid CSV Form.")
    raise ValueError("User not found")


def set_account_details(
    user: str, account: Account, deposit_counter: int, savings_account: SavingsAccount
) -> None:
    """
    Update account, deposit counter, and savings account details for a user in the database.

    Args:
        user (str): The username of the user to update.
        account (Account): The user's main account object.
        deposit_counter (int): The updated deposit counter for the savings account.
        savings_account (SavingsAccount): The user's savings account object.

    Raises:
        FileNotFoundError: If the CSV file is not found.
        Exception: If there is any other issue writing to the file.
    """
    updated_rows = []
    try:
        with open("dont_look/users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["user"] == user:
                    row["balance"] = str(account.get_balance())
                    row["deposit_counter"] = str(
                        savings_account.get_deposit_counter()
                    )  # Update deposit counter
                    row["savings_balance"] = str(savings_account.get_balance())
                updated_rows.append(row)

        with open("dont_look/users.csv", "w", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "user",
                    "password",
                    "balance",
                    "deposit_counter",
                    "savings_balance",
                ],
            )
            writer.writeheader()
            writer.writerows(updated_rows)
    except FileNotFoundError:
        print("Error: users.csv file not found.")
    except Exception as e:
        print(f"Error: {e}")
