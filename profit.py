from openpyxl import load_workbook
from calculations import (
    calculate_allocation_percentage,
    calculate_total_coins_owned,
    get_current_price,
    get_loan_amount,
)
import pandas as pd
import datetime
from data.loan_data import loan_one, loan_two


def calculate_and_save_profit():
    filename = "data/profit.xlsx"
    df = pd.read_excel(filename)

    now = datetime.datetime.now()
    date = now.strftime("%m/%d/%Y")

    Kaspa_coins = calculate_total_coins_owned("kaspa")
    bitcoin_coins = calculate_total_coins_owned("bitcoin")
    loans = (get_loan_amount(loan_one) + get_loan_amount(loan_two)) - 1000
    kaspa_market_value = Kaspa_coins * get_current_price("kaspa")
    bitcoin_market_value = bitcoin_coins * get_current_price("bitcoin")
    market_value = kaspa_market_value + bitcoin_market_value
    profit = round(market_value - loans, 2)

    new_row = {"Date": date, "Profit": profit}
    print(new_row)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_excel(filename, index=False)


def calculate_and_save_allocation_percentage():
    filename = "data/profit.xlsx"

    # Load workbook and sheet
    wb = load_workbook(filename)
    if "Sheet2" in wb.sheetnames:
        ws = wb["Sheet2"]
    else:
        ws = wb.create_sheet("Sheet2")

    now = datetime.datetime.now()
    date = now.strftime("%m/%d/%Y")
    allocation = calculate_allocation_percentage()

    # Find next empty row
    next_row = ws.max_row + 1

    # Write new row
    ws.cell(row=next_row, column=1, value=date)
    ws.cell(row=next_row, column=2, value=allocation["bitcoin"])
    ws.cell(row=next_row, column=3, value=allocation["kaspa"])

    wb.save(filename)

calculate_and_save_profit()
calculate_and_save_allocation_percentage()
