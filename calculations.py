import json
import pandas as pd
import requests


def calculate_total_average(coin):
    with open("average.json") as f:
        data = json.load(f)[coin]
        old_coins = data["coins"]
        old_average_price = data["avergae_buy_price"]

    df = pd.read_csv(f"{coin}_buys.csv")

    new_coins = df["Coins"].sum()
    new_price = df["Price"].mean()

    weighted_avg = ((old_average_price * old_coins) + (new_price * new_coins)) / (
        old_coins + new_coins
    )

    return f"New Average Price: {weighted_avg}"


def calculate_total_coins_owned(coin):
    with open("average.json") as f:
        data = json.load(f)[coin]
        old_coins = data["coins"]

    df = pd.read_csv(f"{coin}_buys.csv")

    new_coins = df["Coins"].sum()

    total_coins = old_coins + new_coins

    print(f"Total coins owned: {total_coins}")


def calulate_new_total_coins(coin):
    df = pd.read_csv(f"{coin}_buys.csv")
    coins = df["Coins"].sum()
    return coins


def calulate_new_average(coin):
    df = pd.read_csv(f"{coin}_buys.csv")
    new_average = df["Price"].mean()

    print(f"Average price for new {coin} bought: {new_average}")


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
    df = pd.read_csv(f"{coin}_buys.csv")
    total_cost = df["Cost"].sum()
    return total_cost


def calulate_profit(coin):
    coins = calulate_new_total_coins(coin)
    cost = calculate_costs(coin)
    current_price = get_current_price(coin)

    current_value = coins * current_price
    profit = round((current_value - cost),2)
    percentage = round((profit/cost*100),2)
    return f'{profit} Dollars, {percentage}%'

print(calulate_new_total_coins("bitcoin"))