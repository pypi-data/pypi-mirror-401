from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.violated_charging_station_opening_hours_type import (
    ViolatedChargingStationOpeningHoursType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ViolatedChargingStationOpeningHours")


@_attrs_define
class ViolatedChargingStationOpeningHours:
    """A charging stop was planned at the destination of this section, but the `postActions` would not be completed within
    the opening hours.

        Attributes:
            type_ (ViolatedChargingStationOpeningHoursType): Detail type. Each type of detail might contain extra
                attributes.

                **NOTE:** The list of possible detail types may be extended in the future.
                The client application is expected to handle such a case gracefully.
            title (str | Unset): Detail title
            cause (str | Unset): Cause of the notice
            opening_hours (str | Unset): Specifies date and time period during which the restriction applies. Value is a
                string in the Time
                Domain format. Time Domain is part of the GDF (Geographic Data Files) specification, which is an ISO standard.
                Current standard is GDF 5.1 which is [ISO 20524-1:2020](https://www.iso.org/standard/68244.html).

                For a detailed description of the Time Domain specification and usage in routing services, please refer to
                the documentation available in the [Time Domain](https://www.here.com/docs/bundle/routing-api-developer-
                guide-v8/page/concepts/time-domain.html) page of the Developer Guide.
                 Example: -(d1){w1}(d3){d1}.
    """

    type_: ViolatedChargingStationOpeningHoursType
    title: str | Unset = UNSET
    cause: str | Unset = UNSET
    opening_hours: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        title = self.title

        cause = self.cause

        opening_hours = self.opening_hours

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
        })
        if title is not UNSET:
            field_dict["title"] = title
        if cause is not UNSET:
            field_dict["cause"] = cause
        if opening_hours is not UNSET:
            field_dict["opening_hours"] = opening_hours

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = ViolatedChargingStationOpeningHoursType(d.pop("type"))

        title = d.pop("title", UNSET)

        cause = d.pop("cause", UNSET)

        opening_hours = d.pop("opening_hours", UNSET)

        violated_charging_station_opening_hours = cls(
            type_=type_,
            title=title,
            cause=cause,
            opening_hours=opening_hours,
        )

        violated_charging_station_opening_hours.additional_properties = d
        return violated_charging_station_opening_hours

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
