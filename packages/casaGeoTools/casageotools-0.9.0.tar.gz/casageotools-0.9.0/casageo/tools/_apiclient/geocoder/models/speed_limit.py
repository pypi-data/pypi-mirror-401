from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.speed_limit_direction import SpeedLimitDirection
from ..models.speed_limit_source import SpeedLimitSource
from ..models.speed_limit_speed_unit import SpeedLimitSpeedUnit
from ..types import UNSET, Unset

T = TypeVar("T", bound="SpeedLimit")


@_attrs_define
class SpeedLimit:
    """
    Attributes:
        max_speed (int): Used in combination with speed limit unit to indicate allowable speed limit at a location, for
            unlimited speed, the value is "999"
        speed_unit (SpeedLimitSpeedUnit): Country defined speed unit
        direction (SpeedLimitDirection | Unset): Rendered in compass value, which is N, S, E, W, NE, SE, NW, SW
        source (SpeedLimitSource | Unset): A generalised identification of the source of `Speed Limit` information.

            Description of supported values:

            - `derived`: Based on administrative regulations, for example: highway exit/entry ramps that do not have posted
            speed limits.
            - `posted`: Based on a posted speed limit sign, speed limit information painted on the road, or data obtained
            from official sources.
    """

    max_speed: int
    speed_unit: SpeedLimitSpeedUnit
    direction: SpeedLimitDirection | Unset = UNSET
    source: SpeedLimitSource | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_speed = self.max_speed

        speed_unit = self.speed_unit.value

        direction: str | Unset = UNSET
        if not isinstance(self.direction, Unset):
            direction = self.direction.value

        source: str | Unset = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "maxSpeed": max_speed,
            "speedUnit": speed_unit,
        })
        if direction is not UNSET:
            field_dict["direction"] = direction
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_speed = d.pop("maxSpeed")

        speed_unit = SpeedLimitSpeedUnit(d.pop("speedUnit"))

        _direction = d.pop("direction", UNSET)
        direction: SpeedLimitDirection | Unset
        if isinstance(_direction, Unset):
            direction = UNSET
        else:
            direction = SpeedLimitDirection(_direction)

        _source = d.pop("source", UNSET)
        source: SpeedLimitSource | Unset
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = SpeedLimitSource(_source)

        speed_limit = cls(
            max_speed=max_speed,
            speed_unit=speed_unit,
            direction=direction,
            source=source,
        )

        speed_limit.additional_properties = d
        return speed_limit

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
