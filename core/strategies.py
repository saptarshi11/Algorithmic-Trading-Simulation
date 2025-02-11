import api.fetch as api
import math

config = api.get_settings()

"""
Format your strategies responses as a dict with the values you need.

Example:

response = {
    "buy": True,
    "price": current_candle["open"],
    "amount": config["account"]["baseOrderValue"],
}
"""


# This strategy will buy if the price is considerably below the moving average and the stock has recently experienced a sharp decline in share price.
def bearish_comeback(candles, period):
    current_candle = candles[-1]
    most_recent_candle = candles[-2]
    for i in range(len(candles)):
        price_difference = (
            candles[i - (period + 1)]["open"] - most_recent_candle["open"]
        )  # Use (i - 1) because we want to buy at the open of the next candle (the current candle)
        ratio = price_difference / most_recent_candle["std_dev"]

        A = config["strategy1"]["A"]
        B = config["strategy1"]["B"]

        def check_price_against_sma(candle):
            if candle["open"] > candle["sma"]:
                return True
            elif candle["open"] < candle["sma"] and candle["sma"] - candle["open"] > (
                candle["std_dev"] * 4.2
            ):
                return True
            else:
                return False

        sma_allowed = check_price_against_sma(current_candle)

        if (
            ratio > A - (B * math.log(period + 1))
            and most_recent_candle["close"] - most_recent_candle["open"] < 0
        ):
            response = {
                "buy": True,
                "price": current_candle["open"],
                "amount": config["account"]["baseOrderValue"] * ratio,
            }
        else:
            response = {
                "buy": False,
            }
        return response
