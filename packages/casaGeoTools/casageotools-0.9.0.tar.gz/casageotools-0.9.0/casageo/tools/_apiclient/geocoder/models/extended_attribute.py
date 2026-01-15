from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ev_availability_attributes import EvAvailabilityAttributes
    from ..models.ev_charging_attributes import EvChargingAttributes
    from ..models.fuel_station_attributes import FuelStationAttributes
    from ..models.truck_amenity_generic import TruckAmenityGeneric
    from ..models.truck_amenity_showers import TruckAmenityShowers


T = TypeVar("T", bound="ExtendedAttribute")


@_attrs_define
class ExtendedAttribute:
    """
    Attributes:
        ev_station (EvChargingAttributes | Unset):
        ev_availability (EvAvailabilityAttributes | Unset):
        fuel_station (FuelStationAttributes | Unset):
        truck_amenities (list[TruckAmenityGeneric | TruckAmenityShowers] | Unset): **BETA, RESTRICTED**

            This field contains a listing of acceptable key-value pairs for amenities at places useful for truck drivers.
    """

    ev_station: EvChargingAttributes | Unset = UNSET
    ev_availability: EvAvailabilityAttributes | Unset = UNSET
    fuel_station: FuelStationAttributes | Unset = UNSET
    truck_amenities: list[TruckAmenityGeneric | TruckAmenityShowers] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.truck_amenity_generic import TruckAmenityGeneric

        ev_station: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ev_station, Unset):
            ev_station = self.ev_station.to_dict()

        ev_availability: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ev_availability, Unset):
            ev_availability = self.ev_availability.to_dict()

        fuel_station: dict[str, Any] | Unset = UNSET
        if not isinstance(self.fuel_station, Unset):
            fuel_station = self.fuel_station.to_dict()

        truck_amenities: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.truck_amenities, Unset):
            truck_amenities = []
            for truck_amenities_item_data in self.truck_amenities:
                truck_amenities_item: dict[str, Any]
                if isinstance(truck_amenities_item_data, TruckAmenityGeneric):
                    truck_amenities_item = truck_amenities_item_data.to_dict()
                else:
                    truck_amenities_item = truck_amenities_item_data.to_dict()

                truck_amenities.append(truck_amenities_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ev_station is not UNSET:
            field_dict["evStation"] = ev_station
        if ev_availability is not UNSET:
            field_dict["evAvailability"] = ev_availability
        if fuel_station is not UNSET:
            field_dict["fuelStation"] = fuel_station
        if truck_amenities is not UNSET:
            field_dict["truckAmenities"] = truck_amenities

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ev_availability_attributes import EvAvailabilityAttributes
        from ..models.ev_charging_attributes import EvChargingAttributes
        from ..models.fuel_station_attributes import FuelStationAttributes
        from ..models.truck_amenity_generic import TruckAmenityGeneric
        from ..models.truck_amenity_showers import TruckAmenityShowers

        d = dict(src_dict)
        _ev_station = d.pop("evStation", UNSET)
        ev_station: EvChargingAttributes | Unset
        if isinstance(_ev_station, Unset):
            ev_station = UNSET
        else:
            ev_station = EvChargingAttributes.from_dict(_ev_station)

        _ev_availability = d.pop("evAvailability", UNSET)
        ev_availability: EvAvailabilityAttributes | Unset
        if isinstance(_ev_availability, Unset):
            ev_availability = UNSET
        else:
            ev_availability = EvAvailabilityAttributes.from_dict(_ev_availability)

        _fuel_station = d.pop("fuelStation", UNSET)
        fuel_station: FuelStationAttributes | Unset
        if isinstance(_fuel_station, Unset):
            fuel_station = UNSET
        else:
            fuel_station = FuelStationAttributes.from_dict(_fuel_station)

        _truck_amenities = d.pop("truckAmenities", UNSET)
        truck_amenities: list[TruckAmenityGeneric | TruckAmenityShowers] | Unset = UNSET
        if _truck_amenities is not UNSET:
            truck_amenities = []
            for truck_amenities_item_data in _truck_amenities:

                def _parse_truck_amenities_item(
                    data: object,
                ) -> TruckAmenityGeneric | TruckAmenityShowers:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        truck_amenities_item_type_0 = TruckAmenityGeneric.from_dict(
                            data
                        )

                        return truck_amenities_item_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    truck_amenities_item_type_1 = TruckAmenityShowers.from_dict(data)

                    return truck_amenities_item_type_1

                truck_amenities_item = _parse_truck_amenities_item(
                    truck_amenities_item_data
                )

                truck_amenities.append(truck_amenities_item)

        extended_attribute = cls(
            ev_station=ev_station,
            ev_availability=ev_availability,
            fuel_station=fuel_station,
            truck_amenities=truck_amenities,
        )

        extended_attribute.additional_properties = d
        return extended_attribute

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
