"""
admin.py

Handles administrator operations.
"""

from core.database import Database
from core.market import StockMarket
from core.utils import (
    print_header,
    print_table_header,
    print_table_row,
    get_non_empty_input,
    confirm_action,
    error,
    success,
    format_currency
)


class AdminPanel:
    """
    Administrator control panel.
    """

    def __init__(self):
        self.database = Database()
        self.market = StockMarket()


    # ===========================
    # User Management
    # ===========================

    def view_users(self):
        """
        Display all registered users.
        """

        print_header("REGISTERED USERS")

        users = self.database.get_users()


        if not users:
            error("No users found.")
            return


        headers = [
            "Username",
            "Created Date",
            "Wallet Balance",
            "Stocks Owned"
        ]

        print_table_header(headers)


        for username, data in users.items():

            print_table_row([
                username,
                data.get("created_date", "-"),
                format_currency(
                    data.get("wallet", 0)
                ),
                len(
                    data.get(
                        "portfolio",
                        {}
                    )
                )
            ])


    def search_user(self):
        """
        Search a user account.
        """

        print_header("SEARCH USER")

        username = (
            get_non_empty_input(
                "Enter username: "
            ).lower()
        )


        users = self.database.get_users()


        if username not in users:
            error("User not found.")
            return


        data = users[username]


        print("\nUser Details")
        print("-" * 40)

        print(
            "Username:",
            username
        )

        print(
            "Created:",
            data.get(
                "created_date",
                "-"
            )
        )

        print(
            "Wallet:",
            format_currency(
                data.get(
                    "wallet",
                    0
                )
            )
        )

        print(
            "Stocks Owned:",
            len(
                data.get(
                    "portfolio",
                    {}
                )
            )
        )


    def delete_user(self):
        """
        Permanently remove a user.
        """

        print_header(
            "DELETE USER"
        )


        username = (
            get_non_empty_input(
                "Enter username to delete: "
            ).lower()
        )


        users = self.database.get_users()


        if username not in users:
            error("User does not exist.")
            return


        if not confirm_action(
            f"Delete account {username}?"
        ):
            return


        del users[username]


        self.database.save_users(users)


        success(
            "User deleted successfully."
        )


    # ===========================
    # Market Management
    # ===========================

    def market_menu(self):
        """
        Display market options.
        """

        while True:

            print_header(
                "MARKET MANAGEMENT"
            )

            print("1. View Market")
            print("2. Add Stock")
            print("3. Remove Stock")
            print("4. Update Stock Price")
            print("5. Refresh Market")
            print("6. Back")

            choice = input(
                "\nEnter choice: "
            )


            if choice == "1":
                self.market.display_market()

            elif choice == "2":
                self.market.add_stock()

            elif choice == "3":
                self.market.remove_stock()

            elif choice == "4":
                self.market.update_stock_price()

            elif choice == "5":
                self.market.refresh_market()

            elif choice == "6":
                break

            else:
                error("Invalid option.")


    # ===========================
    # Platform Analytics
    # ===========================

    def platform_statistics(self):
        """
        Display complete system statistics.
        """

        print_header(
            "PLATFORM STATISTICS"
        )


        users = self.database.get_users()

        stocks = self.database.get_market()

        transactions = (
            self.database.get_transactions()
        )


        total_balance = 0

        total_holdings = 0


        for data in users.values():

            total_balance += (
                data.get(
                    "wallet",
                    0
                )
            )

            total_holdings += len(
                data.get(
                    "portfolio",
                    {}
                )
            )


        print(
            "Total Registered Users:",
            len(users)
        )

        print(
            "Available Stocks:",
            len(stocks)
        )

        print(
            "Total Transactions:",
            len(transactions)
        )

        print(
            "Total User Wallet Balance:",
            format_currency(total_balance)
        )

        print(
            "Total Different Holdings:",
            total_holdings
        )


    # ===========================
    # Main Admin Dashboard
    # ===========================

    def dashboard(self):
        """
        Administrator menu.
        """

        while True:

            print_header(
                "ADMIN CONTROL PANEL"
            )

            print(
                "1. View All Users"
            )

            print(
                "2. Search User"
            )

            print(
                "3. Delete User"
            )

            print(
                "4. Market Management"
            )

            print(
                "5. Platform Statistics"
            )

            print(
                "6. Logout"
            )


            choice = input(
                "\nEnter your choice: "
            )


            if choice == "1":

                self.view_users()


            elif choice == "2":

                self.search_user()


            elif choice == "3":

                self.delete_user()


            elif choice == "4":

                self.market_menu()


            elif choice == "5":

                self.platform_statistics()


            elif choice == "6":

                success(
                    "Admin logged out successfully."
                )

                break


            else:

                error(
                    "Invalid choice. Try again."
                )