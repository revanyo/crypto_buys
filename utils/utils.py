import subprocess
import time
import requests
from utils.kraken_auth import handle_kraken_auth

def git_pull():
    subprocess.run(["git", "pull"], check=True)

def get_current_balance(coin):
    coin = 'KAS' if coin.lower() == 'kaspa' else 'XBT.F'

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
    current_balance = (float)(response.json()['result'][coin])
    allocated_balance = (float)(get_allocated_balance(coin))
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

def allocate_earn_funds():
    urlpath = "/0/private/Earn/Allocate"
    allocation_amount = get_current_balance('BTC') - float(get_allocated_balance('BTC'))
    payload = {
        "nonce": str(int(time.time() * 1000)),
        "amount": allocation_amount,
        'strategy_id':'ESVDZB3-C3ZRV-JLKVFR'
    }
    api_key, signature = handle_kraken_auth(urlpath, payload)
    
    api_url = "https://api.kraken.com" + urlpath

    headers = {
        "API-Key": api_key,
        "API-Sign": signature,
        "User-Agent": "kraken-api-client"
    }

    requests.post(api_url, headers=headers, data=payload).json()