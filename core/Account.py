import utils.indicator as indicator
import api.fetch as api

config = api.get_settings()


class Account:
    def __init__(
        self,
        uninvested_balance,
        balance_absolute,
        orders,
        profit,
        open_position_amount,
        total_invested,
        shares_owned,
        win_rate,
        completed_trades,
        profitable_trades,
        open_positions,
    ):
        self.uninvested_balance = uninvested_balance  # Initial account balance
        # e.g. 10 = minimum of 10% of account balance put into each trade
        self.balance_absolute = balance_absolute
        self.orders = (
            orders  # List of dicts: order amount, buy/sell price, units bought
        )
        self.profit = profit
        self.open_position_amount = open_position_amount
        self.total_invested = total_invested
        self.shares_owned = shares_owned
        self.win_rate = win_rate
        self.completed_trades = completed_trades
        self.profitable_trades = profitable_trades
        self.open_positions = open_positions

    def buy_order(self, datetime, order_value, stock_price):  # Place a buy order
        order = {
            "type": "BUY",
            "datetime": datetime,
            "amount": order_value,
            "price": stock_price,
            "no_shares": order_value / stock_price,
        }

        self.uninvested_balance -= order["amount"]
        self.total_invested += order["amount"]
        self.shares_owned += order["no_shares"]
        self.open_position_amount = self.shares_owned * order["price"]
        self.balance_absolute = self.uninvested_balance + self.open_position_amount
        self.open_positions += 1

        self.orders.append(order)

    def sell_order(self, datetime, stock_price):  # Place a sell order
        return_sum = self.shares_owned * stock_price

        order = {
            "type": "SELL",
            "datetime": datetime,
            "amount": return_sum,
            "price": stock_price,
            "no_shares": self.shares_owned,
        }

        trade_profit = return_sum - self.total_invested

        self.uninvested_balance += return_sum
        self.balance_absolute = self.uninvested_balance
        self.profit = self.balance_absolute - config["account"]["initialBalance"]
        self.completed_trades += 1
        if trade_profit > 0:
            self.profitable_trades += 1

        self.total_invested = 0
        self.shares_owned = 0
        self.open_position_amount = 0
        self.open_positions = 0

        self.orders.append(order)

    def check_balance(self):  # Does an initial balance check
        if config["account"]["initialBalance"] < config["account"]["baseOrderValue"]:
            return False
        else:
            return True
