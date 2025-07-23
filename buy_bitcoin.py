import datetime
import sys
from utils.utils import allocate_earn_funds, get_current_balance
import pandas as pd

def bitcoin_buy():
    filename = "data/bitcoin_buys.xlsx"
    df = pd.read_excel(filename)
    coins_owned = df["Coins"].sum()

    coins_bought = (float(get_current_balance("bitcoin"))) - (coins_owned - .0000311)
    if abs(coins_bought) < 0.00001:
        sys.exit()

    last_price = 50 / coins_bought
    now = datetime.datetime.now()
    buy_date = now.strftime("%m/%d/%Y")

    new_row = {"Date": buy_date, "Coins": coins_bought, "Price": last_price, "Cost": 50}
    print(new_row)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_excel(filename, index=False)

bitcoin_buy()
allocate_earn_funds()