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

    last_candle = None

    while True:
        now = int(time.time())

        # Binance 5 minute candle alignment
        candle_start = now - (now % 300)
        candle_end = candle_start + 300

        # New candle detected
        if candle_start != last_candle:
            last_candle = candle_start

            start_price = get_btc_price()
            print(f"New candle started: {start_price}")

            # Wait until last 40 seconds of candle
            wait_time = candle_end - int(time.time()) - 40

            if wait_time > 0:
                await asyncio.sleep(wait_time)

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
                "⏱ 40 seconds before candle close"
            )

            await bot.send_message(
                chat_id=CHAT_ID,
                text=message
            )

            print("Signal sent!")

        # Check every 5 seconds
        await asyncio.sleep(5)


asyncio.run(main())
