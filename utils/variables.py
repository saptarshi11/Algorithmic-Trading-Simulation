# Variables for running simulations

import random, json, string, os
import api.fetch as api


def randomise():
    config = api.get_settings()
    # config["indicators"]["maPeriod"] = random.randint(160, 240)
    config["indicators"]["rsiPeriod"] = random.randint(10, 20)
    config["indicators"]["atrPeriod"] = random.randint(15, 25)
    # config["indicators"]["stdDevPeriod"] = random.randint(25, 30)
    config["account"]["maxOrderValue"] = random.randint(
        (int(0.2 * config["account"]["initialBalance"])),
        (int(0.8 * config["account"]["initialBalance"])),
    )
    config["multipliers"]["buyMultiplier"] = random.uniform(1, 3)
    config["multipliers"]["bandMultiplier"] = random.uniform(1, 2)

    config["strategy1"]["A"] = round(random.uniform(3.4, 3.8), 2)
    config["strategy1"]["B"] = round(random.uniform(1.2, 1.7), 2)
    config["multipliers"]["stoplossAtrMultiplier"] = round(
        random.uniform(1.25, 2.25), 2
    )
    config["multipliers"]["takeprofitAtrMultiplier"] = round(
        random.uniform(2.5, 3.5), 2
    )

    with open("config.json", "w") as settings:
        json.dump(config, settings, indent=2)


def generate_uid(length):
    letters = string.ascii_lowercase + string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(length))


def write_to_json(all_backtests):
    simulation_id = generate_uid(6)
    file_path = os.path.join("z.results", f"sim-{simulation_id}.json")
    all_backtest_dicts = [backtest.to_dict() for backtest in all_backtests]

    with open(file_path, "w") as file:
        json.dump(all_backtest_dicts, file, indent=2)

    return simulation_id


def add_to_top_results(result):
    file_path = os.path.join("z.results", ".BEST-BACKTESTS.json")

    try:
        with open(file_path, "r") as file:
            existing_data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print(
            f"Warning: {file_path} is empty or contains invalid JSON. Initializing empty list."
        )
        existing_data = []

    existing_data.append(result.to_dict())

    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=2)


def load_best_backtests():
    file_path = os.path.join("z.results", f".BEST-BACKTESTS.json")

    try:
        with open(file_path, "r") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(
            f"Warning: {file_path} is empty, missing, or invalid. Returning an empty list."
        )
        existing_data = []

    return existing_data


def overwrite_top_results(backtests_to_write):
    file_path = os.path.join("z.results", f".BEST-BACKTESTS.json")

    all_backtest_dicts = [backtest.to_dict() for backtest in backtests_to_write]
    with open(file_path, "w") as file:
        json.dump(all_backtest_dicts, file, indent=2)


def random_colour():
    letters = "0123456789ABCDEF"
    color = "#"
    for i in range(6):
        color += letters[random.randint(0, 15)]
    return color


def generate_number(digits):
    number = ""
    for i in range(digits):
        digit = str(random.randint(0, 9))
        number += digit
    return number
