
from abc import ABC, abstractmethod
from typing import Dict

from redis_cache_manager import RedisCacheManager
from services.buenbit.buenbit import BuenbitApiHandle


class TickerBase(ABC):

    @abstractmethod
    def set(self, key: str, value: Dict):
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str):
        raise NotImplementedError


class Ticker(TickerBase):

    def __init__(self):
        self.__redis_manager = RedisCacheManager()

    def set(self, key: str, value: Dict):
        self.__redis_manager.set_data(key=key, value=value)

    def get(self, key: str):
        return self.__redis_manager.get_data(key=key)


class RecurrentTicker:

    def __init__(self):
        self.ticker = Ticker()
        self.buenbit_api = BuenbitApiHandle()

    def set_ticker(self):
        data = self.buenbit_api.handle()
        self.ticker.set(key=data["timestamp"], value=data["price"])
