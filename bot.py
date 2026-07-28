import os
import asyncio
import time
from telegram import Bot
from price import get_btc_price
from signals import get_signal

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)


async def main():
    print("Starting BTC 5M bot...")

    now = int(time.time())

    # Current 5-minute candle
    candle_start = now - (now % 300)
    candle_end = candle_start + 300

    start_price = get_btc_price()
    print(f"Start price: {start_price}")

    # Wait until 60 seconds before candle close
    wait_time = candle_end - int(time.time()) - 60

    if wait_time > 0:
        print(f"Waiting {wait_time} seconds...")
        await asyncio.sleep(wait_time)

    current_price = get_btc_price()

    signal, change = get_signal(start_price, current_price)

    message = (
        "₿ Shuja BTC 5M Signal\n\n"
        f"Start: ${start_price:,.2f}\n"
        f"Current: ${current_price:,.2f}\n"
        f"Change: {change:.4f}%\n\n"
        f"Signal: {signal}\n"
        "⏱ 60 seconds before candle close"
    )

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )

    print("Signal sent!")

async def run_bot():
    while True:
        await main()
        await asyncio.sleep(300)


asyncio.run(run_bot())
