import os
import asyncio
from telegram import Bot
from price import get_btc_price

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

async def main():
    print("Starting BTC bot...")

    btc_price = get_btc_price()
    print("BTC price:", btc_price)

    message = (
        "₿ Shuja BTC 5M Monitor\n\n"
        f"BTC Price: ${btc_price:,.2f}\n\n"
        "Status: Watching 5-minute market..."
    )

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )

    print("Telegram message sent!")

asyncio.run(main())
