from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Driver")


@_attrs_define
class Driver:
    """Driver parameters to be used for calculating routes with automatically added
    rest stops.

        Attributes:
            schedule (str | Unset): A comma separated list of duration pairs in seconds. Each pair is two positive non-zero
                integers.
                The first specifies the maximum allowed drive duration before stopping to rest, and the second the resting
                duration before continuing driving.

                Format `driveDuration,restDuration[,driveDuration,restDuration]...`

                * driveDuration - duration in seconds, describes maximum driving duration allowed in a route's section
                  till the next stop or route end. Minimum value is 240.
                * restDuration - duration in seconds, describes minimum resting duration required before continuing driving

                The routing engine adds necessary stops for rest to fulfill driver work hours requirements.
                If the route duration exceeds the defined drive-rest sequence the remaining route is added as the last drive
                section
                (or several sections if there are `via` waypoints on the remaining route) with critical notice
                `travelTimeExceedsDriverWorkHours`.

                **Limitations**:
                * `driver[schedule]` is only supported for `truck`, `bus` and `privateBus` transport modes.
                * `driver[schedule]` is not supported in combination with any of these parameters: `arrivalTime`, `ev[*]`.
                * `driver[schedule]` doesn't support route alternatives. So `alternatives` parameter value is ignored in
                combination with `driver[schedule]`.
                * Ferry travel, boarding, and deboarding durations are neither considered part of drive duration nor rest
                duration unless ferry
                  travel duration is below 15 minutes. In this case, ferry travel duration is considered as drive duration.
                * Via waypoint stop-durations are neither considered part of drive duration nor rest duration.
                * Routing requires a minimum driving duration (`driveDuration`) of 240 seconds before a rest stop.
    """

    schedule: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schedule = self.schedule

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if schedule is not UNSET:
            field_dict["schedule"] = schedule

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schedule = d.pop("schedule", UNSET)

        driver = cls(
            schedule=schedule,
        )

        driver.additional_properties = d
        return driver

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
