from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.coordinate import Coordinate


T = TypeVar("T", bound="CorridorArea")


@_attrs_define
class CorridorArea:
    """A polyline with a specified radius in meters that defines an area.

    Attributes:
        type_ (str):  Example: corridor.
        polyline (list[Coordinate]): List of coordinates defining polyline.
        radius (int): The width in meters of the corridor determines the outline of the polygon.
    """

    type_: str
    polyline: list[Coordinate]
    radius: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        polyline = []
        for polyline_item_data in self.polyline:
            polyline_item = polyline_item_data.to_dict()
            polyline.append(polyline_item)

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
        from ..models.coordinate import Coordinate

        d = dict(src_dict)
        type_ = d.pop("type")

        polyline = []
        _polyline = d.pop("polyline")
        for polyline_item_data in _polyline:
            polyline_item = Coordinate.from_dict(polyline_item_data)

            polyline.append(polyline_item)

        radius = d.pop("radius")

        corridor_area = cls(
            type_=type_,
            polyline=polyline,
            radius=radius,
        )

        corridor_area.additional_properties = d
        return corridor_area

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
