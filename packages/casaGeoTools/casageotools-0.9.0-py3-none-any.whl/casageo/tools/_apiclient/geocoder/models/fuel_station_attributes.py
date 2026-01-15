from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.car_fuel import CarFuel
    from ..models.truck_fuel import TruckFuel


T = TypeVar("T", bound="FuelStationAttributes")


@_attrs_define
class FuelStationAttributes:
    """
    Attributes:
        fuel_types (list[CarFuel | TruckFuel] | Unset): **BETA, RESTRICTED**

            List of fuel types available or not available at this place
        pay_at_the_pump (bool | Unset): **BETA, RESTRICTED**

            When set to:
            - `true` indicates that payment can be made at fuel pumps via credit card or other method at this place
            - `false` indicates that payment can not be made at fuel pumps via credit card or other method at this place
        high_volume_pumps (bool | Unset): **BETA, RESTRICTED**

            When set to:
            - `true` indicates that high volume pumps for commercial vehicles are available at this place
            - `false` indicates that high volume pumps for commercial vehicles are not available at this place
    """

    fuel_types: list[CarFuel | TruckFuel] | Unset = UNSET
    pay_at_the_pump: bool | Unset = UNSET
    high_volume_pumps: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.car_fuel import CarFuel

        fuel_types: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.fuel_types, Unset):
            fuel_types = []
            for fuel_types_item_data in self.fuel_types:
                fuel_types_item: dict[str, Any]
                if isinstance(fuel_types_item_data, CarFuel):
                    fuel_types_item = fuel_types_item_data.to_dict()
                else:
                    fuel_types_item = fuel_types_item_data.to_dict()

                fuel_types.append(fuel_types_item)

        pay_at_the_pump = self.pay_at_the_pump

        high_volume_pumps = self.high_volume_pumps

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fuel_types is not UNSET:
            field_dict["fuelTypes"] = fuel_types
        if pay_at_the_pump is not UNSET:
            field_dict["payAtThePump"] = pay_at_the_pump
        if high_volume_pumps is not UNSET:
            field_dict["highVolumePumps"] = high_volume_pumps

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.car_fuel import CarFuel
        from ..models.truck_fuel import TruckFuel

        d = dict(src_dict)
        _fuel_types = d.pop("fuelTypes", UNSET)
        fuel_types: list[CarFuel | TruckFuel] | Unset = UNSET
        if _fuel_types is not UNSET:
            fuel_types = []
            for fuel_types_item_data in _fuel_types:

                def _parse_fuel_types_item(data: object) -> CarFuel | TruckFuel:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        fuel_types_item_type_0 = CarFuel.from_dict(data)

                        return fuel_types_item_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    fuel_types_item_type_1 = TruckFuel.from_dict(data)

                    return fuel_types_item_type_1

                fuel_types_item = _parse_fuel_types_item(fuel_types_item_data)

                fuel_types.append(fuel_types_item)

        pay_at_the_pump = d.pop("payAtThePump", UNSET)

        high_volume_pumps = d.pop("highVolumePumps", UNSET)

        fuel_station_attributes = cls(
            fuel_types=fuel_types,
            pay_at_the_pump=pay_at_the_pump,
            high_volume_pumps=high_volume_pumps,
        )

        fuel_station_attributes.additional_properties = d
        return fuel_station_attributes

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
