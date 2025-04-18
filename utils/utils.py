import time
import requests
from utils.kraken_auth import handle_kraken_auth

def get_current_balance(coin):
    coin = 'KAS' if coin.lower() == 'kaspa' else 'XXBT'

    urlpath = "/0/private/Balance"

    payload = {
        "nonce": str(int(time.time() * 1000))
    }

    api_key, signature = handle_kraken_auth(urlpath, payload)
    
    api_url = "https://api.kraken.com" + urlpath

    headers = {
        "API-Key": api_key,
        "API-Sign": signature,
        "User-Agent": "kraken-api-client"
    }

    response = requests.post(api_url, headers=headers, data=payload)
    current_balance = response.json()['result'][coin]
    return current_balance
