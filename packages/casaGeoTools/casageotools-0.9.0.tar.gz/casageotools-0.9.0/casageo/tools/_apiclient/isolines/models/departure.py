from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_place import BasePlace


T = TypeVar("T", bound="Departure")


@_attrs_define
class Departure:
    """Describe a departure or arrival location and time.

    Attributes:
        place (BasePlace):  Example: {'type': 'place', 'location': {'lat': 50.339167, 'lng': 18.93}}.
        time (datetime.datetime | Unset): **RFC 3339**, section 5.6 as defined by either `date-time` or `date-only` 'T'
            `partial-time` (ie no time-offset).
    """

    place: BasePlace
    time: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        place = self.place.to_dict()

        time: str | Unset = UNSET
        if not isinstance(self.time, Unset):
            time = self.time.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "place": place,
        })
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_place import BasePlace

        d = dict(src_dict)
        place = BasePlace.from_dict(d.pop("place"))

        _time = d.pop("time", UNSET)
        time: datetime.datetime | Unset
        if isinstance(_time, Unset):
            time = UNSET
        else:
            time = isoparse(_time)

        departure = cls(
            place=place,
            time=time,
        )

        departure.additional_properties = d
        return departure

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
