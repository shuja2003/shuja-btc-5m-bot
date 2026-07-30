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
    try:
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

        print(f"Attempting Telegram send at {checkpoint}s...", flush=True)

        result = await bot.send_message(
            chat_id=CHAT_ID,
            text=message
        )

        print(
            f"Telegram message sent successfully. "
            f"Message ID: {result.message_id}",
            flush=True
        )

        print(message, flush=True)

        return signal

    except Exception as e:
        print(
            f"TELEGRAM SEND ERROR at {checkpoint}s: "
            f"{type(e).__name__}: {e}",
            flush=True
        )
        raise


async def run_bot():
    print("Starting Shuja BTC 5M Bot", flush=True)

    now = get_binance_time()

    candle_start = now - (now % 300)
    candle_end = candle_start + 300

    start_price = get_candle_open_price()

    print(f"New candle: {start_price}", flush=True)

    previous_signal = None
    sent = set()

    while True:
        now = get_binance_time()
        seconds_left = candle_end - now

        print(f"Seconds left: {seconds_left}", flush=True)

        for checkpoint in [90, 60, 30]:
            if seconds_left <= checkpoint and checkpoint not in sent:

                print(
                    f"Sending {checkpoint}s signal",
                    flush=True
                )

                previous_signal = await send_signal(
                    checkpoint,
                    start_price,
                    previous_signal
                )

                sent.add(checkpoint)

        if seconds_left <= 0:
            print(
                "5-minute candle finished.",
                flush=True
            )
            break

        await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(run_bot())

    except Exception as e:
        print(
            f"BOT ERROR: {type(e).__name__}: {e}",
            flush=True
        )
        raise
