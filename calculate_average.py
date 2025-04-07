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
    total_coins = old_coins+new_coins

    print(f'Sum of new coins: {new_coins}')

    print(f'New Average Price: {weighted_avg}')
    print(f'Total coins owned: {total_coins}')

def calculate_total_coins_owned(coin):
    with open('average.json') as f:
        data = json.load(f)[coin]
        old_coins= data['coins']

    df = pd.read_csv(f'{coin}_buys.csv')

    new_coins = df['Coins'].sum()

    total_coins = old_coins+new_coins

    print(f'Total coins owned: {total_coins}')
