from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DisplayResponseCoordinate")


@_attrs_define
class DisplayResponseCoordinate:
    """
    Attributes:
        lat (float): Latitude of the address. For example: `"52.19404"`
        lng (float): Longitude of the address. For example: `"8.80135"`
    """

    lat: float
    lng: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        lat = self.lat

        lng = self.lng

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "lat": lat,
            "lng": lng,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        lat = d.pop("lat")

        lng = d.pop("lng")

        display_response_coordinate = cls(
            lat=lat,
            lng=lng,
        )

        display_response_coordinate.additional_properties = d
        return display_response_coordinate

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
