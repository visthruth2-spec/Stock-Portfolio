"""
authentication.py

Handles user registration, login,
account settings and admin access.
"""

import getpass

from core.database import Database
from models.user import User
from core.utils import (
    get_non_empty_input,
    get_current_date,
    success,
    error,
    confirm_action,
    print_header
)


class Authentication:
    """
    Handles all authentication operations.
    """

    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"

    def __init__(self):
        self.database = Database()

    # ============================
    # Database Helpers
    # ============================

    def load_users(self):
        """
        Load users from JSON database.
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


    # ============================
    # Registration System
    # ============================

    def register(self):
        """
        Create a new user account.
        """

        print_header("CREATE NEW ACCOUNT")

        users = self.load_users()

        username = (
            get_non_empty_input(
                "Enter username: "
            ).lower()
        )

        if username in users:
            error("Username already exists.")
            return None

        password = getpass.getpass(
            "Create password: "
        )

        confirm_password = getpass.getpass(
            "Confirm password: "
        )

        if password != confirm_password:
            error("Passwords do not match.")
            return None

        new_user = User(
            username=username,
            password=password,
            created_date=get_current_date()
        )

        users[username] = new_user

        self.save_users(users)

        success(
            "Account created successfully!"
        )

        return new_user


    # ============================
    # Login System
    # ============================

    def login(self):
        """
        Verify login credentials.
        """

        print_header("USER LOGIN")

        users = self.load_users()

        username = (
            get_non_empty_input(
                "Username: "
            ).lower()
        )

        password = getpass.getpass(
            "Password: "
        )

        user = users.get(username)

        if user and user.verify_password(password):

            success(
                f"Welcome {username}!"
            )

            return user

        error(
            "Invalid username or password."
        )

        return None


    # ============================
    # Admin Login
    # ============================

    def admin_login(self):
        """
        Login for administrator.
        """

        print_header("ADMIN LOGIN")

        username = input(
            "Admin Username: "
        )

        password = getpass.getpass(
            "Admin Password: "
        )

        if (
            username == self.ADMIN_USERNAME
            and password == self.ADMIN_PASSWORD
        ):

            success(
                "Admin login successful."
            )

            return True

        error(
            "Invalid admin credentials."
        )

        return False


    # ============================
    # Account Management
    # ============================

    def change_password(self, user):
        """
        Update account password.
        """

        users = self.load_users()

        old_password = getpass.getpass(
            "Current Password: "
        )

        if not user.verify_password(
            old_password
        ):
            error("Incorrect password.")
            return

        new_password = getpass.getpass(
            "New Password: "
        )

        confirm = getpass.getpass(
            "Confirm Password: "
        )

        if new_password != confirm:
            error("Passwords do not match.")
            return

        users[user.username].change_password(
            new_password
        )

        self.save_users(users)

        success(
            "Password changed successfully."
        )


    def view_account(self, user):
        """
        Display user information.
        """

        print_header(
            "ACCOUNT DETAILS"
        )

        print(
            f"Username       : {user.username}"
        )

        print(
            f"Created Date   : {user.created_date}"
        )

        print(
            f"Wallet Balance : ₹{user.wallet:,.2f}"
        )

        print(
            f"Stocks Owned   : {len(user.portfolio)}"
        )


    def delete_account(self, user):
        """
        Permanently delete a user account.
        """

        print_header(
            "DELETE ACCOUNT"
        )

        warning_message = (
            "This action will remove all "
            "your data permanently."
        )

        print(warning_message)

        if not confirm_action(
            "Do you want to continue"
        ):
            return False

        users = self.load_users()

        if user.username in users:

            del users[user.username]

            self.save_users(users)

            success(
                "Account deleted successfully."
            )

            return True

        error(
            "Account not found."
        )

        return False