import time
from abc import ABC, abstractmethod
from typing import Dict, List

from redis_cache_manager import RedisCacheManager
from services.buenbit.buenbit import BuenbitApiHandle


class TickerBase(ABC):

    @abstractmethod
    def set(self, key: str, value: Dict):
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str):
        raise NotImplementedError


class TickerManagerDataBase(TickerBase):

    def __init__(self):
        self.__db_manager = RedisCacheManager()

    def set(self, key: str, value: Dict):
        self.__db_manager.set_data(key=key, value=value)

    def get(self, key: str):
        return self.__db_manager.get_data(key=key)

    def get_zrange(self, key, start, end):
        return self.__db_manager.get_z_range_by_score(
            key=key,
            start=start,
            end=end
        )


class BuenbitTicker(TickerManagerDataBase):

    def __init__(self):
        super().__init__()
        self.buenbit_api = BuenbitApiHandle()

    def set_ticker(self, market_identifier: str = "btcars"):
        data = self.buenbit_api.handle(market_identifier)
        value = {data["price"]: data["timestamp"]}
        self.set(key="prices", value=value)

    def get_average_price(self, since_timestamp, until_timestamp) -> Dict:
        range_data = self.get_zrange(
            key="prices",
            start=since_timestamp,
            end=until_timestamp
        )

        average = 0
        if range_data:
            values = [float(price) for price, _ in range_data]
            average = round(sum(values) / len(values), 2)
        average_price = {"average_price": average}
        return average_price

    def get_tickers_list(
        self,
        since_timestamp: str,
        until_timestamp: str
    ) -> List[Dict]:

        range_data = self.get_zrange(
            key="prices",
            start=since_timestamp,
            end=until_timestamp
        )
        range_data = [
            {"timestamp": float(timestamp), "price": float(price)}
            for price, timestamp in range_data
        ]
        return range_data
