from datetime import datetime
import json
from matplotlib.dates import relativedelta
import pandas as pd
import requests
from utils.utils import git_pull


def get_loan_amount(loan):
    start_date = datetime.strptime(loan["start"], "%Y-%m-%d")
    today = datetime.today()

    delta = relativedelta(today, start_date)
    months_paid = delta.years * 12 + delta.months

    monthly_rate = loan["rate"] / 12 / 100
    balance = loan["principal"]

    for _ in range(months_paid):
        interest = balance * monthly_rate
        principal_payment = loan["payment"] - interest
        balance -= principal_payment
        if balance <= 0:
            balance = 0.0
            break

    return round(balance, 2)


def calculate_total_average(coin):
    with open("data/average.json") as f:
        data = json.load(f)[coin]
        old_coins = data["coins"]
        old_average_price = data["avergae_buy_price"]

    filename = f"data/{coin}_buys.xlsx"
    df = pd.read_excel(filename)

    new_coins = df["Coins"].sum()
    new_price = df["Price"].mean()

    weighted_avg = ((old_average_price * old_coins) + (new_price * new_coins)) / (
        old_coins + new_coins
    )

    return f"New Average Price: {weighted_avg}"


def calculate_total_coins_owned(coin):
    with open("data/average.json") as f:
        data = json.load(f)[coin]
        old_coins = data["coins"]

    filename = f"data/{coin}_buys.xlsx"
    df = pd.read_excel(filename)

    new_coins = df["Coins"].sum()

    total_coins = old_coins + new_coins

    return total_coins


def calculate_new_total_coins(coin):
    filename = f"data/{coin}_buys.xlsx"
    df = pd.read_excel(filename)
    coins = df["Coins"].sum()
    return float(coins)


def calculate_new_average(coin):
    filename = f"data/{coin}_buys.xlsx"
    df = pd.read_excel(filename)
    new_average = df["Price"].mean()

    return new_average


def get_current_price(coin):
    headers = {"Accept": "application/json"}

    url, pair = (
        ("https://api.kraken.com/0/public/Ticker?pair=KASUSD", "KASUSD")
        if coin == "kaspa"
        else ("https://api.kraken.com/0/public/Ticker?pair=BTCUSD", "XXBTZUSD")
    )

    last_price = requests.request("GET", url, headers=headers).json()["result"][pair][
        "c"
    ][0]
    # if coin == "kaspa":
    #     return .125
    return float(last_price)


def calculate_costs(coin):
    filename = f"data/{coin}_buys.xlsx"
    df = pd.read_excel(filename)
    total_cost = df["Cost"].sum()
    return total_cost


def calcululate_current_value_new_coins(coin):
    coins = calculate_new_total_coins(coin)
    current_price = get_current_price(coin)

    current_value = coins * current_price
    return current_value


def calulate_profit(coin):
    coins = calculate_new_total_coins(coin)
    cost = calculate_costs(coin)
    current_price = get_current_price(coin)

    current_value = coins * current_price
    profit = round((current_value - cost), 2)
    percentage = round((profit / cost * 100), 2)
    return profit, percentage


def calculate_total_profit(coin):
    with open("data/average.json") as f:
        data = json.load(f)[coin]
        old_coins = data["coins"]
        old_average_price = data["avergae_buy_price"]
    cost_basis = (calculate_costs(coin)) + (old_coins * old_average_price)
    market_value = (old_coins + calculate_new_total_coins(coin)) * get_current_price(
        coin
    )
    total_profit = round(market_value - cost_basis, 2)
    percentage = round((total_profit / cost_basis) * 100, 2)
    return total_profit, percentage


def calculate_allocation_percentage():
    kaspa_coins = calculate_total_coins_owned("kaspa")
    bitcoin_coins = calculate_total_coins_owned("bitcoin")

    kaspa_market_value = kaspa_coins * get_current_price("kaspa")
    bitcoin_market_value = bitcoin_coins * get_current_price("bitcoin")
    total_market_value = kaspa_market_value + bitcoin_market_value

    kaspa_allocation = kaspa_market_value / total_market_value
    bitcoin_allocation = 1 - kaspa_allocation

    return {
        "kaspa": kaspa_allocation,
        "bitcoin": bitcoin_allocation,
    }


def calculate_portfolio_minus_loan():
    kaspa_coins = calculate_total_coins_owned("kaspa")
    bitcoin_coins = calculate_total_coins_owned("bitcoin")

    kaspa_market_value = kaspa_coins * get_current_price("kaspa")
    bitcoin_market_value = bitcoin_coins * get_current_price("bitcoin")
    total_market_value = kaspa_market_value + bitcoin_market_value

    return {"total": total_market_value, "net": total_market_value}


def calculate_combined_total_profit():
    """
    Calculate combined total profit from both Bitcoin and Kaspa.
    Returns tuple: (total_profit_usd, weighted_percentage)
    """
    btc_profit, btc_percentage = calculate_total_profit("bitcoin")
    kaspa_profit, kaspa_percentage = calculate_total_profit("kaspa")

    total_profit = btc_profit + kaspa_profit

    with open("data/average.json") as f:
        data = json.load(f)
        btc_old_coins = data["bitcoin"]["coins"]
        btc_old_avg_price = data["bitcoin"]["avergae_buy_price"]
        kaspa_old_coins = data["kaspa"]["coins"]
        kaspa_old_avg_price = data["kaspa"]["avergae_buy_price"]

    btc_cost_basis = (calculate_costs("bitcoin")) + (btc_old_coins * btc_old_avg_price)
    kaspa_cost_basis = (calculate_costs("kaspa")) + (
        kaspa_old_coins * kaspa_old_avg_price
    )
    total_cost_basis = btc_cost_basis + kaspa_cost_basis

    weighted_percentage = round((total_profit / total_cost_basis) * 100, 2)

    return total_profit, weighted_percentage


def base_profit():
    git_pull()
    print(
        f"Kaspa Price: ${get_current_price('kaspa')} Bitcoin Price: ${get_current_price('bitcoin')}"
    )
    print(f'Kaspa {calulate_profit("kaspa")[0]} USD, {calulate_profit("kaspa")[1]}%')
    print(
        f'Kaspa Total {calculate_total_profit("kaspa")[0]} USD, {calculate_total_profit("kaspa")[1]}%'
    )
    print(
        f'Bitcoin {calulate_profit("bitcoin")[0]} USD, {calulate_profit("bitcoin")[1]}%'
    )

    portfolio = calculate_portfolio_minus_loan()
    print(f'Total Portfolio Net Worth: {round(portfolio["total"],2)}')

    allocation = calculate_allocation_percentage()
    print(
        f"Portfolio Allocation: "
        f'Kaspa: {round(allocation["kaspa"]*100, 2)}%, '
        f'Bitcoin: {round(allocation["bitcoin"]*100, 2)}%'
    )


if __name__ == "__main__":
    base_profit()
