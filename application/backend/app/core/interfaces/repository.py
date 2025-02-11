from abc import ABC, abstractmethod
from typing import List


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> List:
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, filter_data: dict):
        raise NotImplementedError

    async def find_some(self, filter_data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, filter_data: dict, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update_many(self, filter_data: dict, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, filter_data: dict):
        raise NotImplementedError
