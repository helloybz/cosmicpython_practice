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
