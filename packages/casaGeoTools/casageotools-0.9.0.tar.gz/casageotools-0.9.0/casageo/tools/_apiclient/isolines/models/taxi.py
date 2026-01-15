from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Taxi")


@_attrs_define
class Taxi:
    """Taxi-specific parameters

    Attributes:
        allow_drive_through_taxi_roads (bool | Unset): Specifies if a vehicle is allowed to drive through taxi-only
            roads and lanes. Even if
            this option is set to `false`, the vehicle is still allowed on taxi-only roads at the
            start of the route and at the destination.
             Default: True.
    """

    allow_drive_through_taxi_roads: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allow_drive_through_taxi_roads = self.allow_drive_through_taxi_roads

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allow_drive_through_taxi_roads is not UNSET:
            field_dict["allowDriveThroughTaxiRoads"] = allow_drive_through_taxi_roads

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        allow_drive_through_taxi_roads = d.pop("allowDriveThroughTaxiRoads", UNSET)

        taxi = cls(
            allow_drive_through_taxi_roads=allow_drive_through_taxi_roads,
        )

        taxi.additional_properties = d
        return taxi

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
