from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Scooter")


@_attrs_define
class Scooter:
    """Scooter-specific parameters

    Attributes:
        allow_highway (bool | Unset): Specifies whether the scooter is allowed on the highway or not. This parameter is
            optional. If not provided, the scooter is not allowed to use the highway by default. There is a similar
            parameter avoid[features]=controlledAccessHighway to disallow highway usage. avoid[features] takes precedence,
            so if this parameter is also used, scooters are not allowed to use highways even if `allowHighway` is set to
            `true`. Default: False.
    """

    allow_highway: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allow_highway = self.allow_highway

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allow_highway is not UNSET:
            field_dict["allowHighway"] = allow_highway

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        allow_highway = d.pop("allowHighway", UNSET)

        scooter = cls(
            allow_highway=allow_highway,
        )

        scooter.additional_properties = d
        return scooter

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
