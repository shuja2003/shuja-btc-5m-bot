import os
import asyncio
from telegram import Bot
from telegram.request import HTTPXRequest

from price import (
    get_btc_price,
    get_candle_open_price,
    get_binance_time,
    get_trend,
)

from signals import get_signal

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

request = HTTPXRequest(
    connect_timeout=5.0,
    read_timeout=5.0,
    write_timeout=5.0,
    pool_timeout=5.0,
)

bot = Bot(
    token=BOT_TOKEN,
    request=request,
)


async def send_countdown(start_price, time_left):
    current_price = get_btc_price()
    trend = get_trend()

    message = (
        "₿ Shuja BTC 5M Signal\n\n"
        f"Time left: {time_left} seconds\n\n"
        f"Start: ${start_price:,.2f}\n"
        f"Current: ${current_price:,.2f}\n"
        f"Trend: {trend}\n\n"
        "Preparing final signal..."
    )

    result = await asyncio.wait_for(
        bot.send_message(
            chat_id=CHAT_ID,
            text=message,
        ),
        timeout=10,
    )

    print(f"{time_left}s alert sent. ID: {result.message_id}", flush=True)


async def send_final_signal(start_price):
    current_price = get_btc_price()
    trend = get_trend()

    signal, change, _ = get_signal(
        start_price,
        current_price,
        trend,
        None,
    )

    message = (
        "₿ Shuja BTC 5M Signal\n\n"
        "Time left: 60 seconds\n\n"
        f"Start: ${start_price:,.2f}\n"
        f"Current: ${current_price:,.2f}\n"
        f"Trend: {trend}\n"
        f"Change: {change:.4f}%\n\n"
        f"Signal: {signal}"
    )

    result = await asyncio.wait_for(
        bot.send_message(
            chat_id=CHAT_ID,
            text=message,
        ),
        timeout=10,
    )

    print(f"60s signal sent. ID: {result.message_id}", flush=True)
    print(message, flush=True)


async def run_bot():
    print("Starting Shuja BTC 5M Bot", flush=True)

    while True:
        now = get_binance_time()

        candle_start = now - (now % 300)
        candle_end = candle_start + 300

        start_price = get_candle_open_price()

        checkpoints = [270, 240, 210, 180, 150, 120, 90, 60]

        for checkpoint in checkpoints:

            while True:
                now = get_binance_time()
                seconds_left = candle_end - now

                print(f"Seconds left: {seconds_left}", flush=True)

                if seconds_left <= checkpoint:
                    break

                await asyncio.sleep(5)

            if checkpoint == 60:
                await send_final_signal(start_price)
            else:
                await send_countdown(start_price, checkpoint)

        print("Candle completed. Waiting for next candle...", flush=True)

        while get_binance_time() < candle_end:
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run_bot())
