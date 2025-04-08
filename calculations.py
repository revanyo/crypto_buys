import json
import pandas as pd

def calculate_total_average(coin):
    with open('average.json') as f:
        data = json.load(f)[coin]
        old_coins= data['coins']
        old_average_price= data['avergae_buy_price']

    df = pd.read_csv(f'{coin}_buys.csv')

    new_coins = df['Coins'].sum()
    new_price = df['Price'].mean()

    weighted_avg = ((old_average_price * old_coins) + (new_price * new_coins)) / (old_coins + new_coins)

    print(f'New Average Price: {weighted_avg}')

def calculate_total_coins_owned(coin):
    with open('average.json') as f:
        data = json.load(f)[coin]
        old_coins= data['coins']

    df = pd.read_csv(f'{coin}_buys.csv')

    new_coins = df['Coins'].sum()

    total_coins = old_coins+new_coins

    print(f'Total coins owned: {total_coins}')

def calulate_new_total_coins(coin):
    df = pd.read_csv(f'{coin}_buys.csv')
    print(f'New coins of {coin} bought: {df["Coins"].sum()}')

def calulate_new_average(coin):
    df = pd.read_csv(f'{coin}_buys.csv')
    new_average = df['Price'].mean()

    print(f'Average price for new {coin} bought: {new_average}')

calulate_new_average('kaspa')


