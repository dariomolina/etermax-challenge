from abc import ABC, abstractmethod
from typing import Dict

from django.core.cache import cache


class RedisCacheManagerBase(ABC):

    @staticmethod
    @abstractmethod
    def set_data(key: str, value: Dict) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_data(request) -> Dict:
        raise NotImplementedError


class RedisCacheManager(RedisCacheManagerBase):

    @staticmethod
    def set_data(key: str, value: Dict, timeout=None) -> None:
        cache.set(key, value, timeout=timeout)

    @staticmethod
    def get_data(key: str) -> Dict:
        value = cache.get(key)
        return value
