# The result of one backtest


class Backtest:
    def __init__(
        self,
        unique_id,
        ticker,
        sim_period,
        total_investment,
        final_amount,
        total_return,
        win_rate,
        ma_period,
        rsi_period,
        atr_period,
        std_dev_period,
        max_order_value,
        max_concurrent_positions,
        buy_multiplier,
        band_multiplier,
        A_strategy_1,
        B_strategy_1,
        stoploss_atr_multiplier,
        takeprofit_atr_multiplier,
    ):
        # Constants
        self.unique_id = unique_id
        self.ticker = ticker
        self.sim_period = sim_period
        self.total_investment = total_investment
        self.final_amount = final_amount
        self.total_return = total_return
        self.win_rate = win_rate

        # Variables
        self.ma_period = ma_period
        self.rsi_period = rsi_period
        self.atr_period = atr_period
        self.std_dev_period = std_dev_period
        self.max_order_value = max_order_value
        self.max_concurrent_positions = max_concurrent_positions
        self.buy_multiplier = buy_multiplier
        self.band_multiplier = band_multiplier
        self.A_strategy_1 = A_strategy_1
        self.B_strategy_1 = B_strategy_1
        self.stoploss_atr_multiplier = stoploss_atr_multiplier
        self.takeprofit_atr_multiplier = takeprofit_atr_multiplier

    def to_dict(self):
        return self.__dict__


"""
# Example backtest results

backtest = Backtest(
    ticker="AAPL"  -- Ticker
    sim_period=252  -- backtest duration (days)
    total_investment=10000,  -- total amount invested
    final_amount=12000,  -- amount left at end of sim
    avg_annual_return=0.10,  -- average annual return (%)
    total_return=0.20,  -- total return over period (%)
    win_rate=0.65,    -- win rate (%)

    ma_period=14,    -- period used for calculating moving average        (14-50)
    rsi_period=7,    -- period used for calculating RSI                   (7-20)
    atr_period=14,   -- period used for calculating ATR                   (7-20)
    std_dev_period=10,  -- period used for calculating std. dev.          (7-20)
    max_order_value=5000,    -- max amount of any order
    max_concurrent_positions=5,    -- max positions that can be open at once
    buy_multiplier=1.5,    -- amount allocated entry capital is multiplied by before order is placed
    band_multiplier=2,     -- how many standard deviations will trigger a buy/sell with mean reversion
)
"""
