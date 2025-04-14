import csv
import datetime
import requests


def kaspa_buy():
    url = "https://api.kraken.com/0/public/Ticker?pair=KASUSD"

    headers = {
    'Accept': 'application/json'
    }

    last_price = round(float(requests.request("GET", url, headers=headers).json()['result']['KASUSD']['c'][0]), 5)
    coins_bought = round(50 / float(last_price), 8)

    now = datetime.datetime.now()
    buy_date = now.strftime("%m/%d/%Y")
    new_row = [buy_date,coins_bought,last_price,50]

    with open("kaspa_buys.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(new_row)

kaspa_buy()