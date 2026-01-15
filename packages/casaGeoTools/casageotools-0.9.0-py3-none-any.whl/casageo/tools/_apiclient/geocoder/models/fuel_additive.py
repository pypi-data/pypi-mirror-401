from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.fuel_additive_type import FuelAdditiveType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fuel_price import FuelPrice


T = TypeVar("T", bound="FuelAdditive")


@_attrs_define
class FuelAdditive:
    """
    Attributes:
        type_ (FuelAdditiveType): **BETA, RESTRICTED**

            Indicates the type or brand of Diesel Emission Fluid (DEF) available.
        available (bool): **BETA, RESTRICTED**

            When set to:
            - `true` indicates that Diesel Emission Fluid (DEF) is available at this place
            - `false` indicates that Diesel Emission Fluid (DEF) is not available at this place
        in_cans (bool | Unset): **BETA, RESTRICTED**

            When set to:
            - `true` indicates that Diesel Emission Fluid (DEF) is available in cans.
            - `false` indicates that Diesel Emission Fluid (DEF) is not available in cans.
        at_the_pump (bool | Unset): **BETA, RESTRICTED**

            When set to:
            - `true` indicates that Diesel Emission Fluid (DEF) is available at the pump.
            - `false` indicates that Diesel Emission Fluid (DEF) is not available at the pump.
        price (FuelPrice | Unset):
    """

    type_: FuelAdditiveType
    available: bool
    in_cans: bool | Unset = UNSET
    at_the_pump: bool | Unset = UNSET
    price: FuelPrice | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        available = self.available

        in_cans = self.in_cans

        at_the_pump = self.at_the_pump

        price: dict[str, Any] | Unset = UNSET
        if not isinstance(self.price, Unset):
            price = self.price.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "available": available,
        })
        if in_cans is not UNSET:
            field_dict["inCans"] = in_cans
        if at_the_pump is not UNSET:
            field_dict["atThePump"] = at_the_pump
        if price is not UNSET:
            field_dict["price"] = price

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fuel_price import FuelPrice

        d = dict(src_dict)
        type_ = FuelAdditiveType(d.pop("type"))

        available = d.pop("available")

        in_cans = d.pop("inCans", UNSET)

        at_the_pump = d.pop("atThePump", UNSET)

        _price = d.pop("price", UNSET)
        price: FuelPrice | Unset
        if isinstance(_price, Unset):
            price = UNSET
        else:
            price = FuelPrice.from_dict(_price)

        fuel_additive = cls(
            type_=type_,
            available=available,
            in_cans=in_cans,
            at_the_pump=at_the_pump,
            price=price,
        )

        fuel_additive.additional_properties = d
        return fuel_additive

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
