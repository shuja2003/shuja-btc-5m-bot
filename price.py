import requests
import time


def get_btc_price():
    url = "https://data-api.binance.vision/api/v3/ticker/price?symbol=BTCUSDT"

    response = requests.get(url, timeout=10)
    data = response.json()

    return float(data["price"])


def get_candle_open_price():
    url = "https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=1"

    response = requests.get(url, timeout=10)
    data = response.json()

    candle_open = float(data[0][1])

    return candle_open
