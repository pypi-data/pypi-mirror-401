from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="StructuredOpeningHours")


@_attrs_define
class StructuredOpeningHours:
    """
    Attributes:
        start (str): String with a modified [iCalendar DATE-
            TIME](https://datatracker.ietf.org/doc/html/rfc5545#section-3.3.5) value.
            The date part is omitted, values starts with the time section maker "T". Example: T132000
        duration (str): String with an [iCalendar DURATION](https://datatracker.ietf.org/doc/html/rfc5545#section-3.3.6)
            value.
            A closed day has the value PT00:00M
        recurrence (str): String with a [RECUR](https://datatracker.ietf.org/doc/html/rfc5545#section-3.3.10) rule. Note
            that,
             in contrast to the RFC, the assignment operator is a colon `:` and not an equal sign `=`.
    """

    start: str
    duration: str
    recurrence: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start = self.start

        duration = self.duration

        recurrence = self.recurrence

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "start": start,
            "duration": duration,
            "recurrence": recurrence,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start = d.pop("start")

        duration = d.pop("duration")

        recurrence = d.pop("recurrence")

        structured_opening_hours = cls(
            start=start,
            duration=duration,
            recurrence=recurrence,
        )

        structured_opening_hours.additional_properties = d
        return structured_opening_hours

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
