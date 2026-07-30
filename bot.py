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

        print(f"Attempting Telegram send at {checkpoint}s...")

        result = await bot.send_message(
            chat_id=CHAT_ID,
            text=message
        )

        print(f"Telegram message sent successfully. Message ID: {result.message_id}")
        print(message)

        return signal

    except Exception as e:
        print(f"TELEGRAM SEND ERROR at {checkpoint}s: {type(e).__name__}: {e}")
        raise
