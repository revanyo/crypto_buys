import json
import pandas as pd

with open('average.json') as f:
    data = json.load(f)
    old_coins= data['coins']
    old_average_price= data['avergae_buy_price']

df = pd.read_csv('bitcoin_buys.csv')

new_coins = df['Coins'].sum()
new_price = df['Price'].mean()

print(new_coins)
print(new_price)

# weighted_avg = ((old_average_price * old_coins) + (new_price * new_coins)) / (old_coins + new_coins)
# total_coins = old_coins+new_coins
