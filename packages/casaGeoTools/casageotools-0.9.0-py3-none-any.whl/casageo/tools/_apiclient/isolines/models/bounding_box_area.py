from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BoundingBoxArea")


@_attrs_define
class BoundingBoxArea:
    """A bounding box defined by two longitudes and two latitudes.

    Attributes:
        type_ (str):  Example: boundingBox.
        north (float): Latitude in WGS-84 degrees of the northern boundary of the box. Example: 30.0.
        south (float): Latitude in WGS-84 degrees of the southern boundary of the box. Example: 30.0.
        east (float): Longitude in WGS-84 degrees of the eastern boundary of the box Example: 30.0.
        west (float): Longitude in WGS-84 degrees of the western boundary of the box. Example: 30.0.
    """

    type_: str
    north: float
    south: float
    east: float
    west: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        north = self.north

        south = self.south

        east = self.east

        west = self.west

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "north": north,
            "south": south,
            "east": east,
            "west": west,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        north = d.pop("north")

        south = d.pop("south")

        east = d.pop("east")

        west = d.pop("west")

        bounding_box_area = cls(
            type_=type_,
            north=north,
            south=south,
            east=east,
            west=west,
        )

        bounding_box_area.additional_properties = d
        return bounding_box_area

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
