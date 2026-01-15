from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Access")


@_attrs_define
class Access:
    """
    Attributes:
        automobiles (bool | Unset): Applicable to automobiles.

            - `true`: The road allows automobiles.
            - `false`: The road doesn't allow automobiles.
        bicycles (bool | Unset): Applicable to bicycles.

            - `true`: The road allows bicycles.
            - `false`: The road doesn't allow bicycles.
        buses (bool | Unset): Applicable to buses.

            - `true`: The road allows buses.
            - `false`: The road doesn't allow buses.
        carpools (bool | Unset): Applicable to carpools.

            - `true`: The road allows carpooling.
            - `false`: The road doesn't allow carpooling.
        deliveries (bool | Unset): Applicable to deliveries.

            - `true`: The road allows deliveries.
            - `false`: The road doesn't allow deliveries.
        emergency_vehicles (bool | Unset): Applicable to emergency vehicles.

            - `true`: The road allows emergency vehicles.
            - `false`: The road doesn't allow emergency vehicles.
        motorcycles (bool | Unset): Applicable to motorcycles.

            - `true`: The road allows motorcycles.
            - `false`: The road doesn't allow motorcycles.
        pedestrians (bool | Unset): Applicable to pedestrians.

            - `true`: The road allows pedestrians.
            - `false`: The road doesn't allow pedestrians.
        taxis (bool | Unset): Applicable to taxis.

            - `true`: The road allows taxis.
            - `false`: The road doesn't allow taxis.
        through_traffic (bool | Unset): Applicable to through traffic.

            - `true`: The road allows through traffic.
            - `false`: The road doesn't allow through traffic.
        trucks (bool | Unset): Applicable to trucks.

            - `true`: The road allows trucks.
            - `false`: The road doesn't allow trucks.
    """

    automobiles: bool | Unset = UNSET
    bicycles: bool | Unset = UNSET
    buses: bool | Unset = UNSET
    carpools: bool | Unset = UNSET
    deliveries: bool | Unset = UNSET
    emergency_vehicles: bool | Unset = UNSET
    motorcycles: bool | Unset = UNSET
    pedestrians: bool | Unset = UNSET
    taxis: bool | Unset = UNSET
    through_traffic: bool | Unset = UNSET
    trucks: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        automobiles = self.automobiles

        bicycles = self.bicycles

        buses = self.buses

        carpools = self.carpools

        deliveries = self.deliveries

        emergency_vehicles = self.emergency_vehicles

        motorcycles = self.motorcycles

        pedestrians = self.pedestrians

        taxis = self.taxis

        through_traffic = self.through_traffic

        trucks = self.trucks

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if automobiles is not UNSET:
            field_dict["automobiles"] = automobiles
        if bicycles is not UNSET:
            field_dict["bicycles"] = bicycles
        if buses is not UNSET:
            field_dict["buses"] = buses
        if carpools is not UNSET:
            field_dict["carpools"] = carpools
        if deliveries is not UNSET:
            field_dict["deliveries"] = deliveries
        if emergency_vehicles is not UNSET:
            field_dict["emergencyVehicles"] = emergency_vehicles
        if motorcycles is not UNSET:
            field_dict["motorcycles"] = motorcycles
        if pedestrians is not UNSET:
            field_dict["pedestrians"] = pedestrians
        if taxis is not UNSET:
            field_dict["taxis"] = taxis
        if through_traffic is not UNSET:
            field_dict["throughTraffic"] = through_traffic
        if trucks is not UNSET:
            field_dict["trucks"] = trucks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        automobiles = d.pop("automobiles", UNSET)

        bicycles = d.pop("bicycles", UNSET)

        buses = d.pop("buses", UNSET)

        carpools = d.pop("carpools", UNSET)

        deliveries = d.pop("deliveries", UNSET)

        emergency_vehicles = d.pop("emergencyVehicles", UNSET)

        motorcycles = d.pop("motorcycles", UNSET)

        pedestrians = d.pop("pedestrians", UNSET)

        taxis = d.pop("taxis", UNSET)

        through_traffic = d.pop("throughTraffic", UNSET)

        trucks = d.pop("trucks", UNSET)

        access = cls(
            automobiles=automobiles,
            bicycles=bicycles,
            buses=buses,
            carpools=carpools,
            deliveries=deliveries,
            emergency_vehicles=emergency_vehicles,
            motorcycles=motorcycles,
            pedestrians=pedestrians,
            taxis=taxis,
            through_traffic=through_traffic,
            trucks=trucks,
        )

        access.additional_properties = d
        return access

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
