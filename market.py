"""
market.py

Handles stock market operations.
"""

import random

from core.database import Database
from models.stock import Stock
from core.utils import (
    print_header,
    print_table_header,
    print_table_row,
    success,
    error,
    get_non_empty_input,
    get_float,
    confirm_action,
    format_currency
)


class StockMarket:
    """
    Handles all stock market operations.
    """

    def __init__(self):
        self.database = Database()
        self.stocks = self.load_market()


    # ==========================
    # Database Operations
    # ==========================

    def load_market(self):
        """
        Load stocks from database.
        """

        market_data = self.database.get_market()

        stocks = {}

        for symbol, data in market_data.items():

            stocks[symbol] = Stock.from_dict(
                symbol,
                data
            )

        return stocks


    def save_market(self):
        """
        Save all stock objects to JSON.
        """

        data = {}

        for symbol, stock in self.stocks.items():

            data[symbol] = stock.to_dict()

        self.database.save_market(data)


    # ==========================
    # Display Operations
    # ==========================

    def display_market(self):
        """
        Display all available stocks.
        """

        print_header("LIVE STOCK MARKET")

        headers = [
            "Symbol",
            "Company",
            "Price",
            "Movement"
        ]

        print_table_header(headers)

        for stock in self.stocks.values():

            status = stock.get_status()

            movement = (
                f"{status['direction']} "
                f"{status['percentage']}%"
            )

            print_table_row([
                stock.symbol,
                stock.company_name,
                format_currency(stock.current_price),
                movement
            ])


    def search_stock(self):
        """
        Search a stock.
        """

        print_header("SEARCH STOCK")

        keyword = (
            get_non_empty_input(
                "Enter stock symbol or name: "
            ).lower()
        )

        found = False

        for stock in self.stocks.values():

            if (
                keyword in stock.symbol.lower()
                or
                keyword in stock.company_name.lower()
            ):

                print("\nStock Found:")
                print(stock.display())

                found = True


        if not found:
            error("Stock not found.")


    def view_stock_history(self):
        """
        Show stock price history.
        """

        symbol = (
            get_non_empty_input(
                "Enter stock symbol: "
            )
            .upper()
        )

        stock = self.stocks.get(symbol)

        if stock:
            stock.show_history()
        else:
            error("Stock does not exist.")


    # ==========================
    # Market Simulation
    # ==========================

    def refresh_market(self):
        """
        Simulate market changes.
        Prices change randomly between
        -5% and +5%.
        """

        print_header(
            "MARKET REFRESH"
        )

        for stock in self.stocks.values():

            change = random.uniform(
                -5,
                5
            )

            new_price = (
                stock.current_price *
                (1 + change / 100)
            )

            stock.update_price(
                round(new_price, 2)
            )

            status = stock.get_status()

            print(
                f"{stock.symbol:<12}"
                f"{status['direction']} "
                f"{status['percentage']}%"
            )

        self.save_market()

        success(
            "Market prices updated successfully."
        )


    # ==========================
    # Admin Operations
    # ==========================

    def add_stock(self):
        """
        Add a new stock to market.
        """

        print_header("ADD NEW STOCK")

        symbol = (
            get_non_empty_input(
                "Stock Symbol: "
            )
            .upper()
        )

        if symbol in self.stocks:
            error("Stock already exists.")
            return


        company = get_non_empty_input(
            "Company Name: "
        )

        price = get_float(
            "Starting Price: ₹",
            minimum=1
        )


        if not confirm_action(
            "Add this stock to market?"
        ):
            return


        self.stocks[symbol] = Stock(
            symbol,
            company,
            price
        )

        self.save_market()

        success(
            "Stock added successfully."
        )


    def remove_stock(self):
        """
        Remove a stock from market.
        """

        print_header(
            "REMOVE STOCK"
        )

        symbol = (
            get_non_empty_input(
                "Enter stock symbol: "
            )
            .upper()
        )

        if symbol not in self.stocks:
            error("Stock not found.")
            return


        if confirm_action(
            f"Delete {symbol}?"
        ):

            del self.stocks[symbol]

            self.save_market()

            success(
                "Stock removed successfully."
            )


    def update_stock_price(self):
        """
        Update stock price manually.
        """

        print_header(
            "UPDATE STOCK PRICE"
        )

        symbol = (
            get_non_empty_input(
                "Stock Symbol: "
            )
            .upper()
        )

        stock = self.stocks.get(symbol)

        if not stock:
            error("Stock does not exist.")
            return


        print(
            "Current Price:",
            format_currency(
                stock.current_price
            )
        )


        new_price = get_float(
            "New Price: ₹",
            minimum=1
        )


        stock.update_price(
            new_price
        )

        self.save_market()

        success(
            "Stock price updated."
        )


    # ==========================
    # Helper Methods
    # ==========================

    def stock_exists(self, symbol):
        """
        Check whether stock exists.
        """

        return (
            symbol.upper()
            in self.stocks
        )


    def get_stock(self, symbol):
        """
        Return stock object.
        """

        return self.stocks.get(
            symbol.upper()
        )


    def get_price(self, symbol):
        """
        Return current stock price.
        """

        stock = self.get_stock(symbol)

        if stock:
            return stock.current_price

        return None