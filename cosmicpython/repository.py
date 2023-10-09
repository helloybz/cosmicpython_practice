from abc import ABC, abstractmethod

from .model import Batch


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, batch: Batch) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, reference: object) -> Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def add(self, batch: Batch) -> None:
        ...
