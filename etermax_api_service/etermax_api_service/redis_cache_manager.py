from abc import ABC, abstractmethod
from typing import Dict

from django_redis import get_redis_connection

redis_client = get_redis_connection()


class RedisCacheManagerBase(ABC):

    @staticmethod
    @abstractmethod
    def set_data(key: str, value: Dict) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_data(key: str) -> Dict:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_z_range_by_score(key: str, start: str, end: str) -> Dict:
        raise NotImplementedError


class RedisCacheManager(RedisCacheManagerBase):

    @staticmethod
    def set_data(key: str, value: Dict, timeout=None) -> None:
        redis_client.zadd(key, value)

    @staticmethod
    def get_data(key: str) -> Dict:
        value = redis_client.get(key)
        return value

    @staticmethod
    def get_z_range_by_score(key: str, start: str, end: str):
        range_data = redis_client.zrangebyscore(key, start, end, withscores=True)
        return range_data
