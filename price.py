import requests


def get_btc_price():
    url = "https://data-api.binance.vision/api/v3/ticker/price?symbol=BTCUSDT"

    response = requests.get(url, timeout=10)
    data = response.json()

    return float(data["price"])


def get_candle_open_price():
    url = "https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=1"

    response = requests.get(url, timeout=10)
    data = response.json()

    return float(data[0][1])


def get_binance_time():
    url = "https://data-api.binance.vision/api/v3/time"

    response = requests.get(url, timeout=10)
    data = response.json()

    return int(data["serverTime"] / 1000)


def get_trend():
    url = "https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=5"

    response = requests.get(url, timeout=10)
    data = response.json()

    up = 0
    down = 0

    for candle in data:
        open_price = float(candle[1])
        close_price = float(candle[4])

        if close_price > open_price:
            up += 1
        elif close_price < open_price:
            down += 1

    if up >= 3:
        return "UP"
    elif down >= 3:
        return "DOWN"
    else:
        return "SIDEWAYS"
