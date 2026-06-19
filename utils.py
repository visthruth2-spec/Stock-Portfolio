"""
utils.py

Utility functions for Smart Stock Portfolio System.
"""

import os
from datetime import datetime


# ==============================
# Terminal Utility Functions
# ==============================

def clear_screen():
    """
    Clears terminal screen.
    Works on Windows, Linux, and macOS.
    """

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def pause():
    """
    Stops program until user presses Enter.
    """

    input("\nPress Enter to continue...")


# ==============================
# Display Functions
# ==============================

def print_line(length=60):
    """
    Prints a horizontal line.
    """

    print("=" * length)


def print_header(title):
    """
    Prints a formatted heading.
    """

    print_line()
    print(title.center(60))
    print_line()


def print_message(message):
    """
    Displays a normal message.
    """

    print(f"\n→ {message}")


def success(message):
    """
    Displays success messages.
    """

    print(f"\n✓ SUCCESS: {message}")


def error(message):
    """
    Displays error messages.
    """

    print(f"\n✗ ERROR: {message}")


def warning(message):
    """
    Displays warning messages.
    """

    print(f"\n! WARNING: {message}")


# ==============================
# Input Validation Functions
# ==============================

def get_non_empty_input(message):
    """
    Prevents empty input.
    """

    while True:

        value = input(message).strip()

        if value:
            return value

        error("Input cannot be empty.")


def get_integer(message, minimum=None, maximum=None):
    """
    Gets a valid integer.
    """

    while True:

        try:
            value = int(input(message))

            if minimum is not None and value < minimum:
                error(
                    f"Value must be at least {minimum}."
                )
                continue

            if maximum is not None and value > maximum:
                error(
                    f"Value cannot exceed {maximum}."
                )
                continue

            return value

        except ValueError:
            error("Please enter numbers only.")


def get_float(message, minimum=None):
    """
    Gets a valid decimal number.
    """

    while True:

        try:
            value = float(input(message))

            if minimum is not None and value < minimum:
                error(
                    f"Value must be at least {minimum}."
                )
                continue

            return value

        except ValueError:
            error("Please enter a valid amount.")


def get_menu_choice(start, end):
    """
    Validates menu selections.
    """

    return get_integer(
        "\nEnter your choice: ",
        start,
        end
    )


# ==============================
# Financial Functions
# ==============================

def format_currency(amount):
    """
    Formats money in Indian Rupee style.
    """

    return f"₹{amount:,.2f}"


def calculate_percentage(
    old_value,
    new_value
):
    """
    Calculates percentage change.
    """

    if old_value == 0:
        return 0

    return (
        (new_value - old_value)
        / old_value
    ) * 100


# ==============================
# Date and Time Functions
# ==============================

def get_current_datetime():
    """
    Returns current date and time.
    """

    return datetime.now().strftime(
        "%d/%m/%Y %I:%M:%S %p"
    )


def get_current_date():
    """
    Returns current date.
    """

    return datetime.now().strftime(
        "%d/%m/%Y"
    )


# ==============================
# Confirmation Functions
# ==============================

def confirm_action(message):
    """
    Asks user to confirm an action.
    """

    while True:

        choice = (
            input(
                f"\n{message} (Y/N): "
            )
            .strip()
            .lower()
        )

        if choice == "y":
            return True

        if choice == "n":
            return False

        error(
            "Please enter Y or N only."
        )


# ==============================
# Table Display Functions
# ==============================

def print_table_header(headers):
    """
    Prints table headings.
    """

    print()

    for header in headers:
        print(
            f"{header:<20}",
            end=""
        )

    print()

    print("-" * (20 * len(headers)))


def print_table_row(values):
    """
    Prints a row of table data.
    """

    for value in values:
        print(
            f"{str(value):<20}",
            end=""
        )

    print()