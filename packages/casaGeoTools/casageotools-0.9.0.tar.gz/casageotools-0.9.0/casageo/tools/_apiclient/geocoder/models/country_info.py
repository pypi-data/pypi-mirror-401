from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CountryInfo")


@_attrs_define
class CountryInfo:
    """
    Attributes:
        alpha2 (str | Unset): [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) country code
        alpha3 (str | Unset): [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) country code
    """

    alpha2: str | Unset = UNSET
    alpha3: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        alpha2 = self.alpha2

        alpha3 = self.alpha3

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if alpha2 is not UNSET:
            field_dict["alpha2"] = alpha2
        if alpha3 is not UNSET:
            field_dict["alpha3"] = alpha3

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        alpha2 = d.pop("alpha2", UNSET)

        alpha3 = d.pop("alpha3", UNSET)

        country_info = cls(
            alpha2=alpha2,
            alpha3=alpha3,
        )

        country_info.additional_properties = d
        return country_info

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
