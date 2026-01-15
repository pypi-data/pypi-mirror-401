from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.time_restricted_weekdays import TimeRestrictedWeekdays
from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeRestrictedPrice")


@_attrs_define
class TimeRestrictedPrice:
    """
    Attributes:
        type_ (str): Type of price represented by this object. The API customer is responsible for correctly visualizing
            the pricing model. As it is possible to extend the supported price types in the future,
            the price information should be hidden when an unknown type is encountered.

            Available price types are:

              * `restricted` - A single price value valid for a specific time or duration
        currency (str): Local currency of the price compliant to ISO 4217
        value (float): The price value
        estimated (bool | Unset): Attribute value is `true` if the fare price is estimated, `false` if it is an exact
            value. Default: False.
        unit (int | Unset): Duration in seconds. Example: 198.
        days (list[TimeRestrictedWeekdays] | Unset): This price applies only for the selected days Example: ['sa',
            'su'].
        min_duration (int | Unset): Duration in seconds. Example: 198.
        max_duration (int | Unset): Duration in seconds. Example: 198.
        from_time (str | Unset): **RFC 3339**, section 5.6 as defined by `partial-time`. Example: 08:30:00.
        to_time (str | Unset): **RFC 3339**, section 5.6 as defined by `partial-time`. Example: 08:30:00.
    """

    type_: str
    currency: str
    value: float
    estimated: bool | Unset = False
    unit: int | Unset = UNSET
    days: list[TimeRestrictedWeekdays] | Unset = UNSET
    min_duration: int | Unset = UNSET
    max_duration: int | Unset = UNSET
    from_time: str | Unset = UNSET
    to_time: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        currency = self.currency

        value = self.value

        estimated = self.estimated

        unit = self.unit

        days: list[str] | Unset = UNSET
        if not isinstance(self.days, Unset):
            days = []
            for days_item_data in self.days:
                days_item = days_item_data.value
                days.append(days_item)

        min_duration = self.min_duration

        max_duration = self.max_duration

        from_time = self.from_time

        to_time = self.to_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "currency": currency,
            "value": value,
        })
        if estimated is not UNSET:
            field_dict["estimated"] = estimated
        if unit is not UNSET:
            field_dict["unit"] = unit
        if days is not UNSET:
            field_dict["days"] = days
        if min_duration is not UNSET:
            field_dict["minDuration"] = min_duration
        if max_duration is not UNSET:
            field_dict["maxDuration"] = max_duration
        if from_time is not UNSET:
            field_dict["fromTime"] = from_time
        if to_time is not UNSET:
            field_dict["toTime"] = to_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        currency = d.pop("currency")

        value = d.pop("value")

        estimated = d.pop("estimated", UNSET)

        unit = d.pop("unit", UNSET)

        _days = d.pop("days", UNSET)
        days: list[TimeRestrictedWeekdays] | Unset = UNSET
        if _days is not UNSET:
            days = []
            for days_item_data in _days:
                days_item = TimeRestrictedWeekdays(days_item_data)

                days.append(days_item)

        min_duration = d.pop("minDuration", UNSET)

        max_duration = d.pop("maxDuration", UNSET)

        from_time = d.pop("fromTime", UNSET)

        to_time = d.pop("toTime", UNSET)

        time_restricted_price = cls(
            type_=type_,
            currency=currency,
            value=value,
            estimated=estimated,
            unit=unit,
            days=days,
            min_duration=min_duration,
            max_duration=max_duration,
            from_time=from_time,
            to_time=to_time,
        )

        time_restricted_price.additional_properties = d
        return time_restricted_price

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
