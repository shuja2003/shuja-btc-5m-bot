import requests

def get_klines(limit=30):
    url = (
        f"https://data-api.binance.vision/api/v3/klines"
        f"?symbol=BTCUSDT&interval=5m&limit={limit}"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()
