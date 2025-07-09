from datetime import datetime
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

    allocated_balance = get_allocated_balance(coin)
    return current_balance + allocated_balance

def get_allocated_balance(coin):
    if coin == 'KAS':
        return 0
    urlpath = "/0/private/Earn/Allocations"

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

    response = requests.post(api_url, headers=headers, data=payload).json()
    items = response['result']['items']
    strategies = [item for item in items if item['native_asset'] == 'BTC']
    allocated_amount = strategies[0]['amount_allocated']['total']['native']
    return allocated_amount