from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TimeZoneInfo")


@_attrs_define
class TimeZoneInfo:
    """
    Attributes:
        name (str): The name of the time zone as defined in the [tz
            database](https://en.wikipedia.org/wiki/Tz_database). For example: "Europe/Berlin"
        utc_offset (str): The UTC offset for this time zone at request time. For example "+02:00"
    """

    name: str
    utc_offset: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        utc_offset = self.utc_offset

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "utcOffset": utc_offset,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        utc_offset = d.pop("utcOffset")

        time_zone_info = cls(
            name=name,
            utc_offset=utc_offset,
        )

        time_zone_info.additional_properties = d
        return time_zone_info

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
