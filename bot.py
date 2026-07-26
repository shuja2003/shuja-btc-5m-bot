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

    while True:
        start_time = time.time()
        start_price = get_btc_price()

        print("5M round started:", start_price)

        # Wait until last 50 seconds of 5 minute candle
        await asyncio.sleep(250)

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
            "⏱ Last 50 seconds"
        )

        await bot.send_message(
            chat_id=CHAT_ID,
            text=message
        )

        print("50 second signal sent!")

        # wait for next 5 minute round
        await asyncio.sleep(50)

asyncio.run(main())
