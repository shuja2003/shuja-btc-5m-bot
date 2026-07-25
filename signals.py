def get_signal(start_price, current_price):
    change = ((current_price - start_price) / start_price) * 100

    if change > 0.05:
        signal = "BUY 🟢"
    elif change < -0.05:
        signal = "SELL 🔴"
    else:
        signal = "WAIT ⏳"

    return signal, change
