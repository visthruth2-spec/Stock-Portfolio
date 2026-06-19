"""
reports.py

Handles portfolio analysis and report generation.
"""

from datetime import datetime

from core.market import StockMarket
from core.utils import (
    print_header,
    format_currency,
    success,
    error
)


class ReportManager:
    """
    Handles portfolio reports and analytics.
    """

    def __init__(self):
        self.market = StockMarket()


    # ==================================
    # Calculate Portfolio Statistics
    # ==================================

    def calculate_statistics(self, user):
        """
        Calculate complete portfolio analytics.
        """

        if not user.portfolio:
            return None


        total_investment = 0
        current_value = 0

        best_stock = None
        worst_stock = None

        best_profit = float("-inf")
        worst_profit = float("inf")


        for symbol, data in user.portfolio.items():

            quantity = data["quantity"]

            average_price = data["average_price"]


            current_price = (
                self.market.get_price(symbol)
            )


            invested_amount = (
                quantity * average_price
            )

            current_amount = (
                quantity * current_price
            )


            profit = (
                current_amount -
                invested_amount
            )


            total_investment += invested_amount

            current_value += current_amount


            if profit > best_profit:

                best_profit = profit

                best_stock = symbol


            if profit < worst_profit:

                worst_profit = profit

                worst_stock = symbol


        total_profit = (
            current_value -
            total_investment
        )


        percentage = 0

        if total_investment > 0:

            percentage = (
                total_profit /
                total_investment
            ) * 100


        return {

            "investment": total_investment,

            "current_value": current_value,

            "profit": total_profit,

            "percentage": round(
                percentage,
                2
            ),

            "best_stock": best_stock,

            "worst_stock": worst_stock,

            "best_profit": best_profit,

            "worst_profit": worst_profit
        }


    # ==================================
    # Display Portfolio Report
    # ==================================

    def display_report(self, user):
        """
        Show portfolio performance report.
        """

        print_header(
            "PORTFOLIO ANALYSIS REPORT"
        )


        stats = (
            self.calculate_statistics(user)
        )


        if not stats:

            error(
                "No investments found."
            )

            return


        print(
            "Total Investment      :",
            format_currency(
                stats["investment"]
            )
        )


        print(
            "Current Portfolio Value:",
            format_currency(
                stats["current_value"]
            )
        )


        print(
            "Overall Profit/Loss   :",
            format_currency(
                stats["profit"]
            )
        )


        print(
            "Return Percentage     :",
            f"{stats['percentage']}%"
        )


        print("\nStock Performance")


        print(
            "Best Performing Stock :",
            stats["best_stock"],
            f"({format_currency(stats['best_profit'])})"
        )


        print(
            "Worst Performing Stock:",
            stats["worst_stock"],
            f"({format_currency(stats['worst_profit'])})"
        )


        print(
            "\nRisk Level:",
            self.calculate_risk(user)
        )


        print(
            "Diversification:",
            self.diversification_level(user)
        )


    # ==================================
    # Risk Analysis
    # ==================================

    def calculate_risk(self, user):
        """
        Estimate portfolio risk.
        """

        total_stocks = len(
            user.portfolio
        )


        if total_stocks >= 8:
            return "LOW RISK"

        elif total_stocks >= 4:
            return "MEDIUM RISK"

        return "HIGH RISK"


    # ==================================
    # Diversification Analysis
    # ==================================

    def diversification_level(self, user):
        """
        Analyze diversification.
        """

        count = len(
            user.portfolio
        )


        if count >= 8:
            return "Excellent"

        elif count >= 5:
            return "Good"

        elif count >= 3:
            return "Average"

        return "Poor"


    # ==================================
    # Generate Text Report
    # ==================================

    def generate_report_file(self, user):
        """
        Save portfolio report to text file.
        """

        stats = self.calculate_statistics(user)


        if not stats:

            error(
                "Nothing to generate."
            )

            return


        filename = (
            f"{user.username}_portfolio_report.txt"
        )


        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:


            file.write(
                "=" * 50 + "\n"
            )

            file.write(
                "SMART STOCK PORTFOLIO REPORT\n"
            )

            file.write(
                "=" * 50 + "\n\n"
            )


            file.write(
                f"Generated On: "
                f"{datetime.now()}\n\n"
            )


            file.write(
                f"User: {user.username}\n\n"
            )


            file.write(
                f"Total Investment: "
                f"{format_currency(stats['investment'])}\n"
            )


            file.write(
                f"Current Value: "
                f"{format_currency(stats['current_value'])}\n"
            )


            file.write(
                f"Overall Profit/Loss: "
                f"{format_currency(stats['profit'])}\n"
            )


            file.write(
                f"Return Percentage: "
                f"{stats['percentage']}%\n\n"
            )


            file.write(
                f"Best Stock: "
                f"{stats['best_stock']}\n"
            )


            file.write(
                f"Worst Stock: "
                f"{stats['worst_stock']}\n"
            )


            file.write(
                f"Risk Level: "
                f"{self.calculate_risk(user)}\n"
            )


            file.write(
                "Diversification: "
                f"{self.diversification_level(user)}"
            )


        success(
            f"Report generated successfully:\n{filename}"
        )