import datetime
import requests
import csv

def bitcoin_buy():
    url = "https://api.kraken.com/0/public/Ticker?pair=BTCUSD"

    headers = {
    'Accept': 'application/json'
    }

    last_price = round(float(requests.request("GET", url, headers=headers).json()['result']['XXBTZUSD']['c'][0]), 2)
    coins_bought = round(50/ float(last_price), 8)

    now = datetime.datetime.now()
    buy_date = now.strftime("%m/%d/%Y")
    new_row = [buy_date,coins_bought,last_price,50]

    with open("bitcoin_buys.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(new_row)

bitcoin_buy()