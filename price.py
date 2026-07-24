import requests

def get_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

    response = requests.get(url, timeout=10)
    data = response.json()

    return float(data["price"])
