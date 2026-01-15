from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FarePassValidityPeriod")


@_attrs_define
class FarePassValidityPeriod:
    """Specifies a temporal validity period for a pass

    Attributes:
        period (str): Extensible enum: `annual` `extendedAnnual` `minutes` `days` `months` `...`
            Specifies one of the following validity periods:
              - `annual`: pass is valid from Jan 1 to Dec 31
              - `extendedAnnual`: pass is valid from Jan 1 to Jan 31 of the following year
              - `minutes`: pass is valid for a specified number of minutes See `unit`.
              - `days`: pass is valid for a specified number of days. See `unit`.
              - `months`: pass is valid for a specified number of months. See `unit`.
        count (int | Unset): Required if period is `minutes`, days` or `months`, it specifies how many of these units
            are covered by the pass.
    """

    period: str
    count: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period = self.period

        count = self.count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "period": period,
        })
        if count is not UNSET:
            field_dict["count"] = count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period = d.pop("period")

        count = d.pop("count", UNSET)

        fare_pass_validity_period = cls(
            period=period,
            count=count,
        )

        fare_pass_validity_period.additional_properties = d
        return fare_pass_validity_period

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
