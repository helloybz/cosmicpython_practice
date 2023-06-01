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
        self.qty = qty
        self.eta = eta

    def allocate(self, orderline: OrderLine) -> None:
        if orderline.sku == self.sku:
            self.qty -= orderline.qty
        else:
            raise ValueError("SKU not matched.")

    @property
    def available_quantity(self) -> int:
        return self.qty
