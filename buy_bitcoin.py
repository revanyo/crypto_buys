import datetime
import sys
from utils.utils import get_current_balance
import pandas as pd

def bitcoin_buy():
    filename = "data/bitcoin_buys.xlsx"
    df = pd.read_excel(filename)
    coins_owned = df["Coins"].sum()

  
    coins_bought = (float(get_current_balance("bitcoin")) - 0.00119649) - coins_owned
    if(coins_bought < .00001):
        sys.exit()

    last_price = 50 / coins_bought
    now = datetime.datetime.now()
    buy_date = now.strftime("%m/%d/%Y")

    new_row = {"Date": buy_date, "Coins": coins_bought, "Price": last_price, "Cost": 50}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_excel(filename, index=False)

bitcoin_buy()