from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Location")


@_attrs_define
class Location:
    """Location on the Earth

    Example:
        {'lat': 52.531677, 'lng': 13.381777}

    Attributes:
        lat (float): Location of a point on the Earth north or south of the equator in decimal degrees. Example:
            52.531677.
        lng (float): Location of a place on the Earth east or west of the prime meridian in decimal degrees. Example:
            13.381777.
        elv (float | Unset): Ellipsoid(geodetic) height in meters. Difference between the WGS84 ellipsoid and a point on
            the Earth’s surface.
            Note: Similar elevation can be obtained from a GPS receiver.
             Example: 512.5.
    """

    lat: float
    lng: float
    elv: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        lat = self.lat

        lng = self.lng

        elv = self.elv

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "lat": lat,
            "lng": lng,
        })
        if elv is not UNSET:
            field_dict["elv"] = elv

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        lat = d.pop("lat")

        lng = d.pop("lng")

        elv = d.pop("elv", UNSET)

        location = cls(
            lat=lat,
            lng=lng,
            elv=elv,
        )

        location.additional_properties = d
        return location

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
