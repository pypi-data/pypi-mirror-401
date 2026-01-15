from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="StreetInfo")


@_attrs_define
class StreetInfo:
    """
    Attributes:
        base_name (str | Unset): Base name part of the street name.
        street_type (str | Unset): Street type part of the street name.
        street_type_precedes (bool | Unset): Defines if the street type is before or after the base name.
        street_type_attached (bool | Unset): Defines if the street type is attached or unattached to the base name.
        prefix (str | Unset): A prefix is a directional identifier that precedes, but is not included in, the base name
            of a road.
        suffix (str | Unset): A suffix is a directional identifier that follows, but is not included in, the base name
            of a road.
        direction (str | Unset): Indicates the official directional identifiers assigned to highways, typically either
            "North/South" or "East/West"
        language (str | Unset): BCP 47 compliant language code
    """

    base_name: str | Unset = UNSET
    street_type: str | Unset = UNSET
    street_type_precedes: bool | Unset = UNSET
    street_type_attached: bool | Unset = UNSET
    prefix: str | Unset = UNSET
    suffix: str | Unset = UNSET
    direction: str | Unset = UNSET
    language: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        base_name = self.base_name

        street_type = self.street_type

        street_type_precedes = self.street_type_precedes

        street_type_attached = self.street_type_attached

        prefix = self.prefix

        suffix = self.suffix

        direction = self.direction

        language = self.language

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if base_name is not UNSET:
            field_dict["baseName"] = base_name
        if street_type is not UNSET:
            field_dict["streetType"] = street_type
        if street_type_precedes is not UNSET:
            field_dict["streetTypePrecedes"] = street_type_precedes
        if street_type_attached is not UNSET:
            field_dict["streetTypeAttached"] = street_type_attached
        if prefix is not UNSET:
            field_dict["prefix"] = prefix
        if suffix is not UNSET:
            field_dict["suffix"] = suffix
        if direction is not UNSET:
            field_dict["direction"] = direction
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        base_name = d.pop("baseName", UNSET)

        street_type = d.pop("streetType", UNSET)

        street_type_precedes = d.pop("streetTypePrecedes", UNSET)

        street_type_attached = d.pop("streetTypeAttached", UNSET)

        prefix = d.pop("prefix", UNSET)

        suffix = d.pop("suffix", UNSET)

        direction = d.pop("direction", UNSET)

        language = d.pop("language", UNSET)

        street_info = cls(
            base_name=base_name,
            street_type=street_type,
            street_type_precedes=street_type_precedes,
            street_type_attached=street_type_attached,
            prefix=prefix,
            suffix=suffix,
            direction=direction,
            language=language,
        )

        street_info.additional_properties = d
        return street_info

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
