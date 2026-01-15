from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DynamicSpeedInfo")


@_attrs_define
class DynamicSpeedInfo:
    """Describes dynamic speed information, such as traffic speed, estimated speed without traffic, and turn time.

    Attributes:
        traffic_speed (float): Speed in meters per second
        base_speed (float): Speed in meters per second
        turn_time (int): Duration in seconds. Example: 198.
    """

    traffic_speed: float
    base_speed: float
    turn_time: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        traffic_speed = self.traffic_speed

        base_speed = self.base_speed

        turn_time = self.turn_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "trafficSpeed": traffic_speed,
            "baseSpeed": base_speed,
            "turnTime": turn_time,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        traffic_speed = d.pop("trafficSpeed")

        base_speed = d.pop("baseSpeed")

        turn_time = d.pop("turnTime")

        dynamic_speed_info = cls(
            traffic_speed=traffic_speed,
            base_speed=base_speed,
            turn_time=turn_time,
        )

        dynamic_speed_info.additional_properties = d
        return dynamic_speed_info

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
