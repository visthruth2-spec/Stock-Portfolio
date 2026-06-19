"""
transaction.py

Contains Transaction class for storing
stock trading records.
"""

import uuid
from datetime import datetime


class Transaction:
    """
    Represents a single stock transaction.
    """

    def __init__(
        self,
        username,
        transaction_type,
        stock_symbol,
        quantity,
        price,
        transaction_id=None,
        date_time=None,
        profit_loss=0
    ):
        """
        Initialize transaction object.
        """

        self.transaction_id = (
            transaction_id
            if transaction_id
            else self.generate_id()
        )

        self.username = username

        self.transaction_type = (
            transaction_type.upper()
        )

        self.stock_symbol = (
            stock_symbol.upper()
        )

        self.quantity = int(quantity)

        self.price = float(price)

        self.total_amount = (
            self.quantity * self.price
        )

        self.profit_loss = float(profit_loss)

        self.date_time = (
            date_time
            if date_time
            else self.current_time()
        )

    # ====================================
    # Helper Methods
    # ====================================

    def generate_id(self):
        """
        Generate a short unique transaction ID.
        """

        return (
            "TXN-" +
            str(uuid.uuid4())[:8].upper()
        )

    def current_time(self):
        """
        Returns current date and time.
        """

        return datetime.now().strftime(
            "%d/%m/%Y %I:%M:%S %p"
        )

    # ====================================
    # Display Methods
    # ====================================

    def display(self):
        """
        Returns formatted transaction details.
        """

        output = (
            f"Transaction ID : {self.transaction_id}\n"
            f"User           : {self.username}\n"
            f"Type           : {self.transaction_type}\n"
            f"Stock          : {self.stock_symbol}\n"
            f"Quantity       : {self.quantity}\n"
            f"Price          : ₹{self.price:.2f}\n"
            f"Total Amount   : ₹{self.total_amount:.2f}\n"
            f"Date & Time    : {self.date_time}"
        )

        if self.transaction_type == "SELL":

            if self.profit_loss >= 0:
                output += (
                    f"\nProfit         : "
                    f"₹{self.profit_loss:.2f}"
                )

            else:
                output += (
                    f"\nLoss           : "
                    f"₹{abs(self.profit_loss):.2f}"
                )

        return output


    # ====================================
    # JSON Conversion Methods
    # ====================================

    def to_dict(self):
        """
        Converts transaction object
        into dictionary.
        """

        return {

            "transaction_id": self.transaction_id,

            "username": self.username,

            "type": self.transaction_type,

            "stock_symbol": self.stock_symbol,

            "quantity": self.quantity,

            "price": self.price,

            "total_amount": self.total_amount,

            "profit_loss": self.profit_loss,

            "date_time": self.date_time
        }


    @classmethod
    def from_dict(cls, data):
        """
        Creates Transaction object
        from stored JSON data.
        """

        return cls(
            username=data["username"],

            transaction_type=data["type"],

            stock_symbol=data["stock_symbol"],

            quantity=data["quantity"],

            price=data["price"],

            transaction_id=data["transaction_id"],

            date_time=data["date_time"],

            profit_loss=data.get(
                "profit_loss",
                0
            )
        )