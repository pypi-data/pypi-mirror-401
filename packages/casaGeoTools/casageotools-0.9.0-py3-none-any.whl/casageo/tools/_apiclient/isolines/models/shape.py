from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Shape")


@_attrs_define
class Shape:
    """A struct used to control the shape of the returned isolines.

    Attributes:
        max_points (int | Unset): Limits the number of points in the resulting isoline geometry.

            If the isoline consists of multiple components, the sum of points from all components is considered.
            This parameter doesn't affect performance. Look at `optimizeFor` parameter to optimize for performance.

            Notes:
              Quality of isolines degrades as maxPoints value is decreased,
              It is Recommended use `maxPoints` value greater than 100 for optimal quality isolines.
             Example: 150.
        max_resolution (int | Unset): Distance in meters. Default: 0. Example: 189.
    """

    max_points: int | Unset = UNSET
    max_resolution: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_points = self.max_points

        max_resolution = self.max_resolution

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_points is not UNSET:
            field_dict["maxPoints"] = max_points
        if max_resolution is not UNSET:
            field_dict["maxResolution"] = max_resolution

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_points = d.pop("maxPoints", UNSET)

        max_resolution = d.pop("maxResolution", UNSET)

        shape = cls(
            max_points=max_points,
            max_resolution=max_resolution,
        )

        shape.additional_properties = d
        return shape

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
