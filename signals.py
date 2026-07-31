def get_signal(start_price, current_price, trend, previous_signal=None):
    change = ((current_price - start_price) / start_price) * 100

    if abs(change) < 0.01:
        signal = "⏳ WAIT"

    elif change >= 0.02 and trend == "UP":
        signal = "🟢 BUY UP"

    elif change <= -0.02 and trend == "DOWN":
        signal = "🔴 BUY DOWN"

    else:
        signal = "⏳ WAIT"

    reversal = None

    if previous_signal == "🟢 BUY UP" and signal == "🔴 BUY DOWN":
        reversal = "⚠️ REVERSAL: UP changed to DOWN"

    elif previous_signal == "🔴 BUY DOWN" and signal == "🟢 BUY UP":
        reversal = "⚠️ REVERSAL: DOWN changed to UP"

    return signal, change, reversal
