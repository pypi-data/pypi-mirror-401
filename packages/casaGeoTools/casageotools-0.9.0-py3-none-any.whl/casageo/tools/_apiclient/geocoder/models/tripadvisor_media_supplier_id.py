from enum import Enum


class TripadvisorMediaSupplierId(str, Enum):
    TRIPADVISOR = "tripadvisor"

    def __str__(self) -> str:
        return str(self.value)
