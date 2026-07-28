def get_signal(start_price, current_price):
    change = ((current_price - start_price) / start_price) * 100

    # Strong move up
    if change >= 0.05:
        signal = "🟢 BUY UP"

    # Strong move down
    elif change <= -0.05:
        signal = "🔴 BUY DOWN"

    # Small move up
    elif change >= 0.02:
        signal = "🟢 BUY UP"

    # Small move down
    elif change <= -0.02:
        signal = "🔴 BUY DOWN"

    else:
        signal = "⏳ WAIT"

    return signal, change
