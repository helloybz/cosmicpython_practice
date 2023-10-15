from abc import ABC, abstractmethod

from .model import Batch


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, batch: Batch) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, reference: str) -> Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def add(self, batch: Batch) -> None:
        ...

    def get(self, reference):
        ...

    def list(self):
        ...


class FakeRepository(AbstractRepository):
    def __init__(self, batches: list[Batch]):
        self._batches = set(batches)

    def add(self, batch: Batch) -> None:
        self._batches.add(batch)

    def get(self, reference: str) -> Batch:
        return next(batch for batch in self._batches if batch.ref == reference)

    def list(self) -> list[Batch]:
        return list(self._batches)
