from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

import requests
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv(Path(".env"))

PATH_TO_HISTORY_FILE = os.path.join("./src/history.json")


@dataclass
class ExchangeRate:
    from_: str
    to: str
    value: float

    @classmethod
    def from_response(cls, response: requests.Response) -> ExchangeRate:
        pure_response: dict = response.json()["Realtime Currency Exchange Rate"]
        from_ = pure_response["1. From_Currency Code"]
        to = pure_response["3. To_Currency Code"]
        value = pure_response["5. Exchange Rate"][0:-5]

        return cls(from_=from_, to=to, value=value)

    def __eq__(self, other: ExchangeRate) -> bool:
        return self.value == other.value


ExchangeRates = List[ExchangeRate]


class ExchangeRatesHistory:
    _last_exchange_data: ExchangeRates = None
    history_data: Dict[List] = {"result": []}

    @classmethod
    def read_history_file(cls):
        with open(PATH_TO_HISTORY_FILE, "r") as file:
            cls.history_data = json.load(file)
        return cls.history_data

    @classmethod
    def update_file(cls) -> None:
        """Doing updates file "history.json" and "history_data" variable,  or creating the file if it out"""
        new_data = asdict(cls._last_exchange_data)

        if not os.path.isfile(PATH_TO_HISTORY_FILE):
            with open(PATH_TO_HISTORY_FILE, "w") as file:
                cls.history_data["result"].append(new_data)
                json.dump(cls.history_data, file, indent=2)
        else:
            cls.read_history_file()
            with open(PATH_TO_HISTORY_FILE, "w") as file:
                cls.history_data["result"].append(new_data)
                json.dump(cls.history_data, file, indent=2)

    @classmethod
    def add(cls, instance: ExchangeRate) -> None:
        """We would like to add ExchangeRates instances if it is not last duplicated"""

        if not cls._last_exchange_data:
            cls._last_exchange_data = instance
            cls.update_file()
        elif cls._last_exchange_data != instance:
            cls._last_exchange_data = instance
            cls.update_file()


def btc_usd(request):
    # NOTE: Connect to the external exchange rates API
    API_KEY = os.getenv("API_KEY_EXCHANGE_RATE")
    url = (
        "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&"
        f"from_currency=BTC&to_currency=USD&apikey={API_KEY}"
    )

    response = requests.get(url)
    exchange_rate = ExchangeRate.from_response(response)
    ExchangeRatesHistory.add(exchange_rate)

    return JsonResponse(asdict(exchange_rate))


def history(request):
    if os.path.isfile(PATH_TO_HISTORY_FILE):
        ExchangeRatesHistory.read_history_file()
    return JsonResponse(ExchangeRatesHistory.history_data)
