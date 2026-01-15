from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.coordinate import Coordinate


T = TypeVar("T", bound="PolygonArea")


@_attrs_define
class PolygonArea:
    """A polygon defined as a list of coordinates.

    The polygon is automatically closed, so repeating the first vertex is not required. Self-intersecting polygons are
    not supported.

        Attributes:
            type_ (str):  Example: polygon.
            outer (list[Coordinate]): List of coordinates defining the outline of the polygon.
    """

    type_: str
    outer: list[Coordinate]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        outer = []
        for outer_item_data in self.outer:
            outer_item = outer_item_data.to_dict()
            outer.append(outer_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "outer": outer,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.coordinate import Coordinate

        d = dict(src_dict)
        type_ = d.pop("type")

        outer = []
        _outer = d.pop("outer")
        for outer_item_data in _outer:
            outer_item = Coordinate.from_dict(outer_item_data)

            outer.append(outer_item)

        polygon_area = cls(
            type_=type_,
            outer=outer,
        )

        polygon_area.additional_properties = d
        return polygon_area

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
