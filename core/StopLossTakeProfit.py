import api.fetch as api

config = api.get_settings()


class StopLossTakeProfit:
    def __init__(self, initial_stoploss=None, initial_takeprofit=None):
        self.stoploss = initial_stoploss
        self.takeprofit = initial_takeprofit
        self.values_set = False
        self.stoploss_region = {
            "x0": None,
            "x1": None,
            "y0": None,
            "y1": None,
            "fillcolor": "#ff3636",
            "opacity": 0.35,
        }
        self.takeprofit_region = {
            "x0": None,
            "x1": None,
            "y0": None,
            "y1": None,
            "fillcolor": "#31e62e",
            "opacity": 0.35,
        }

        self.stoploss_regions = []
        self.takeprofit_regions = []

    def update(self, entry_price, atr, datetime):
        self.stoploss = entry_price - (
            atr * config["multipliers"]["stoplossAtrMultiplier"]
        )
        self.takeprofit = entry_price + (
            atr * config["multipliers"]["takeprofitAtrMultiplier"]
        )
        self.values_set = True

        self.update_stoploss_region(
            y1=entry_price,
            y0=entry_price - (config["multipliers"]["stoplossAtrMultiplier"] * atr),
            x0=datetime,
        )
        self.update_takeprofit_region(
            y0=entry_price,
            y1=entry_price + (config["multipliers"]["takeprofitAtrMultiplier"] * atr),
            x0=datetime,
        )

    def remove(self):
        self.stoploss = None
        self.takeprofit = None
        self.values_set = False

    def exit(self, current_candle):
        max_value = max(current_candle["high"], current_candle["close"])
        min_value = min(current_candle["low"], current_candle["close"])

        if max_value > self.takeprofit:
            self.update_takeprofit_region(x1=current_candle["datetime"])
            self.update_stoploss_region(x1=current_candle["datetime"])
            self.add_complete_stoploss_region()
            self.add_complete_takeprofit_region()
            return {"sell": True, "price": self.takeprofit}

        elif min_value < self.stoploss:
            self.update_takeprofit_region(x1=current_candle["datetime"])
            self.update_stoploss_region(x1=current_candle["datetime"])
            self.add_complete_stoploss_region()
            self.add_complete_takeprofit_region()
            return {"sell": True, "price": self.stoploss}

        return {"sell": False, "price": None}

    def update_stoploss_region(self, x0=None, x1=None, y0=None, y1=None):
        self.stoploss_region.update(
            {
                "x0": self.stoploss_region["x0"] if x0 is None else x0,
                "x1": self.stoploss_region["x1"] if x1 is None else x1,
                "y0": self.stoploss_region["y0"] if y0 is None else y0,
                "y1": self.stoploss_region["y1"] if y1 is None else y1,
            }
        )

    def add_complete_stoploss_region(self):
        self.stoploss_regions.append(self.stoploss_region.copy())

    def update_takeprofit_region(self, x0=None, x1=None, y0=None, y1=None):
        self.takeprofit_region.update(
            {
                "x0": self.takeprofit_region["x0"] if x0 is None else x0,
                "x1": self.takeprofit_region["x1"] if x1 is None else x1,
                "y0": self.takeprofit_region["y0"] if y0 is None else y0,
                "y1": self.takeprofit_region["y1"] if y1 is None else y1,
            }
        )

    def add_complete_takeprofit_region(self):
        self.takeprofit_regions.append(self.takeprofit_region.copy())
