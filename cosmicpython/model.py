from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: date | None) -> None:
        self.ref = ref
        self.sku = sku
        self.eta = eta
        self._purchased_qty = qty
        self._allocated_lines: set[OrderLine] = set()

    def allocate(self, orderline: OrderLine) -> None:
        if self.can_allocate(orderline):
            self._allocated_lines.add(orderline)

    def deallocate(self, orderline: OrderLine) -> None:
        if orderline in self._allocated_lines:
            self._allocated_lines.remove(orderline)

    @property
    def allocated_qty(self) -> int:
        return sum(orderine.qty for orderine in self._allocated_lines)

    @property
    def available_quantity(self) -> int:
        return self._purchased_qty - self.allocated_qty

    def can_allocate(self, orderline: OrderLine) -> bool:
        return self.sku == orderline.sku and self.available_quantity >= orderline.qty

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Batch) and self.ref == other.ref

    def __hash__(self) -> int:
        return hash(self.ref)

    def __gt__(self, other) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


def allocate(line: OrderLine, batches: list[Batch]) -> str:
    best_batch = next(batch for batch in sorted(batches) if batch.can_allocate(line))

    best_batch.allocate(line)

    return best_batch.ref
