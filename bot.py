import os
import asyncio
from telegram import Bot
from price import get_btc_price
from signal import get_signal

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

async def main():
    print("Starting BTC 5M bot...")

    start_price = get_btc_price()
    print("Start price:", start_price)

    # Test movement (later we will replace this with real 5-minute tracking)
    current_price = get_btc_price()

    signal, change = get_signal(start_price, current_price)

    message = (
        "₿ Shuja BTC 5M Signal\n\n"
        f"BTC Price: ${current_price:,.2f}\n"
        f"Change: {change:.4f}%\n\n"
        f"Signal: {signal}"
    )

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )

    print("Signal sent!")

asyncio.run(main())
