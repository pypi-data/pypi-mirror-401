from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CmVersionSection")


@_attrs_define
class CmVersionSection:
    """
    Attributes:
        region (str): Region ID
        dvn (str): Map version details (DVN) containing the base line for the map schema and an identifier for the
            weekly or quarterly update.

            - Format: YYQ<weekly/quaterly update>
              - Example: 23150 (map schema: Q1/2023, weekly update 50)
    """

    region: str
    dvn: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        region = self.region

        dvn = self.dvn

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "region": region,
            "dvn": dvn,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        region = d.pop("region")

        dvn = d.pop("dvn")

        cm_version_section = cls(
            region=region,
            dvn=dvn,
        )

        cm_version_section.additional_properties = d
        return cm_version_section

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
