import api.fetch as api


class Rules:
    def __init__(self, payload):
        self.payload = payload
        self.config = api.get_settings()

    def balance_valid(self):
        initial_buy_amount = self.payload["initial_buy_amount"]
        if initial_buy_amount > self.config["account"]["maxOrderValue"]:
            initial_buy_amount = self.config["account"]["maxOrderValue"]
        if initial_buy_amount > (self.payload["account"]).uninvested_balance:
            initial_buy_amount = (self.payload["account"]).uninvested_balance

        if initial_buy_amount > 0:
            response = {"valid": True, "amount": initial_buy_amount}
        else:
            response = {"valid": False, "amount": 0}

        return response

    def max_positions_reached(self):
        account = self.payload["account"]
        if account.open_positions >= self.config["account"]["maxConcurrentPositions"]:
            return False
        else:
            return True

    # Go through all the rules
    def correctify(self):
        balance_valid = Rules.balance_valid(self)["valid"]
        max_positions_reached = Rules.max_positions_reached(self)
        response = {
            "balance_valid": balance_valid,
            "max_positions_reached": max_positions_reached,
        }

        return response
