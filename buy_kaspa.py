from openpyxl import load_workbook
import datetime
import pandas as pd

from utils.utils import get_current_balance


def kaspa_buy():
    filename = "data/kaspa_buys.xlsx"
    df = pd.read_excel(filename)
    coins_owned = df["coins"].sum()

    coins_bought = get_current_balance("kaspa") - coins_owned
    last_price = 50 / coins_bought
    now = datetime.datetime.now()
    buy_date = now.strftime("%m/%d/%Y")

    new_row = {"Date": buy_date, "Coins": coins_bought, "Price": last_price, "Cost": 50}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_excel(filename, index=False)


kaspa_buy()
