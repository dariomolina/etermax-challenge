import time
from abc import ABC, abstractmethod
from typing import Dict, List

from redis_cache_manager import RedisCacheManager
from services.buenbit.buenbit import BuenbitApiHandle


class TickerBase(ABC):
    """
    Abstract base class for ticker management.
    """

    @abstractmethod
    def set(self, key: str, value: Dict):
        """
        Set a key-value pair in the cache.

        Args:
            key (str): The key under which the value should be stored.
            value (Dict): The value to be stored.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def get_zrange(self, key: str, start, end):
        """
        Retrieve a range of elements from a sorted set in the cache by score.

        Args:
            key (str): The key of the sorted set.
            start: The minimum score of the range.
            end: The maximum score of the range.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError


class TickerManagerDataBase(TickerBase):
    """
    Implementation of TickerBase using Redis for cache management.
    """

    def __init__(self):
        """
        Initialize TickerManagerDataBase with a RedisCacheManager
        instance.
        """
        self.__db_manager = RedisCacheManager()

    def set(self, key: str, value: Dict):
        """
        Set a key-value pair in the Redis cache.

        Args:
            key (str): The key under which the value should be stored.
            value (Dict): The value to be stored.
        """
        self.__db_manager.set_data(key=key, value=value)

    def get_zrange(self, key: str, start: str, end: str):
        """
        Retrieve a range of elements from a sorted set in the Redis
        cache by score.

        Args:
            key (str): The key of the sorted set.
            start (str): The minimum score of the range.
            end (str): The maximum score of the range.

        Returns:
            List[Tuple[str, float]]: A list of elements within the
            specified score range, with their scores.
        """
        return self.__db_manager.get_z_range_by_score(
            key=key,
            start=start,
            end=end
        )


class BuenbitTicker(TickerManagerDataBase):
    """
    Ticker manager for handling Buenbit API data and caching it.
    """

    def __init__(self):
        """
        Initialize BuenbitTicker with a BuenbitApiHandle instance.
        """
        super().__init__()
        self.buenbit_api = BuenbitApiHandle()

    def set_ticker(self, market_identifier: str = "btcars") -> None:
        """
        Fetch ticker data from Buenbit API and store it in the cache.

        Args:
            market_identifier (str, optional): The market identifier
            for the API request. Defaults to "btcars".
        """
        # Retrieves ticker data from Buenbit API
        data = self.buenbit_api.handle(market_identifier)

        # Creates a dictionary with price as key and timestamp as value
        value = {data["price"]: data["timestamp"]}

        # Stores the data in the cache
        self.set(key="prices", value=value)

    def get_average_price(self, since_timestamp, until_timestamp) -> Dict:
        """
        Calculate the average price of tickers within a specified
        timestamp range.

        Args:
            since_timestamp: The start of the time range.
            until_timestamp: The end of the time range.

        Returns:
            Dict: A dictionary containing the average price.
        """
        # get filtered data from redis
        range_data = self.get_zrange(
            key="prices",
            start=since_timestamp,
            end=until_timestamp
        )

        # obtain average price
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
        """
        Retrieve a list of tickers within a specified time range.

        Args:
            since_timestamp (str): The start of the time range.
            until_timestamp (str): The end of the time range.

        Returns:
            List[Dict]: A list of dictionaries, each containing a
            timestamp and a price.
        """
        # get filtered data from redis
        range_data = self.get_zrange(
            key="prices",
            start=since_timestamp,
            end=until_timestamp
        )

        # Processing to structure the query as a list of
        # dictionaries for the timestamp and price fields
        range_data = [
            {"timestamp": int(timestamp), "price": float(price)}
            for price, timestamp in range_data
        ]
        return range_data
