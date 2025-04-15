from openpyxl import load_workbook
import datetime
import requests


def kaspa_buy():
    url = "https://api.kraken.com/0/public/Ticker?pair=KASUSD"

    headers = {"Accept": "application/json"}

    last_price = round(
        float(
            requests.request("GET", url, headers=headers).json()["result"]["KASUSD"][
                "c"
            ][0]
        ),
        5,
    )
    coins_bought = round(50 / float(last_price), 8)

    now = datetime.datetime.now()
    buy_date = now.strftime("%m/%d/%Y")
    new_row = [buy_date, coins_bought, last_price, 50]

    filename = "data/kaspa_buys.xlsx"

    wb = load_workbook(filename)
    ws = wb.active
    ws.append(new_row)
    wb.save(filename)


kaspa_buy()
