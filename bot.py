import asyncio
from telegram import Bot
import os
import requests
async def run_bot():
    print("Starting Shuja BTC 5M Bot 24/7", flush=True)

    while True:
        try:
            now = get_binance_time()

            candle_start = now - (now % 300)
            candle_end = candle_start + 300

            start_price = get_candle_open_price()

            seconds_left = candle_end - now

            print(f"Seconds left: {seconds_left}", flush=True)

            checkpoints = [120, 60, 30]
            previous = seconds_left

            for checkpoint in checkpoints:
                wait_time = previous - checkpoint

                if wait_time > 0:
                    print(f"Waiting {wait_time} seconds...", flush=True)
                    await asyncio.sleep(wait_time)

                if checkpoint == 30:
                    await send_final_signal(start_price)
                else:
                    await send_countdown(start_price, checkpoint)

                previous = checkpoint

            print("Candle completed. Starting next candle...", flush=True)
            await asyncio.sleep(5)

        except Exception as e:
            print(f"Error: {e}", flush=True)
            await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(run_bot())

    
