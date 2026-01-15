from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MatchTraceVia")


@_attrs_define
class MatchTraceVia:
    """Via waypoint in the middle of route

    Attributes:
        index (int): Index of the corresponding trace point
        stop_duration (int | Unset): Duration in seconds. Example: 198.
    """

    index: int
    stop_duration: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        index = self.index

        stop_duration = self.stop_duration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "index": index,
        })
        if stop_duration is not UNSET:
            field_dict["stopDuration"] = stop_duration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        index = d.pop("index")

        stop_duration = d.pop("stopDuration", UNSET)

        match_trace_via = cls(
            index=index,
            stop_duration=stop_duration,
        )

        match_trace_via.additional_properties = d
        return match_trace_via

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
