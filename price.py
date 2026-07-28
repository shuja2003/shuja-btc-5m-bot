import requests

def get_btc_price():
    url = "https://data-api.binance.vision/api/v3/ticker/price?symbol=BTCUSDT"

    response = requests.get(url, timeout=10)
    data = response.json()

    return float(data["price"])
