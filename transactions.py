"""
transactions.py

Handles transaction history and reports.
"""

from models.transaction import Transaction
from core.database import Database
from core.utils import (
    print_header,
    print_table_header,
    print_table_row,
    get_non_empty_input,
    format_currency,
    error
)


class TransactionManager:
    """
    Handles transaction records.
    """

    def __init__(self):
        self.database = Database()

    # =================================
    # Database Operations
    # =================================

    def load_transactions(self):
        """
        Load transactions from JSON database.
        """

        transaction_data = (
            self.database.get_transactions()
        )

        transactions = []

        for data in transaction_data:
            transactions.append(
                Transaction.from_dict(data)
            )

        return transactions


    def get_user_transactions(self, username):
        """
        Return transactions of a specific user.
        """

        transactions = self.load_transactions()

        return [
            transaction
            for transaction in transactions
            if transaction.username == username
        ]


    # =================================
    # Display Functions
    # =================================

    def view_history(self, username):
        """
        Display complete transaction history.
        """

        print_header(
            "TRANSACTION HISTORY"
        )

        transactions = (
            self.get_user_transactions(
                username
            )
        )

        if not transactions:
            error("No transactions found.")
            return


        transactions.sort(
            key=lambda x: x.date_time,
            reverse=True
        )


        headers = [
            "ID",
            "Type",
            "Stock",
            "Qty",
            "Amount",
            "Date"
        ]

        print_table_header(headers)


        for transaction in transactions:

            print_table_row([
                transaction.transaction_id,
                transaction.transaction_type,
                transaction.stock_symbol,
                transaction.quantity,
                format_currency(
                    transaction.total_amount
                ),
                transaction.date_time
            ])


    def filter_transactions(self, username):
        """
        Show BUY or SELL transactions.
        """

        print_header(
            "FILTER TRANSACTIONS"
        )

        choice = (
            get_non_empty_input(
                "Enter BUY or SELL: "
            )
            .upper()
        )


        if choice not in [
            "BUY",
            "SELL"
        ]:
            error("Invalid option.")
            return


        transactions = (
            self.get_user_transactions(
                username
            )
        )


        filtered = [
            transaction
            for transaction in transactions
            if transaction.transaction_type == choice
        ]


        if not filtered:
            error(
                f"No {choice} transactions found."
            )
            return


        for transaction in filtered:

            print("\n" + "=" * 50)

            print(
                transaction.display()
            )


    def search_stock_transactions(
        self,
        username
    ):
        """
        Search transactions by stock symbol.
        """

        print_header(
            "SEARCH TRANSACTIONS"
        )


        symbol = (
            get_non_empty_input(
                "Enter stock symbol: "
            )
            .upper()
        )


        transactions = (
            self.get_user_transactions(
                username
            )
        )


        results = [
            transaction
            for transaction in transactions
            if transaction.stock_symbol == symbol
        ]


        if not results:
            error(
                "No matching transactions found."
            )
            return


        for transaction in results:

            print("\n" + "=" * 50)

            print(
                transaction.display()
            )


    # =================================
    # Profit/Loss Reports
    # =================================

    def realized_profit_report(
        self,
        username
    ):
        """
        Calculate profit or loss from sold stocks.
        """

        print_header(
            "REALIZED PROFIT REPORT"
        )


        transactions = (
            self.get_user_transactions(
                username
            )
        )


        total_profit = 0


        for transaction in transactions:

            if (
                transaction.transaction_type
                == "SELL"
            ):

                total_profit += (
                    transaction.profit_loss
                )


        print(
            "Total Realized Profit/Loss:",
            format_currency(total_profit)
        )


        if total_profit > 0:

            print(
                "Status: PROFIT"
            )

        elif total_profit < 0:

            print(
                "Status: LOSS"
            )

        else:

            print(
                "Status: BREAK EVEN"
            )


    # =================================
    # Advanced Analysis
    # =================================

    def transaction_summary(
        self,
        username
    ):
        """
        Displays overall trading summary.
        """

        print_header(
            "TRADING SUMMARY"
        )


        transactions = (
            self.get_user_transactions(
                username
            )
        )


        if not transactions:
            error("No records found.")
            return


        total_buy = 0
        total_sell = 0
        buy_count = 0
        sell_count = 0


        for transaction in transactions:

            if (
                transaction.transaction_type
                == "BUY"
            ):

                buy_count += 1

                total_buy += (
                    transaction.total_amount
                )

            else:

                sell_count += 1

                total_sell += (
                    transaction.total_amount
                )


        print(
            f"Total Purchases      : {buy_count}"
        )

        print(
            f"Total Sales          : {sell_count}"
        )

        print(
            "Money Invested       :",
            format_currency(total_buy)
        )

        print(
            "Money Received       :",
            format_currency(total_sell)
        )

        print(
            "Net Cash Flow        :",
            format_currency(
                total_sell - total_buy
            )
        )