import requests

def get_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

    response = requests.get(url, timeout=10)
    data = response.json()

    if "price" not in data:
        raise Exception(f"Binance error: {data}")

    return float(data["price"])
