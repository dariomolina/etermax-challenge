from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from django_redis import get_redis_connection

redis_client = get_redis_connection()


class RedisCacheManagerBase(ABC):
    """
    Abstract base class for managing Redis cache operations.
    """

    @staticmethod
    @abstractmethod
    def set_data(key: str, value: Dict) -> None:
        """
        Set a key-value pair in the Redis cache.

        Args:
            key (str): The key under which the value should be stored.
            value (Dict): The value to be stored.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_z_range_by_score(
        key: str,
        start: str,
        end: str
    ) -> List[Tuple[bytes, str]]:
        """
        Retrieve a range of elements from a sorted set in the Redis cache by score.

        Args:
            key (str): The key of the sorted set.
            start (str): The minimum score of the range.
            end (str): The maximum score of the range.

        Returns:
            Dict: The elements within the specified score range.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError


class RedisCacheManager(RedisCacheManagerBase):
    """
    Concrete implementation of RedisCacheManagerBase
    for managing Redis cache operations.
    """

    @staticmethod
    def set_data(key: str, value: Dict) -> None:
        """
        Set a key-value pair in the Redis cache.

        Args:
            key (str): The key under which the value should be stored.
            value (Dict): The value to be stored.
        """
        try:
            redis_client.zadd(key, value)
        except Exception as e:
            raise RuntimeError(f"Error setting data in Redis cache: {e}")

    @staticmethod
    def get_z_range_by_score(
        key: str,
        start: str,
        end: str
    ) -> List[Tuple[bytes, str]]:
        """
        Retrieve a range of elements from a sorted set in the Redis cache by score.

        Args:
            key (str): The key of the sorted set.
            start (str): The minimum score of the range.
            end (str): The maximum score of the range.

        Returns:
            List[Tuple[bytes, str]]: A list of elements within the specified score range, with their scores.
        """
        try:
            range_data = redis_client.zrangebyscore(key, start, end, withscores=True)
        except Exception as e:
            raise RuntimeError(f"Error getting data from Redis cache: {e}")

        return range_data
