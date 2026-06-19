"""
stock.py

Contains the Stock class for handling
stock market information.
"""

from datetime import datetime


class Stock:
    """
    Represents a stock in the market.
    """

    def __init__(
        self,
        symbol,
        company_name,
        price,
        price_history=None
    ):
        """
        Initialize stock object.
        """

        self.symbol = symbol.upper()
        self.company_name = company_name

        self.current_price = float(price)

        # Stores previous price to calculate movement
        self.previous_price = float(price)

        # Store price history
        if price_history is None:
            self.price_history = [
                {
                    "date": self.current_time(),
                    "price": self.current_price
                }
            ]
        else:
            self.price_history = price_history

    # ==================================
    # Helper Methods
    # ==================================

    def current_time(self):
        """
        Returns current date and time.
        """

        return datetime.now().strftime(
            "%d/%m/%Y %I:%M %p"
        )

    # ==================================
    # Price Operations
    # ==================================

    def update_price(self, new_price):
        """
        Updates stock price and stores history.
        """

        if new_price <= 0:
            return False

        self.previous_price = self.current_price

        self.current_price = float(new_price)

        self.price_history.append(
            {
                "date": self.current_time(),
                "price": self.current_price
            }
        )

        return True

    def get_price_change(self):
        """
        Returns the price difference.
        """

        return (
            self.current_price -
            self.previous_price
        )

    def get_percentage_change(self):
        """
        Returns percentage increase or decrease.
        """

        if self.previous_price == 0:
            return 0

        change = (
            (self.current_price - self.previous_price)
            / self.previous_price
        ) * 100

        return round(change, 2)

    def get_movement_symbol(self):
        """
        Returns market movement indicator.
        """

        change = self.get_price_change()

        if change > 0:
            return "▲"

        if change < 0:
            return "▼"

        return "-"

    def get_status(self):
        """
        Returns stock movement information.
        """

        return {
            "change": round(
                self.get_price_change(),
                2
            ),
            "percentage": self.get_percentage_change(),
            "direction": self.get_movement_symbol()
        }

    # ==================================
    # Display Methods
    # ==================================

    def display(self):
        """
        Returns formatted stock details.
        """

        status = self.get_status()

        return (
            f"{self.symbol:<10}"
            f"{self.company_name:<30}"
            f"₹{self.current_price:<12.2f}"
            f"{status['direction']} "
            f"{status['percentage']}%"
        )

    def show_history(self):
        """
        Displays stock price history.
        """

        print("\n==========================================")
        print(f"PRICE HISTORY - {self.symbol}")
        print("==========================================")

        for record in self.price_history:

            print(
                f"{record['date']} | "
                f"₹{record['price']:.2f}"
            )

    # ==================================
    # JSON Conversion Methods
    # ==================================

    def to_dict(self):
        """
        Converts Stock object into dictionary
        for JSON storage.
        """

        return {
            "company_name": self.company_name,
            "price": self.current_price,
            "price_history": self.price_history
        }

    @classmethod
    def from_dict(
        cls,
        symbol,
        data
    ):
        """
        Creates Stock object from JSON data.
        """

        return cls(
            symbol=symbol,
            company_name=data["company_name"],
            price=data["price"],
            price_history=data.get(
                "price_history",
                []
            )
        )