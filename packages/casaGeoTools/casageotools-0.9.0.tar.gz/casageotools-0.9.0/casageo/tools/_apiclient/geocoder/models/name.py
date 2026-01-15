from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.name_type import NameType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Name")


@_attrs_define
class Name:
    """
    Attributes:
        value (str): The text value of this name.
        type_ (NameType): The type of this name.

            Description of supported values:

            - `abbreviation`: Abbreviation is a shortened form of the official name.  For example, "CA" for "California".
            Abbreviation may also be an area code.
            - `areaCode`: Area code is a code representation of an admin. For example for countries this can be an ISO-3 or
            ISO-2 Code: "USA", "US" for "United States".
            - `baseName`: Base name represents the official name in one of the country official languages. For example,
            "Frankfurt am Main".
            - `exonym`: Exonym is a translation of the official name to a language that is not one of the country official
            languages. For example "Francfort-sur-le-Main" for "Frankfurt am Main".
            - `shortened`: A shortened variant of a long name where optional parts are omitted. For example, "Bad Soden" for
            "Bad Soden am Taunus".
            - `synonym`: A synonym is an additional commonly used name that is different than the official name, in the same
            language as the official name. For example, "Frankfurt" for "Frankfurt am Main".
        language (str | Unset): The [BCP 47](https://en.wikipedia.org/wiki/IETF_language_tag) language code.
        primary (bool | Unset): Flag indicating whether it is a primary name. This is the name which is exposed in the
            result by default. This field is visible only when the value is `true`.
        transliterated (bool | Unset): Flag indicating whether the name is transliterated. Additional transliterated
            form of the name is included for all non-Latin-1 names. This field is visible only when the value is `true`.
    """

    value: str
    type_: NameType
    language: str | Unset = UNSET
    primary: bool | Unset = UNSET
    transliterated: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        type_ = self.type_.value

        language = self.language

        primary = self.primary

        transliterated = self.transliterated

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "value": value,
            "type": type_,
        })
        if language is not UNSET:
            field_dict["language"] = language
        if primary is not UNSET:
            field_dict["primary"] = primary
        if transliterated is not UNSET:
            field_dict["transliterated"] = transliterated

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        type_ = NameType(d.pop("type"))

        language = d.pop("language", UNSET)

        primary = d.pop("primary", UNSET)

        transliterated = d.pop("transliterated", UNSET)

        name = cls(
            value=value,
            type_=type_,
            language=language,
            primary=primary,
            transliterated=transliterated,
        )

        name.additional_properties = d
        return name

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
