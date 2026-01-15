from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.truck_fuel_maximum_truck_class import TruckFuelMaximumTruckClass
from ..models.truck_fuel_type import TruckFuelType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fuel_price import FuelPrice


T = TypeVar("T", bound="TruckFuel")


@_attrs_define
class TruckFuel:
    """
    Attributes:
        type_ (TruckFuelType): **BETA, RESTRICTED**

            The type of truck fuel

            Description of supported values:

            - **BETA, RESTRICTED** `truck_cng`: compressed natural gas (CNG) fuel for truck
            - **BETA, RESTRICTED** `truck_diesel`: diesel fuel for truck
            - **BETA, RESTRICTED** `truck_hydrogen`: hydrogen fuel for truck
            - **BETA, RESTRICTED** `truck_lng`: liquefied natural gas (LNG) fuel for truck
        available (bool): **BETA, RESTRICTED**

            When set to:
            - `true` indicates that this type of truck fuel is available at this place
            - `false` indicates that this type of truck fuel is not available at this place
        maximum_truck_class (TruckFuelMaximumTruckClass | Unset): **BETA, RESTRICTED**

            The truck classes

            Description of supported values:

            - **BETA, RESTRICTED** `heavy`: Medium and Heavy trucks are allowed to fuel in the gas station
            - **BETA, RESTRICTED** `medium`: Only medium size truck is allowed to fuel in the gas station
        price (FuelPrice | Unset):
        large_nozzle (bool | Unset): **BETA, RESTRICTED**

            When set to:
            - `true`: indicates that this Place has Truck diesel pumps with large nozzles
            - `false`: indicates that this Place does not have Truck diesel pumps with large nozzles
    """

    type_: TruckFuelType
    available: bool
    maximum_truck_class: TruckFuelMaximumTruckClass | Unset = UNSET
    price: FuelPrice | Unset = UNSET
    large_nozzle: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        available = self.available

        maximum_truck_class: str | Unset = UNSET
        if not isinstance(self.maximum_truck_class, Unset):
            maximum_truck_class = self.maximum_truck_class.value

        price: dict[str, Any] | Unset = UNSET
        if not isinstance(self.price, Unset):
            price = self.price.to_dict()

        large_nozzle = self.large_nozzle

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "available": available,
        })
        if maximum_truck_class is not UNSET:
            field_dict["maximumTruckClass"] = maximum_truck_class
        if price is not UNSET:
            field_dict["price"] = price
        if large_nozzle is not UNSET:
            field_dict["largeNozzle"] = large_nozzle

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fuel_price import FuelPrice

        d = dict(src_dict)
        type_ = TruckFuelType(d.pop("type"))

        available = d.pop("available")

        _maximum_truck_class = d.pop("maximumTruckClass", UNSET)
        maximum_truck_class: TruckFuelMaximumTruckClass | Unset
        if isinstance(_maximum_truck_class, Unset):
            maximum_truck_class = UNSET
        else:
            maximum_truck_class = TruckFuelMaximumTruckClass(_maximum_truck_class)

        _price = d.pop("price", UNSET)
        price: FuelPrice | Unset
        if isinstance(_price, Unset):
            price = UNSET
        else:
            price = FuelPrice.from_dict(_price)

        large_nozzle = d.pop("largeNozzle", UNSET)

        truck_fuel = cls(
            type_=type_,
            available=available,
            maximum_truck_class=maximum_truck_class,
            price=price,
            large_nozzle=large_nozzle,
        )

        truck_fuel.additional_properties = d
        return truck_fuel

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
