import os
import asyncio
import time
from telegram import Bot
from price import get_btc_price, get_candle_open_price
from signals import get_signal

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)


async def run_bot():
    print("Starting BTC 5M continuous bot...")

    last_candle = None

    while True:
        now = int(time.time())

        candle_start = now - (now % 300)
        candle_end = candle_start + 300

        if last_candle != candle_start:
            last_candle = candle_start

            start_price = get_candle_open_price()
            print(f"New candle: {start_price}")

        seconds_left = candle_end - now

        if seconds_left == 60:
            current_price = get_btc_price()

            signal, change = get_signal(
                start_price,
                current_price
            )

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

        await asyncio.sleep(1)


asyncio.run(run_bot())
