import os
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# File name
filename = 'loan_two.csv'

# Delete the file if it exists
if os.path.exists(filename):
    os.remove(filename)
    
total_principal = 6432.45
payment_amount = 142.04
start_date = datetime(2025, 5, 14)
payment_interval = relativedelta(months=1)
interest_rate = 0.00669

rows = []
current_date = start_date

rows.append 
while total_principal > 0.01:  # stop once principal is basically paid off
    interest = total_principal * interest_rate
    payment = min(payment_amount, total_principal + interest)
    total_principal = total_principal + interest - payment
    total_principal = round(total_principal, 2)  # prevent long decimal tails
    rows.append({
        'Date': current_date.strftime('%B %d %Y'),
        'Principal': total_principal,
        'Interest': round(interest, 2)
    })
    current_date += payment_interval

df = pd.DataFrame(rows)
df.to_csv(filename, mode='a', index=False, header=True)