import os
from openpyxl import load_workbook
from calculations import (
    calculate_allocation_percentage,
    calculate_total_coins_owned,
    calculate_total_profit,
    calulate_profit,
    get_current_price,
)
import pandas as pd
import datetime

def save_profit_data():
    filename = "data/profit_data.xlsx"
    columns = [
        "Date",
        "Portfolio Value(USD)",
        "BTC %",
        "KAS %",
        "KAS Profit(USD)",
        "KAS Profit(%)",
        "KAS Total Profit(USD)",
        "KAS Total Profit(%)",
        "BTC Profit(USD)",
        "BTC Profit(%)"
    ]

    if os.path.exists(filename):
        df = pd.read_excel(filename)
    else:
        df = pd.DataFrame(columns=columns)

    now = datetime.datetime.now()
    date = now.strftime("%m/%d/%Y")
    kaspa_profit = calulate_profit('kaspa')
    btc_profit = calulate_profit('bitcoin')
    kaspa_total_profit = calculate_total_profit('kaspa')
    allocation = calculate_allocation_percentage()
    new_row = {
    "Date": date,
    "Portfolio Value(USD)": calculate_portfolio(),
    "BTC %": allocation["bitcoin"],
    "KAS %": allocation["kaspa"],
    "KAS Profit(USD)": kaspa_profit[0],
    "KAS Profit(%)": kaspa_profit[1],
    "KAS Total Profit(USD)": kaspa_total_profit[0],
    "KAS Total Profit(%)": kaspa_total_profit[1],
    "BTC Profit(USD)": btc_profit[0],
    "BTC Profit(%)": btc_profit[1]
}
    print(new_row)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_excel(filename, index=False)

def calculate_portfolio():
    Kaspa_coins = calculate_total_coins_owned("kaspa")
    bitcoin_coins = calculate_total_coins_owned("bitcoin")
    kaspa_market_value = Kaspa_coins * get_current_price("kaspa")
    bitcoin_market_value = bitcoin_coins * get_current_price("bitcoin")
    market_value = kaspa_market_value + bitcoin_market_value
    portfolio = round(market_value, 2)
    return portfolio

save_profit_data()
