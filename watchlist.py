"""
watchlist.py

Handles user's stock watchlist.
"""

from core.database import Database
from core.market import StockMarket
from core.utils import (
    print_header,
    print_table_header,
    print_table_row,
    get_non_empty_input,
    success,
    error,
    confirm_action,
    format_currency
)


class WatchlistManager:
    """
    Handles watchlist operations.
    """

    def __init__(self):
        self.database = Database()
        self.market = StockMarket()


    # ==============================
    # Database Methods
    # ==============================

    def load_watchlists(self):
        """
        Load all watchlists.
        """

        return self.database.get_watchlists()


    def save_watchlists(self, data):
        """
        Save watchlists into JSON.
        """

        self.database.save_watchlists(data)


    def get_user_watchlist(self, username):
        """
        Get a specific user's watchlist.
        """

        watchlists = self.load_watchlists()

        return watchlists.get(
            username,
            []
        )


    # ==============================
    # Add Stock
    # ==============================

    def add_stock(self, username):
        """
        Add stock to watchlist.
        """

        print_header("ADD TO WATCHLIST")


        symbol = (
            get_non_empty_input(
                "Enter stock symbol: "
            )
            .upper()
        )


        if not self.market.stock_exists(symbol):
            error("Stock does not exist.")
            return


        watchlists = self.load_watchlists()


        if username not in watchlists:
            watchlists[username] = []


        if symbol in watchlists[username]:
            error("Stock already exists in watchlist.")
            return


        if not confirm_action(
            f"Add {symbol} to watchlist?"
        ):
            return


        watchlists[username].append(symbol)


        self.save_watchlists(watchlists)


        success(
            f"{symbol} added to watchlist."
        )


    # ==============================
    # Remove Stock
    # ==============================

    def remove_stock(self, username):
        """
        Remove stock from watchlist.
        """

        print_header(
            "REMOVE FROM WATCHLIST"
        )


        watchlist = self.get_user_watchlist(
            username
        )


        if not watchlist:
            error("Your watchlist is empty.")
            return


        self.view_watchlist(username)


        symbol = (
            get_non_empty_input(
                "\nEnter stock to remove: "
            )
            .upper()
        )


        if symbol not in watchlist:
            error("Stock not found in watchlist.")
            return


        if not confirm_action(
            f"Remove {symbol}?"
        ):
            return


        watchlists = self.load_watchlists()


        watchlists[username].remove(symbol)


        self.save_watchlists(watchlists)


        success(
            f"{symbol} removed from watchlist."
        )


    # ==============================
    # View Watchlist
    # ==============================

    def view_watchlist(self, username):
        """
        Display all watched stocks.
        """

        print_header("MY WATCHLIST")


        watchlist = self.get_user_watchlist(
            username
        )


        if not watchlist:
            error("Watchlist is empty.")
            return


        headers = [
            "Symbol",
            "Company",
            "Current Price",
            "Movement"
        ]


        print_table_header(headers)


        for symbol in watchlist:

            stock = self.market.get_stock(
                symbol
            )


            if stock:

                status = stock.get_status()


                movement = (
                    f"{status['direction']} "
                    f"{status['percentage']}%"
                )


                print_table_row([
                    stock.symbol,
                    stock.company_name,
                    format_currency(
                        stock.current_price
                    ),
                    movement
                ])


    # ==============================
    # Extra Features
    # ==============================

    def clear_watchlist(self, username):
        """
        Remove all stocks from watchlist.
        """

        print_header(
            "CLEAR WATCHLIST"
        )


        watchlist = self.get_user_watchlist(
            username
        )


        if not watchlist:
            error("Watchlist already empty.")
            return


        if not confirm_action(
            "Delete all watchlist stocks?"
        ):
            return


        watchlists = self.load_watchlists()


        watchlists[username] = []


        self.save_watchlists(
            watchlists
        )


        success(
            "Watchlist cleared successfully."
        )


    def watchlist_count(self, username):
        """
        Returns number of stocks in watchlist.
        """

        return len(
            self.get_user_watchlist(
                username
            )
        )