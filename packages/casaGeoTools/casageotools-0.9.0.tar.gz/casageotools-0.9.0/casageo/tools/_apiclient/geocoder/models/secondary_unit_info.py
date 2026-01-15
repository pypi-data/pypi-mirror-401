from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SecondaryUnitInfo")


@_attrs_define
class SecondaryUnitInfo:
    """
    Attributes:
        normalized_unit_type (str): The secondary unit designator is provided in a normalized, country-specific format.
            If the secondary unit designator is omitted or unrecognized, it is returned as "unknown".
        unit_value (str): The unit value in normalized form. It may be empty when secondary unit designator has no unit
            value, for example "Basement".
    """

    normalized_unit_type: str
    unit_value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        normalized_unit_type = self.normalized_unit_type

        unit_value = self.unit_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "normalizedUnitType": normalized_unit_type,
            "unitValue": unit_value,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        normalized_unit_type = d.pop("normalizedUnitType")

        unit_value = d.pop("unitValue")

        secondary_unit_info = cls(
            normalized_unit_type=normalized_unit_type,
            unit_value=unit_value,
        )

        secondary_unit_info.additional_properties = d
        return secondary_unit_info

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
