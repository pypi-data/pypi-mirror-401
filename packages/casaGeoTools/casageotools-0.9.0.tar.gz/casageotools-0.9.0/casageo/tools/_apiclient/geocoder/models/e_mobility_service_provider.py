from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EMobilityServiceProvider")


@_attrs_define
class EMobilityServiceProvider:
    """
    Attributes:
        name (str): The name of the e-Mobility Service Provider. The eMSP name may change but the respective partner ID
            will remain stable.
        partner_id (str): The unique and stable ID for the e-Mobility Service Provider provided by HERE platform.
            The partner ID can be used to display EV stations supported by eMSP for which drivers have a subscription.
            The list of eMSP partner IDs can be retrieved using the EV Charge Points API
            [`roaming`](https://www.here.com/docs/bundle/ev-charge-points-api-developer-guide/page/topics/resource-
            roamings.html) resource.
    """

    name: str
    partner_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        partner_id = self.partner_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "partnerId": partner_id,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        partner_id = d.pop("partnerId")

        e_mobility_service_provider = cls(
            name=name,
            partner_id=partner_id,
        )

        e_mobility_service_provider.additional_properties = d
        return e_mobility_service_provider

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
