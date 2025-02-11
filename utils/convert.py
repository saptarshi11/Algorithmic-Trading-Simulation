# Convert OHLC pandas series to list for calculations
def series_to_lists(data):
    datetimes = data.datetimes.to_list()
    opens = data.opens.to_list()
    closes = data.closes.to_list()
    highs = data.highs.to_list()
    lows = data.lows.to_list()

    return datetimes, opens, closes, highs, lows
