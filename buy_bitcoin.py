import datetime
from openpyxl import load_workbook
import requests


def bitcoin_buy():
    url = "https://api.kraken.com/0/public/Ticker?pair=BTCUSD"

    headers = {"Accept": "application/json"}

    last_price = round(
        float(
            requests.request("GET", url, headers=headers).json()["result"]["XXBTZUSD"][
                "c"
            ][0]
        ),
        2,
    )
    coins_bought = round(50 / float(last_price), 8)

    now = datetime.datetime.now()
    buy_date = now.strftime("%m/%d/%Y")
    new_row = [buy_date, coins_bought, last_price, 50]

    filename = "data/bitcoin_buys.xlsx"

    wb = load_workbook(filename)
    ws = wb.active
    ws.append(new_row)
    wb.save(filename)


bitcoin_buy()
