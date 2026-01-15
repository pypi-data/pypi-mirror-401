from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Polygon")


@_attrs_define
class Polygon:
    """A polygon is described by a boundary outer ring and a possible set of inner rings or holes.

    Attributes:
        outer (str | Unset): A special case of a Polyline where the first and last elements in the coordinates array are
            equivalent. Encoded as a string in [Flexible Polyline](https://github.com/heremaps/flexible-polyline) format.
            Coordinates are in the WGS84 coordinate system, including `Elevation` (if present). Example:
            BGk0owkBggpgrE1K6algB4KlgB3K3KlgB4KlgBmgB1KmgBqF2KkQA6a.
        inner (list[str] | Unset): A list of inner rings or holes for the polygon in the form of a list of LinearRings.
    """

    outer: str | Unset = UNSET
    inner: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        outer = self.outer

        inner: list[str] | Unset = UNSET
        if not isinstance(self.inner, Unset):
            inner = self.inner

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if outer is not UNSET:
            field_dict["outer"] = outer
        if inner is not UNSET:
            field_dict["inner"] = inner

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        outer = d.pop("outer", UNSET)

        inner = cast(list[str], d.pop("inner", UNSET))

        polygon = cls(
            outer=outer,
            inner=inner,
        )

        polygon.additional_properties = d
        return polygon

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
