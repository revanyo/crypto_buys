import requests

def kaspa_buy():
    url = "https://api.kraken.com/0/public/Ticker?pair=KASUSD"

    headers = {
    'Accept': 'application/json'
    }

    last_price = requests.request("GET", url, headers=headers).json()['result']['KASUSD']['c'][0]
    coins_bought = 49.5 / float(last_price)

def bitcoin_buy():
    pass