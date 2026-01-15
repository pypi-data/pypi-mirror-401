from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.traffic_mode import TrafficMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="Traffic")


@_attrs_define
class Traffic:
    """Traffic specific parameters.

    Attributes:
        override_flow_duration (int | Unset): Duration in seconds for which flow traffic event would be considered
            valid. While flow
            traffic event is valid it will be used over the historical traffic data.

            **Note**: Flow traffic represents congestion not caused by any long-term incidents.
            State of the flow traffic often changes fast. The farther away from the current time we
            move, the less precise current flow traffic data will be and the more precise historical
            traffic data becomes. That's why it's advised not to use this parameter unless you know
            what you want to achieve and use the default behavior which is almost always better.
        mode (TrafficMode | Unset): Defines what traffic data should be used for route shape and travel duration
            calculation.

            * `default`: Traffic data is considered.
            *    - If `departureTime=any` then only long-term closures will be considered.
            *    - If `departureTime` is not equal to `any` then all traffic data will be taken into account.
            * `disabled`: All traffic data, including long term closures, is ignored.
             Default: TrafficMode.DEFAULT.
    """

    override_flow_duration: int | Unset = UNSET
    mode: TrafficMode | Unset = TrafficMode.DEFAULT
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        override_flow_duration = self.override_flow_duration

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if override_flow_duration is not UNSET:
            field_dict["overrideFlowDuration"] = override_flow_duration
        if mode is not UNSET:
            field_dict["mode"] = mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        override_flow_duration = d.pop("overrideFlowDuration", UNSET)

        _mode = d.pop("mode", UNSET)
        mode: TrafficMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = TrafficMode(_mode)

        traffic = cls(
            override_flow_duration=override_flow_duration,
            mode=mode,
        )

        traffic.additional_properties = d
        return traffic

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
