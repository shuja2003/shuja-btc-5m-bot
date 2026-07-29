def get_signal(start_price, current_price, previous_signal=None):
    change = ((current_price - start_price) / start_price) * 100

    # Too close - avoid risky entries
    if -0.01 < change < 0.01:
        signal = "⏳ WAIT"

    # Strong movement
    elif change >= 0.05:
        signal = "🟢 BUY UP"

    elif change <= -0.05:
        signal = "🔴 BUY DOWN"

    # Medium movement
    elif change >= 0.02:
        signal = "🟢 BUY UP"

    elif change <= -0.02:
        signal = "🔴 BUY DOWN"

    else:
        signal = "⏳ WAIT"

    # Detect reversal
    reversal = None

    if previous_signal:
        if previous_signal == "🟢 BUY UP" and signal == "🔴 BUY DOWN":
            reversal = "⚠️ REVERSAL: UP changed to DOWN"

        elif previous_signal == "🔴 BUY DOWN" and signal == "🟢 BUY UP":
            reversal = "⚠️ REVERSAL: DOWN changed to UP"

    return signal, change, reversal
