from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SinglePrice")


@_attrs_define
class SinglePrice:
    """
    Attributes:
        type_ (str): Type of price represented by this object. The API customer is responsible for correctly visualizing
            the pricing model. As it is possible to extend the supported price types in the future,
            the price information should be hidden when an unknown type is encountered.

            Available price types are:

              * `value` - A single value.
              * `range` - A range value that includes a minimum and maximum price.
        currency (str): Local currency of the price compliant to ISO 4217
        value (float): The price value
        estimated (bool | Unset): Attribute value is `true` if the fare price is estimated, `false` if it is an exact
            value. Default: False.
        unit (int | Unset): Duration in seconds. Example: 198.
    """

    type_: str
    currency: str
    value: float
    estimated: bool | Unset = False
    unit: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        currency = self.currency

        value = self.value

        estimated = self.estimated

        unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "currency": currency,
            "value": value,
        })
        if estimated is not UNSET:
            field_dict["estimated"] = estimated
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        currency = d.pop("currency")

        value = d.pop("value")

        estimated = d.pop("estimated", UNSET)

        unit = d.pop("unit", UNSET)

        single_price = cls(
            type_=type_,
            currency=currency,
            value=value,
            estimated=estimated,
            unit=unit,
        )

        single_price.additional_properties = d
        return single_price

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
