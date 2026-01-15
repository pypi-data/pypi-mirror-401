from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EncodedPolygonArea")


@_attrs_define
class EncodedPolygonArea:
    """A polygon defined as a [Flexible Polyline](https://github.com/heremaps/flexible-polyline) encoded string.

    The polygon is automatically closed, so repeating the first vertex is not required.

        Attributes:
            type_ (str):  Example: encodedPolygon.
            outer (str): [Flexible Polyline](https://github.com/heremaps/flexible-polyline) that defines the outline of the
                polygon.
                Notes:
                * Support only 2D polyline (without `elevation` specified).
                * Minimum count of vertices in polygon is 3.
                * Maximum count of vertices in polygon is 16.
                 Example: BFoz5xJ67i1B1B7PzIhaxL7Y.
    """

    type_: str
    outer: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        outer = self.outer

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "outer": outer,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        outer = d.pop("outer")

        encoded_polygon_area = cls(
            type_=type_,
            outer=outer,
        )

        encoded_polygon_area.additional_properties = d
        return encoded_polygon_area

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
