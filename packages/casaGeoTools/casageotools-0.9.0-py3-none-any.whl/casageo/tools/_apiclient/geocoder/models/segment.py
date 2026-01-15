from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Segment")


@_attrs_define
class Segment:
    """
    Attributes:
        ref (str | Unset): The segment reference follows the format `{segmentId}(#{offset})?`,
            representing its relative position from the result location to a segment.
        side (str | Unset): The side of the link the attribute is applicable to

            - for `resultType=houseNumber` and `resultType=place`: side of the entity to the link
            - for `resultType=street`:
              - on endpoints *Geocode* and *Lookup*: side of the entity to the link, it is always "both"
              - on endpoints *Reverse Geocode* and *Multi-Reverse Geocode*: relative side from input to the link
    """

    ref: str | Unset = UNSET
    side: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ref = self.ref

        side = self.side

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ref is not UNSET:
            field_dict["ref"] = ref
        if side is not UNSET:
            field_dict["side"] = side

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ref = d.pop("ref", UNSET)

        side = d.pop("side", UNSET)

        segment = cls(
            ref=ref,
            side=side,
        )

        segment.additional_properties = d
        return segment

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
