from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.address_usage_usage_type import AddressUsageUsageType

T = TypeVar("T", bound="AddressUsage")


@_attrs_define
class AddressUsage:
    """
    Attributes:
        usage_type (AddressUsageUsageType): A flag specifying whether the address is residential. (only rendered if
            `show=addressUsage` is provided.)
    """

    usage_type: AddressUsageUsageType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        usage_type = self.usage_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "usageType": usage_type,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        usage_type = AddressUsageUsageType(d.pop("usageType"))

        address_usage = cls(
            usage_type=usage_type,
        )

        address_usage.additional_properties = d
        return address_usage

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
