from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ev_availability_station import EvAvailabilityStation


T = TypeVar("T", bound="EvAvailabilityAttributes")


@_attrs_define
class EvAvailabilityAttributes:
    """
    Attributes:
        stations (list[EvAvailabilityStation] | Unset): List of EV stations at the place (Currently only one is
            expected)
    """

    stations: list[EvAvailabilityStation] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        stations: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.stations, Unset):
            stations = []
            for stations_item_data in self.stations:
                stations_item = stations_item_data.to_dict()
                stations.append(stations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if stations is not UNSET:
            field_dict["stations"] = stations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ev_availability_station import EvAvailabilityStation

        d = dict(src_dict)
        _stations = d.pop("stations", UNSET)
        stations: list[EvAvailabilityStation] | Unset = UNSET
        if _stations is not UNSET:
            stations = []
            for stations_item_data in _stations:
                stations_item = EvAvailabilityStation.from_dict(stations_item_data)

                stations.append(stations_item)

        ev_availability_attributes = cls(
            stations=stations,
        )

        ev_availability_attributes.additional_properties = d
        return ev_availability_attributes

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
