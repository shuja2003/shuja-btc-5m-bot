import os
import asyncio
from telegram import Bot

from price import (
    get_btc_price,
    get_candle_open_price,
    get_binance_time,
)
from signals import get_signal

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)


async def send_signal(checkpoint, start_price, previous_signal):
    current_price = get_btc_price()

    signal, change, reversal = get_signal(
        start_price,
        current_price,
        previous_signal
    )

    message = (
        "₿ Shuja BTC 5M Signal\n\n"
        f"Time left: {checkpoint} seconds\n\n"
        f"Start: ${start_price:,.2f}\n"
        f"Current: ${current_price:,.2f}\n"
        f"Change: {change:.4f}%\n\n"
        f"Signal: {signal}"
    )

    if reversal:
        message += f"\n\n{reversal}"

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )

    print(message)

    return signal


async def run_bot():
    print("Starting Shuja BTC 5M Bot")

    last_candle = None
    sent = set()
    previous_signal = None
    start_price = None

    while True:

        now = get_binance_time()

        candle_start = now - (now % 300)
        candle_end = candle_start + 300

        if candle_start != last_candle:
            last_candle = candle_start
            start_price = get_candle_open_price()
            sent = set()
            previous_signal = None

            print(f"New candle: {start_price}")

        seconds_left = candle_end - now

        print(f"Seconds left: {seconds_left}")

        for checkpoint in [90, 60, 30]:
            if seconds_left <= checkpoint and checkpoint not in sent:

                print(f"Sending {checkpoint}s signal")

                previous_signal = await send_signal(
                    checkpoint,
                    start_price,
                    previous_signal
                )

                sent.add(checkpoint)

        await asyncio.sleep(1)


asyncio.run(run_bot())
