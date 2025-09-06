from datetime import datetime
import json
from matplotlib.dates import relativedelta
import pandas as pd
import requests
from data.loan_data import loan_one, loan_two
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
    profit = round((current_value - cost),2)
    percentage = round((profit/cost*100),2)
    return f'Profit: ${profit}, ({percentage}%) --{coin} Price: ${round(current_price,5)}'

def calculate_total_profit(coin):
    with open("data/average.json") as f:
        data = json.load(f)[coin]
        old_coins = data["coins"]
        old_average_price = data["avergae_buy_price"]
    cost_basis = (calculate_costs(coin)) + (old_coins*old_average_price)
    market_value = (old_coins + calculate_new_total_coins(coin))*get_current_price(coin)
    total_profit = market_value - cost_basis
    percentage = round((total_profit / cost_basis) * 100, 2)
    return f"Total profit: ${round(total_profit, 2)}, ({percentage}%) --{coin}"

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
    loans = get_loan_amount(loan_two) 

    kaspa_market_value = kaspa_coins * get_current_price("kaspa")
    bitcoin_market_value = bitcoin_coins * get_current_price("bitcoin")
    total_market_value = kaspa_market_value + bitcoin_market_value

    return {
        "total": total_market_value,
        "loans": loans,
        "net": total_market_value - loans,
    }

def base_profit():
    git_pull()
    print(calulate_profit("kaspa"))
    print(calculate_total_profit("kaspa"))
    print(calulate_profit("bitcoin"))
    print(calculate_total_profit("bitcoin"))

    portfolio = calculate_portfolio_minus_loan()
    print(f'Total Portfolio Net Worth: {round(portfolio["total"],2)} - {portfolio["loans"]} = {round(portfolio["net"],2)}')

    allocation = calculate_allocation_percentage()
    print(
        f'Portfolio Allocation: '
        f'Kaspa: {round(allocation["kaspa"]*100, 2)}%, '
        f'Bitcoin: {round(allocation["bitcoin"]*100, 2)}%'
    )

if __name__ == "__main__":
    base_profit()