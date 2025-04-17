import json
import pandas as pd
import requests


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

    return f"Total coins owned: {total_coins}"


def calculate_new_total_coins(coin):
    filename = f"data/{coin}_buys.xlsx"
    df = pd.read_excel(filename)
    coins = df["Coins"].sum()
    return coins


def calculate_new_average(coin):
    filename = f"data/{coin}_buys.xlsx"
    df = pd.read_excel(filename)
    new_average = df["Price"].mean()

    return f"Average price for new {coin} bought: {new_average}"


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


def calulate_profit(coin):
    coins = calculate_new_total_coins(coin)
    cost = calculate_costs(coin)
    current_price = get_current_price(coin)

    current_value = coins * current_price
    profit = round((current_value - cost),2)
    percentage = round((profit/cost*100),2)
    return f'{profit} Dollars, {percentage}%'