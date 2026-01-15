from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MapView")


@_attrs_define
class MapView:
    """
    Attributes:
        west (float): Longitude of the western-side of the box. For example: "8.80068"
        south (float): Latitude of the southern-side of the box. For example: "52.19333"
        east (float): Longitude of the eastern-side of the box. For example: "8.8167"
        north (float): Latitude of the northern-side of the box. For example: "52.19555"
    """

    west: float
    south: float
    east: float
    north: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        west = self.west

        south = self.south

        east = self.east

        north = self.north

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "west": west,
            "south": south,
            "east": east,
            "north": north,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        west = d.pop("west")

        south = d.pop("south")

        east = d.pop("east")

        north = d.pop("north")

        map_view = cls(
            west=west,
            south=south,
            east=east,
            north=north,
        )

        map_view.additional_properties = d
        return map_view

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
