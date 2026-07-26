def get_signal(start_price, current_price):
    change = ((current_price - start_price) / start_price) * 100

    if change >= 0.01:
        signal = "🟢 BUY UP"
    elif change <= -0.01:
        signal = "🔴 BUY DOWN"
    else:
        signal = "⏳ WAIT"

    return signal, change
