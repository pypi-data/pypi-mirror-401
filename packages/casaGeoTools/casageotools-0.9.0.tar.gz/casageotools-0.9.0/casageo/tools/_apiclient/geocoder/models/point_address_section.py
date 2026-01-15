from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PointAddressSection")


@_attrs_define
class PointAddressSection:
    """
    Attributes:
        hmc_id (str): The point address ID in HERE Map Content
        partition_id (str | Unset): **ALPHA**

            Unique identifier that references a specific subset of geo-location related layers
            (e.g., address, location, street, or place) in the HERE Map Content
    """

    hmc_id: str
    partition_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hmc_id = self.hmc_id

        partition_id = self.partition_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "hmcId": hmc_id,
        })
        if partition_id is not UNSET:
            field_dict["partitionId"] = partition_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        hmc_id = d.pop("hmcId")

        partition_id = d.pop("partitionId", UNSET)

        point_address_section = cls(
            hmc_id=hmc_id,
            partition_id=partition_id,
        )

        point_address_section.additional_properties = d
        return point_address_section

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
