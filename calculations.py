from datetime import datetime
import json
import pandas as pd
import requests

def get_loan_amount():
    # Hardcoded loan files
    loan_files = ['data/loan_one.csv', 'data/loan_two.csv']

    # Get the current date
    current_date = datetime.today()

    total_principal = 0

    for loan_file in loan_files:
        # Load the loan CSV file
        df = pd.read_csv(loan_file)

        # Find the next row with a date after today's date
        next_row = df[df['Date'] > current_date.strftime('%B %d %Y')].iloc[0]
        
        # Add the principal of the next row to the total
        total_principal += next_row['Principal']

    return round(total_principal,2) -5000


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


def calulate_profit(coin):
    coins = calculate_new_total_coins(coin)
    cost = calculate_costs(coin)
    current_price = get_current_price(coin)

    current_value = coins * current_price
    profit = round((current_value - cost),2)
    percentage = round((profit/cost*100),2)
    print()
    return f'Profit: ${profit}, ({percentage}%) --{coin}'

def calculate_total_profit(coin):
    with open("data/average.json") as f:
        data = json.load(f)[coin]
        old_coins = data["coins"]
        old_average_price = data["avergae_buy_price"]
    cost_basis = (calculate_costs(coin)) + (old_coins*old_average_price)
    market_value = (old_coins + calculate_new_total_coins(coin))*get_current_price(coin)
    total_profit = market_value - cost_basis
    percentage = round((total_profit / cost_basis) * 100, 2)
    print()
    return f"Total profit: ${round(total_profit, 2)}, ({percentage}%) --{coin}"
    

def calculate_portfolio_minus_loan():
    Kaspa_coins = calculate_total_coins_owned("kaspa")
    bitcoin_coins = calculate_total_coins_owned("bitcoin")
    loans=get_loan_amount()
    kaspa_market_value=Kaspa_coins*get_current_price("kaspa")
    bitcoin_market_value=bitcoin_coins*get_current_price("bitcoin")
    market_value = kaspa_market_value + bitcoin_market_value
    print()
    return f'Total Portfolio Net Worth: {round(market_value,2)} - {loans} = {round(market_value-loans,2)}'

print(calulate_profit("kaspa"))
print(calculate_total_profit("kaspa"))
print(calulate_profit("bitcoin"))
print(calculate_total_profit("bitcoin"))
print(calculate_portfolio_minus_loan())