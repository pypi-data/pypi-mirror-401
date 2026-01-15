from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FuelPrice")


@_attrs_define
class FuelPrice:
    """
    Attributes:
        amount (float | Unset): **BETA, RESTRICTED**

            Real-time price value for a volume of 1 unit
        currency (str | Unset): **BETA, RESTRICTED**

            Currency in which the amount is expressed
        unit (str | Unset): **BETA, RESTRICTED**

            Unit of measurement for the fuel quantity:
            - `l` litres
            - `gal` gallons
            - `bbl` barrels
            - `kg` kilogram
            - `m3` cubic meters
    """

    amount: float | Unset = UNSET
    currency: str | Unset = UNSET
    unit: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        currency = self.currency

        unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount is not UNSET:
            field_dict["amount"] = amount
        if currency is not UNSET:
            field_dict["currency"] = currency
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount = d.pop("amount", UNSET)

        currency = d.pop("currency", UNSET)

        unit = d.pop("unit", UNSET)

        fuel_price = cls(
            amount=amount,
            currency=currency,
            unit=unit,
        )

        fuel_price.additional_properties = d
        return fuel_price

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
