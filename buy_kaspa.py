import sys
import datetime
import pandas as pd
import json
from utils.utils import get_current_balance, withdraw_asset


def kaspa_buy():
    filename = "data/kaspa_buys.xlsx"
    withdrawals_file = "data/kaspa_withdrawals.json"

    df = pd.read_excel(filename)
    coins_owned = df["Coins"].sum()

    with open(withdrawals_file, "r") as f:
        total_withdrawn = json.load(f)["total"]

    coins_bought = (
        float(get_current_balance("kaspa")) - 5661.903 + total_withdrawn
    ) - coins_owned
    if coins_bought < 10:
        sys.exit()

    last_price = 49.5 / coins_bought
    now = datetime.datetime.now()
    buy_date = now.strftime("%m/%d/%Y")

    new_row = {"Date": buy_date, "Coins": coins_bought, "Price": last_price, "Cost": 50}
    print(new_row)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_excel(filename, index=False)

    row_count = len(df)
    if row_count % 2 == 0:
        withdraw_asset("KAS", 100)

        total_withdrawn += 100
        with open(withdrawals_file, "w") as f:
            json.dump({"total": total_withdrawn}, f)


kaspa_buy()
withdraw_asset("KAS", 100)
