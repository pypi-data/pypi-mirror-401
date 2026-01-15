from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LinkInfoSection")


@_attrs_define
class LinkInfoSection:
    """
    Attributes:
        cm_id (str): link ID in HERE core map
        side (str): The side of the link the attribute is applicable to

            - for `resultType=houseNumber` and `resultType=place`: side of the entity to the link
            - for `resultType=street`:
              - on endpoints *Geocode* and *Lookup*: side of the entity to the link, it is always "both"
              - on endpoints *Reverse Geocode* and *Multi-Reverse Geocode*: relative side from input to the link
    """

    cm_id: str
    side: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cm_id = self.cm_id

        side = self.side

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "cmId": cm_id,
            "side": side,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cm_id = d.pop("cmId")

        side = d.pop("side")

        link_info_section = cls(
            cm_id=cm_id,
            side=side,
        )

        link_info_section.additional_properties = d
        return link_info_section

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
