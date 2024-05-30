import os
from abc import ABC, abstractmethod
from datetime import datetime

import requests


class ApiService(ABC):

    @abstractmethod
    def get(self):
        return NotImplementedError


class BuenbitApiService(ApiService):

    def __init__(self):
        self.url = os.environ.get("BUENBIT_URL", "")
        self.headers = {
            "content-type": "application/json"
        }

    def get(self):
        response = requests.get(
            url=self.url,
            headers=self.headers
        )
        return response.json()


class BuenbitApiHandle:

    def __init__(self):
        self.buenbit_service = BuenbitApiService()

    def handle(self, market_identifier: str = "btcars"):
        data = self.buenbit_service.get()
        btc_ars_data = data['object'][market_identifier]

        ticker_data = {
            'timestamp': int(datetime.now().timestamp()),
            'price': btc_ars_data['selling_price']
        }

        return ticker_data
