from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.match_trace_point import MatchTracePoint
    from ..models.match_trace_via import MatchTraceVia


T = TypeVar("T", bound="MatchTrace")


@_attrs_define
class MatchTrace:
    """Trace file with points and path match parameters

    Example:
        {'trace': [{'lat': 52.0, 'lng': 13.1}, {'lat': 52.1, 'lng': 13.2}, {'lat': 52.2, 'lng': 13.3}], 'via':
            [{'index': 1}]}

    Attributes:
        trace (list[MatchTracePoint]):
        via (list[MatchTraceVia] | Unset):
    """

    trace: list[MatchTracePoint]
    via: list[MatchTraceVia] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        trace = []
        for trace_item_data in self.trace:
            trace_item = trace_item_data.to_dict()
            trace.append(trace_item)

        via: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.via, Unset):
            via = []
            for via_item_data in self.via:
                via_item = via_item_data.to_dict()
                via.append(via_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "trace": trace,
        })
        if via is not UNSET:
            field_dict["via"] = via

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.match_trace_point import MatchTracePoint
        from ..models.match_trace_via import MatchTraceVia

        d = dict(src_dict)
        trace = []
        _trace = d.pop("trace")
        for trace_item_data in _trace:
            trace_item = MatchTracePoint.from_dict(trace_item_data)

            trace.append(trace_item)

        _via = d.pop("via", UNSET)
        via: list[MatchTraceVia] | Unset = UNSET
        if _via is not UNSET:
            via = []
            for via_item_data in _via:
                via_item = MatchTraceVia.from_dict(via_item_data)

                via.append(via_item)

        match_trace = cls(
            trace=trace,
            via=via,
        )

        match_trace.additional_properties = d
        return match_trace

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
