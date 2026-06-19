import json
import os
import random

DATA_DIR = "data"

USERS_FILE = f"{DATA_DIR}/users.json"
MARKET_FILE = f"{DATA_DIR}/market.json"


# =========================
# INIT FILES (AUTO CREATE)
# =========================
def init():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(USERS_FILE):
        json.dump({}, open(USERS_FILE, "w"))

    if not os.path.exists(MARKET_FILE):
        market = {
            "TCS": {"name": "Tata Consultancy Services", "price": 3500},
            "INFY": {"name": "Infosys", "price": 1600},
            "WIPRO": {"name": "Wipro", "price": 450},
            "RELIANCE": {"name": "Reliance Industries", "price": 2500}
        }
        json.dump(market, open(MARKET_FILE, "w"), indent=4)


# =========================
# LOAD / SAVE
# =========================
def load(file):
    return json.load(open(file, "r"))

def save(file, data):
    json.dump(data, open(file, "w"), indent=4)


# =========================
# MARKET SIMULATION
# =========================
def market_update():
    market = load(MARKET_FILE)

    for s in market:
        change = random.randint(-120, 150)
        market[s]["price"] = max(100, market[s]["price"] + change)

    save(MARKET_FILE, market)
    return market


# =========================
# REGISTER
# =========================
def register():
    users = load(USERS_FILE)

    u = input("Username: ")
    p = input("Password: ")

    if u in users:
        print("User already exists!")
        return None

    users[u] = {
        "password": p,
        "wallet": 50000,
        "portfolio": {}
    }

    save(USERS_FILE, users)
    print("✓ Account created successfully!")
    return u


# =========================
# LOGIN
# =========================
def login():
    users = load(USERS_FILE)

    u = input("Username: ")
    p = input("Password: ")

    if u in users and users[u]["password"] == p:
        print("✓ Login successful!")
        return u

    print("Invalid credentials")
    return None


# =========================
# MARKET DISPLAY
# =========================
def show_market():
    market = market_update()

    print("\n===== MARKET =====")
    for k, v in market.items():
        print(f"{k} | {v['name']} | ₹{v['price']}")


# =========================
# BUY STOCK
# =========================
def buy(user):
    users = load(USERS_FILE)
    market = market_update()

    stock = input("Stock symbol: ").upper()

    if stock not in market:
        print("Stock not found")
        return

    qty = int(input("Quantity: "))

    price = market[stock]["price"]
    total = price * qty

    if users[user]["wallet"] < total:
        print("Insufficient balance")
        return

    users[user]["wallet"] -= total

    if stock in users[user]["portfolio"]:
        users[user]["portfolio"][stock]["qty"] += qty
    else:
        users[user]["portfolio"][stock] = {
            "qty": qty,
            "buy_price": price
        }

    save(USERS_FILE, users)

    print(f"✓ Bought {qty} {stock} for ₹{total}")


# =========================
# SELL STOCK
# =========================
def sell(user):
    users = load(USERS_FILE)
    market = market_update()

    p = users[user]["portfolio"]

    stock = input("Stock: ").upper()

    if stock not in p:
        print("Not owned")
        return

    qty = int(input("Quantity: "))

    if qty > p[stock]["qty"]:
        print("Not enough shares")
        return

    price = market[stock]["price"]
    buy_price = p[stock]["buy_price"]

    profit = (price - buy_price) * qty
    earning = price * qty

    users[user]["wallet"] += earning

    p[stock]["qty"] -= qty
    if p[stock]["qty"] == 0:
        del p[stock]

    save(USERS_FILE, users)

    sign = "+" if profit >= 0 else ""

    print(f"✓ Sold {qty} {stock}")
    print(f"Profit / Loss: {sign}₹{profit}")


# =========================
# PORTFOLIO
# =========================
def portfolio(user):
    users = load(USERS_FILE)
    market = market_update()

    p = users[user]["portfolio"]

    print("\n===== PORTFOLIO =====")

    total_buy = 0
    total_now = 0

    for s, d in p.items():
        qty = d["qty"]
        buy = d["buy_price"]
        now = market[s]["price"]

        invested = qty * buy
        current = qty * now

        total_buy += invested
        total_now += current

        pl = current - invested
        sign = "+" if pl >= 0 else ""

        print(f"{s} | Qty:{qty} | Buy:{buy} | Now:{now} | P/L:{sign}{pl}")

    total_pl = total_now - total_buy
    sign = "+" if total_pl >= 0 else ""

    print("\n-----------------------------")
    print(f"TOTAL INVESTED : ₹{total_buy}")
    print(f"CURRENT VALUE  : ₹{total_now}")
    print(f"PROFIT / LOSS  : {sign}₹{total_pl}")


# =========================
# MAIN PROGRAM
# =========================
def main():
    init()

    print("=== STOCK PORTFOLIO SYSTEM ===")

    user = None

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")

        ch = input("Choose: ")

        if ch == "1":
            user = register()

        elif ch == "2":
            user = login()

        elif ch == "3":
            break

        if user:
            while True:
                print("\n1. Market")
                print("2. Buy")
                print("3. Sell")
                print("4. Portfolio")
                print("5. Logout")

                c = input("Choose: ")

                if c == "1":
                    show_market()
                elif c == "2":
                    buy(user)
                elif c == "3":
                    sell(user)
                elif c == "4":
                    portfolio(user)
                elif c == "5":
                    print("\n===================================")
                    print(" THANK YOU FOR USING THE SYSTEM ")
                    print(" HAPPY INVESTING 📈💰 ")
                    print("===================================")
                    break


if __name__ == "__main__":
    main()