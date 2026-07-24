import os
import asyncio
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

async def main():
    await bot.send_message(
        chat_id=CHAT_ID,
        text="🚀 Shuja BTC 5M Bot is online!"
    )

asyncio.run(main())
