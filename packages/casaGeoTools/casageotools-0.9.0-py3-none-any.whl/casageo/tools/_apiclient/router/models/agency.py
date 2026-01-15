from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Agency")


@_attrs_define
class Agency:
    """Contains information about a particular agency.

    Attributes:
        id (str): Unique code of the agency. Specifies if the same agency is used on different sections of the same
            route.

            **NOTE**: The given ID is only valid within the context of the response it is in.
        name (str): Human readable name of the owner of the transport service.
        website (str | Unset): An URL address that links to a particular resource. Example:
            https://url.address.com/resource.
    """

    id: str
    name: str
    website: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        website = self.website

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
        })
        if website is not UNSET:
            field_dict["website"] = website

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        website = d.pop("website", UNSET)

        agency = cls(
            id=id,
            name=name,
            website=website,
        )

        agency.additional_properties = d
        return agency

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
