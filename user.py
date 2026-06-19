"""
user.py

Contains the User class for handling
user account information and operations.
"""


class User:
    """
    Represents a system user.
    """

    DEFAULT_WALLET_BALANCE = 100000.00

    def __init__(
        self,
        username,
        password,
        wallet=None,
        portfolio=None,
        created_date=None
    ):
        """
        Initialize a new user object.
        """

        self.username = username
        self.__password = password

        self.wallet = (
            wallet
            if wallet is not None
            else self.DEFAULT_WALLET_BALANCE
        )

        self.portfolio = (
            portfolio
            if portfolio is not None
            else {}
        )

        self.created_date = created_date

    # =============================
    # Password Management
    # =============================

    def verify_password(self, password):
        """
        Checks whether the password is correct.
        """

        return self.__password == password


    def change_password(self, new_password):
        """
        Updates the user password.
        """

        self.__password = new_password


    def get_password(self):
        """
        Returns password for database storage.
        """

        return self.__password


    # =============================
    # Wallet Management
    # =============================

    def deposit(self, amount):
        """
        Add money to the wallet.
        """

        if amount > 0:
            self.wallet += amount
            return True

        return False


    def withdraw(self, amount):
        """
        Deduct money from wallet.
        """

        if amount <= self.wallet:
            self.wallet -= amount
            return True

        return False


    def get_balance(self):
        """
        Returns current wallet balance.
        """

        return self.wallet


    # =============================
    # Portfolio Management
    # =============================

    def add_stock(self, symbol, quantity, price):
        """
        Adds a stock to the portfolio.

        Calculates average buying price
        if the stock already exists.
        """

        symbol = symbol.upper()

        if symbol in self.portfolio:

            existing = self.portfolio[symbol]

            old_quantity = existing["quantity"]

            old_cost = (
                old_quantity *
                existing["average_price"]
            )

            new_cost = (
                quantity * price
            )

            total_quantity = (
                old_quantity + quantity
            )

            average_price = (
                old_cost + new_cost
            ) / total_quantity

            self.portfolio[symbol] = {
                "quantity": total_quantity,
                "average_price": average_price
            }

        else:

            self.portfolio[symbol] = {
                "quantity": quantity,
                "average_price": price
            }


    def remove_stock(self, symbol, quantity):
        """
        Removes shares from portfolio.
        """

        symbol = symbol.upper()

        if symbol not in self.portfolio:
            return False


        current_quantity = (
            self.portfolio[symbol]["quantity"]
        )


        if quantity > current_quantity:
            return False


        remaining = current_quantity - quantity


        if remaining == 0:
            del self.portfolio[symbol]

        else:
            self.portfolio[symbol][
                "quantity"
            ] = remaining


        return True


    def get_stock_details(self, symbol):
        """
        Returns details of a stock.
        """

        return self.portfolio.get(
            symbol.upper()
        )


    def get_portfolio(self):
        """
        Returns complete portfolio.
        """

        return self.portfolio


    # =============================
    # Database Conversion
    # =============================

    def to_dict(self):
        """
        Converts object into dictionary
        for JSON storage.
        """

        return {
            "password": self.__password,
            "wallet": self.wallet,
            "portfolio": self.portfolio,
            "created_date": self.created_date
        }


    @classmethod
    def from_dict(
        cls,
        username,
        data
    ):
        """
        Creates User object from JSON data.
        """

        return cls(
            username=username,
            password=data["password"],
            wallet=data.get(
                "wallet",
                cls.DEFAULT_WALLET_BALANCE
            ),
            portfolio=data.get(
                "portfolio",
                {}
            ),
            created_date=data.get(
                "created_date"
            )
        )