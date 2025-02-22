import logging
import statistics

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class TradeManager:
    def __init__(self):
        # Active trades stored as dicts with the initial trade level and details.
        self.active_trades = []
        self.max_orders = 10

    def can_enter_trade(self, price):
        # Allow a maximum of 10 orders per chart.
        if len(self.active_trades) >= self.max_orders:
            return False, "Maximum order count reached."
        # Enforce that new trade entries occur at the same initial price.
        if self.active_trades:
            initial_price = self.active_trades[0]['price']
            if price != initial_price:
                return False, f"Price {price} differs from the initial trade price {initial_price}"
        return True, ""

    def enter_trade(self, trade):
        can_enter, msg = self.can_enter_trade(trade['price'])
        if not can_enter:
            logger.debug("Trade entry blocked: %s", msg)
            return False
        self.active_trades.append(trade)
        logger.info("Entered trade: %s", trade)
        return True

    def reverse_trade(self, new_signal):
        logger.info("Signal reversed to %s; closing existing trades.", new_signal)
        self.active_trades.clear()

def calculate_sma(candles, period=40):
    # Calculate the Simple Moving Average over the given period.
    if len(candles) < period:
        # If not enough candles, use the average of available data.
        return statistics.mean([c['close'] for c in candles])
    closing_prices = [c['close'] for c in candles[-period:]]
    return sum(closing_prices) / period

def calculate_dynamic_resistance(candles):
    # Calculate resistance as the highest high over the last 3 hours.
    # For a 5‑minute chart, 3 hours equals 36 candles.
    relevant = candles[-36:] if len(candles) >= 36 else candles
    resistance = max(c['high'] for c in relevant)
    return resistance

def calculate_dynamic_support(candles):
    # Calculate support as the lowest low over the most recent trading day.
    # Here we assume a trading day is roughly 6.5 hours (78 candles) for example purposes.
    relevant = candles[-78:] if len(candles) >= 78 else candles
    support = min(c['low'] for c in relevant)
    return support

def evaluate_trade_signal(candles, support, resistance, sma):
    """
    Evaluate the last three 5‑minute candles for trade signals.
    • Buy if every candle closes on or above the support (or resistance) level and above the 40‑period SMA.
    • Sell if every candle closes on or below the support (or resistance) level and below the 40‑period SMA.
    """
    if len(candles) < 3:
        return "HOLD"
    last_three = candles[-3:]
    # Buy conditions:
    buy_support = all(c['close'] >= support and c['close'] >= sma for c in last_three)
    buy_resistance = all(c['close'] >= resistance and c['close'] >= sma for c in last_three)
    # Sell conditions:
    sell_support = all(c['close'] <= support and c['close'] <= sma for c in last_three)
    sell_resistance = all(c['close'] <= resistance and c['close'] <= sma for c in last_three)

    if buy_support or buy_resistance:
        return "BUY"
    elif sell_support or sell_resistance:
        return "SELL"
    else:
        return "HOLD"

def main():
    # In a live system, candle data would be retrieved using MT5's API.
    # Here we simulate 100 M5 candles with dummy data for demonstration.
    candles = []
    for i in range(100):
        # Simulated price oscillations.
        base = 1.1000 + 0.001 * (i % 5)
        candle = {
            'open': base,
            'high': base + 0.0005,
            'low':  base - 0.0005,
            'close': base + 0.0002 if (i % 2 == 0) else base - 0.0002
        }
        candles.append(candle)

    # Calculate dynamic support, resistance, and 40‑period SMA.
    resistance = calculate_dynamic_resistance(candles)
    support = calculate_dynamic_support(candles)
    sma = calculate_sma(candles, period=40)

    logger.info("Calculated Resistance: %s", resistance)
    logger.info("Calculated Support: %s", support)
    logger.info("Calculated 40‑period SMA: %s", sma)

    # Evaluate trade signal based on the last 3 candles.
    signal = evaluate_trade_signal(candles, support, resistance, sma)
    logger.info("Evaluated Trade Signal: %s", signal)

    # Order management:
    trade_manager = TradeManager()
    current_price = candles[-1]['close']

    # If a trade exists and the new signal is different, reverse (take profit and close position).
    if trade_manager.active_trades and trade_manager.active_trades[0]['signal'] != signal:
        trade_manager.reverse_trade(signal)

    # Place a trade if the signal is BUY or SELL.
    if signal in ["BUY", "SELL"]:
        trade = {"signal": signal, "price": current_price}
        trade_manager.enter_trade(trade)
    else:
        logger.info("No valid trade signal; holding position.")

if __name__ == "__main__":
    main()
