"""
portfolio.py

Handles buying, selling,
and portfolio analysis.
"""

from core.database import Database
from core.wallet import WalletManager
from core.market import StockMarket
from models.user import User
from models.transaction import Transaction
from core.utils import (
    print_header,
    print_table_header,
    print_table_row,
    get_non_empty_input,
    get_integer,
    format_currency,
    success,
    error,
    confirm_action
)


class PortfolioManager:
    """
    Handles all portfolio operations.
    """

    def __init__(self):

        self.database = Database()
        self.wallet = WalletManager()
        self.market = StockMarket()


    # ==============================
    # Database Methods
    # ==============================

    def load_users(self):

        users_data = self.database.get_users()

        users = {}

        for username, data in users_data.items():

            users[username] = User.from_dict(
                username,
                data
            )

        return users


    def save_users(self, users):

        data = {}

        for username, user in users.items():

            data[username] = user.to_dict()

        self.database.save_users(data)


    def save_transaction(self, transaction):

        transactions = (
            self.database.get_transactions()
        )

        transactions.append(
            transaction.to_dict()
        )

        self.database.save_transactions(
            transactions
        )


    # ==============================
    # Buying Stocks
    # ==============================

    def buy_stock(self, user):

        print_header("BUY STOCK")

        self.market.display_market()

        symbol = (
            get_non_empty_input(
                "\nEnter stock symbol: "
            )
            .upper()
        )

        stock = self.market.get_stock(symbol)

        if not stock:
            error("Stock does not exist.")
            return


        quantity = get_integer(
            "Enter quantity: ",
            minimum=1
        )


        total_cost = (
            stock.current_price *
            quantity
        )


        print(
            f"\nTotal Investment: "
            f"{format_currency(total_cost)}"
        )


        if total_cost > user.wallet:

            error(
                "Insufficient wallet balance."
            )

            return


        if not confirm_action(
            "Confirm purchase?"
        ):
            return


        # Deduct money
        self.wallet.deduct_investment(
            user,
            total_cost
        )


        # Update portfolio
        users = self.load_users()

        users[user.username].add_stock(
            symbol,
            quantity,
            stock.current_price
        )

        self.save_users(users)


        # Update current session object
        user.add_stock(
            symbol,
            quantity,
            stock.current_price
        )


        # Create transaction
        transaction = Transaction(
            username=user.username,
            transaction_type="BUY",
            stock_symbol=symbol,
            quantity=quantity,
            price=stock.current_price
        )


        self.save_transaction(
            transaction
        )


        success(
            f"Successfully purchased "
            f"{quantity} shares of {symbol}"
        )


    # ==============================
    # Selling Stocks
    # ==============================

    def sell_stock(self, user):

        print_header("SELL STOCK")


        if not user.portfolio:

            error("Portfolio is empty.")
            return


        self.view_portfolio(user)


        symbol = (
            get_non_empty_input(
                "\nEnter stock to sell: "
            )
            .upper()
        )


        stock_data = (
            user.get_stock_details(symbol)
        )


        if not stock_data:

            error("You do not own this stock.")
            return


        owned_quantity = (
            stock_data["quantity"]
        )


        quantity = get_integer(
            "Enter quantity to sell: ",
            minimum=1,
            maximum=owned_quantity
        )


        current_price = (
            self.market.get_price(symbol)
        )


        selling_amount = (
            current_price * quantity
        )


        investment_cost = (
            stock_data["average_price"]
            * quantity
        )


        profit_loss = (
            selling_amount
            - investment_cost
        )


        print("\nSale Summary")
        print("-" * 30)

        print(
            "Selling Value:",
            format_currency(selling_amount)
        )

        print(
            "Profit/Loss:",
            format_currency(profit_loss)
        )


        if not confirm_action(
            "Confirm selling?"
        ):
            return


        # Add money back
        self.wallet.add_profit(
            user,
            selling_amount
        )


        # Update database user
        users = self.load_users()

        users[user.username].remove_stock(
            symbol,
            quantity
        )

        self.save_users(users)


        # Update current session
        user.remove_stock(
            symbol,
            quantity
        )


        transaction = Transaction(
            username=user.username,
            transaction_type="SELL",
            stock_symbol=symbol,
            quantity=quantity,
            price=current_price,
            profit_loss=profit_loss
        )


        self.save_transaction(transaction)


        success(
            f"Sold {quantity} shares of {symbol}"
        )


    # ==============================
    # Portfolio Analytics
    # ==============================

    def view_portfolio(self, user):

        print_header("MY PORTFOLIO")


        if not user.portfolio:

            error("No investments found.")
            return


        headers = [
            "Stock",
            "Qty",
            "Avg Price",
            "Current",
            "P/L"
        ]

        print_table_header(headers)


        total_investment = 0
        current_value = 0


        for symbol, data in (
            user.portfolio.items()
        ):

            quantity = data["quantity"]

            buy_price = (
                data["average_price"]
            )


            market_price = (
                self.market.get_price(symbol)
            )


            invested = (
                buy_price * quantity
            )


            value = (
                market_price * quantity
            )


            profit = value - invested


            total_investment += invested
            current_value += value


            print_table_row([
                symbol,
                quantity,
                format_currency(buy_price),
                format_currency(
                    market_price
                ),
                format_currency(profit)
            ])


        total_profit = (
            current_value
            - total_investment
        )


        print("\n" + "=" * 70)

        print(
            "Total Investment:",
            format_currency(
                total_investment
            )
        )

        print(
            "Current Value:",
            format_currency(
                current_value
            )
        )

        print(
            "Overall Profit/Loss:",
            format_currency(
                total_profit
            )
        )