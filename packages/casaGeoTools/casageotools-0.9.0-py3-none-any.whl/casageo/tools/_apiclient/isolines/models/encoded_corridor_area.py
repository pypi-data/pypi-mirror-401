from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EncodedCorridorArea")


@_attrs_define
class EncodedCorridorArea:
    """A polygon defined as a [Flexible Polyline](https://github.com/heremaps/flexible-polyline) encoded string
    and with a specified radius that defines an area.

        Attributes:
            type_ (str):  Example: encodedCorridor.
            polyline (str): [Flexible Polyline](https://github.com/heremaps/flexible-polyline) that defines a supporting
                structure for a corridor.
                Notes:
                * Support only 2D polyline (without `elevation` specified).
                * Minimum count of vertices in polyline is 2.
                * Maximum count of vertices in polyline is 100.
                 Example: BFoz5xJ67i1B1B7PzIhaxL7Y.
            radius (int): The width in meters of the corridor determines the outline of the polygon.
    """

    type_: str
    polyline: str
    radius: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        polyline = self.polyline

        radius = self.radius

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "polyline": polyline,
            "radius": radius,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        polyline = d.pop("polyline")

        radius = d.pop("radius")

        encoded_corridor_area = cls(
            type_=type_,
            polyline=polyline,
            radius=radius,
        )

        encoded_corridor_area.additional_properties = d
        return encoded_corridor_area

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
