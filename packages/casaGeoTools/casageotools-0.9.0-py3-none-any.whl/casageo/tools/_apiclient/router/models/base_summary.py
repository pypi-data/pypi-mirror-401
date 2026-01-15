from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseSummary")


@_attrs_define
class BaseSummary:
    """Total value of key attributes for a route section.

    Attributes:
        duration (int): Duration in seconds. Example: 198.
        length (int): Distance in meters. Example: 189.
        base_duration (int | Unset): Duration in seconds. Example: 198.
    """

    duration: int
    length: int
    base_duration: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duration = self.duration

        length = self.length

        base_duration = self.base_duration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "duration": duration,
            "length": length,
        })
        if base_duration is not UNSET:
            field_dict["baseDuration"] = base_duration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        duration = d.pop("duration")

        length = d.pop("length")

        base_duration = d.pop("baseDuration", UNSET)

        base_summary = cls(
            duration=duration,
            length=length,
            base_duration=base_duration,
        )

        base_summary.additional_properties = d
        return base_summary

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
