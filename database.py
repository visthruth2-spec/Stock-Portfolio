"""
database.py

Handles all JSON database operations for the
Smart Stock Portfolio Management System.
"""

import os
import json


class Database:
    """
    Handles reading and writing data
    from JSON files.
    """

    DATA_FOLDER = "data"

    USERS_FILE = os.path.join(
        DATA_FOLDER,
        "users.json"
    )

    MARKET_FILE = os.path.join(
        DATA_FOLDER,
        "market.json"
    )

    TRANSACTION_FILE = os.path.join(
        DATA_FOLDER,
        "transactions.json"
    )

    WATCHLIST_FILE = os.path.join(
        DATA_FOLDER,
        "watchlist.json"
    )

    def __init__(self):
        """
        Initialize database files.
        """

        self.create_database()

    def create_database(self):
        """
        Create data folder and JSON files.
        """

        if not os.path.exists(self.DATA_FOLDER):
            os.mkdir(self.DATA_FOLDER)

        files = {
            self.USERS_FILE: {},
            self.MARKET_FILE: self.default_market(),
            self.TRANSACTION_FILE: [],
            self.WATCHLIST_FILE: {}
        }

        for file, default_data in files.items():

            if not os.path.exists(file):

                self.write_data(
                    file,
                    default_data
                )

    def default_market(self):
        """
        Returns default stock market data.
        """

        return {

            "TCS": {
                "name": "Tata Consultancy Services",
                "price": 3500.00
            },

            "INFY": {
                "name": "Infosys",
                "price": 1600.00
            },

            "RELIANCE": {
                "name": "Reliance Industries",
                "price": 2500.00
            },

            "WIPRO": {
                "name": "Wipro",
                "price": 450.00
            },

            "HDFC": {
                "name": "HDFC Bank",
                "price": 1700.00
            },

            "ICICI": {
                "name": "ICICI Bank",
                "price": 1200.00
            },

            "SBIN": {
                "name": "State Bank of India",
                "price": 850.00
            },

            "TATASTEEL": {
                "name": "Tata Steel",
                "price": 160.00
            }
        }

    def read_data(self, file_path):
        """
        Read JSON data safely.
        """

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):

            return None

    def write_data(self, file_path, data):
        """
        Write data into JSON file.
        """

        try:

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

            return True

        except Exception as error:

            print(
                "Database Error:",
                error
            )

            return False

    # -------------------------
    # User Database Methods
    # -------------------------

    def get_users(self):
        """
        Return all users.
        """

        users = self.read_data(
            self.USERS_FILE
        )

        return users if users else {}

    def save_users(self, users):
        """
        Save all users.
        """

        return self.write_data(
            self.USERS_FILE,
            users
        )

    # -------------------------
    # Market Database Methods
    # -------------------------

    def get_market(self):
        """
        Return all stocks.
        """

        market = self.read_data(
            self.MARKET_FILE
        )

        return market if market else {}

    def save_market(self, market):
        """
        Save market data.
        """

        return self.write_data(
            self.MARKET_FILE,
            market
        )

    # -------------------------
    # Transaction Methods
    # -------------------------

    def get_transactions(self):
        """
        Return all transactions.
        """

        transactions = self.read_data(
            self.TRANSACTION_FILE
        )

        return transactions if transactions else []

    def save_transactions(self, transactions):
        """
        Save transaction history.
        """

        return self.write_data(
            self.TRANSACTION_FILE,
            transactions
        )

    # -------------------------
    # Watchlist Methods
    # -------------------------

    def get_watchlists(self):
        """
        Return all watchlists.
        """

        watchlists = self.read_data(
            self.WATCHLIST_FILE
        )

        return watchlists if watchlists else {}

    def save_watchlists(self, watchlists):
        """
        Save watchlist data.
        """

        return self.write_data(
            self.WATCHLIST_FILE,
            watchlists
        )