"""
wallet.py

Handles all wallet-related operations.
"""

from core.database import Database
from core.utils import (
    print_header,
    success,
    error,
    format_currency,
    get_float,
    confirm_action
)
from models.user import User


class WalletManager:
    """
    Handles wallet operations.
    """

    def __init__(self):
        self.database = Database()

    # ==========================
    # Database Helper Methods
    # ==========================

    def load_users(self):
        """
        Load users from database as User objects.
        """

        users_data = self.database.get_users()

        users = {}

        for username, data in users_data.items():
            users[username] = User.from_dict(
                username,
                data
            )

        return users


    def save_users(self, users):
        """
        Save User objects into JSON.
        """

        data = {}

        for username, user in users.items():
            data[username] = user.to_dict()

        self.database.save_users(data)


    # ==========================
    # Wallet Operations
    # ==========================

    def show_balance(self, user):
        """
        Display current wallet balance.
        """

        print_header("WALLET BALANCE")

        print(
            f"User           : {user.username}"
        )

        print(
            f"Current Balance: "
            f"{format_currency(user.get_balance())}"
        )


    def deposit_money(self, user):
        """
        Add money to user's wallet.
        """

        print_header("DEPOSIT MONEY")

        amount = get_float(
            "Enter deposit amount: ₹",
            minimum=1
        )

        if not confirm_action(
            f"Deposit {format_currency(amount)}?"
        ):
            error("Deposit cancelled.")
            return False

        users = self.load_users()

        users[user.username].deposit(amount)

        self.save_users(users)

        # Update current session object
        user.deposit(amount)

        success(
            f"{format_currency(amount)} deposited successfully."
        )

        self.show_balance(user)

        return True


    def withdraw_money(self, user):
        """
        Remove money from wallet.
        """

        print_header("WITHDRAW MONEY")

        print(
            f"Available Balance: "
            f"{format_currency(user.get_balance())}"
        )

        amount = get_float(
            "Enter withdrawal amount: ₹",
            minimum=1
        )

        if amount > user.get_balance():

            error(
                "Insufficient wallet balance."
            )

            return False


        if not confirm_action(
            f"Withdraw {format_currency(amount)}?"
        ):
            error("Withdrawal cancelled.")
            return False


        users = self.load_users()

        users[user.username].withdraw(amount)

        self.save_users(users)

        # Update current session object
        user.withdraw(amount)

        success(
            f"{format_currency(amount)} withdrawn successfully."
        )

        self.show_balance(user)

        return True


    def add_profit(self, user, amount):
        """
        Add money to wallet after selling stocks.
        """

        users = self.load_users()

        users[user.username].deposit(amount)

        self.save_users(users)

        user.deposit(amount)


    def deduct_investment(self, user, amount):
        """
        Deduct money from wallet when buying stocks.
        """

        if amount > user.get_balance():

            return False


        users = self.load_users()

        users[user.username].withdraw(amount)

        self.save_users(users)

        user.withdraw(amount)

        return True


    # ==========================
    # Wallet Summary
    # ==========================

    def wallet_summary(self, user):
        """
        Display complete wallet details.
        """

        print_header("WALLET SUMMARY")

        print(
            f"Account Holder : {user.username}"
        )

        print(
            f"Wallet Balance : "
            f"{format_currency(user.get_balance())}"
        )

        if user.get_balance() >= 100000:
            status = "Excellent"

        elif user.get_balance() >= 50000:
            status = "Good"

        elif user.get_balance() >= 10000:
            status = "Average"

        else:
            status = "Low Balance"


        print(
            f"Financial Status: {status}"
        )