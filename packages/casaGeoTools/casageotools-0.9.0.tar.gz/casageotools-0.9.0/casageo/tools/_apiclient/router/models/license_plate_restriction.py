from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LicensePlateRestriction")


@_attrs_define
class LicensePlateRestriction:
    """Contains details of the violated license plate restriction.

    Attributes:
        type_ (str | Unset): Extensible enum: `lastCharacter` `...`
            Specifies the components of the vehicle license plate
            considered for the restriction.
        forbidden_characters (list[str] | Unset): A list of restricted characters in the vehicle license plate.

            The `type` property indicates which character of the vehicle license plate is considered for matching.
            The condition is met if that character matches any of the characters in the `forbiddenCharacters` array.

            For example, if `type` is set to `lastCharacter` and `forbiddenCharacters` is set to `["7", "8"]` then the
            condition is met if the last character
            of the vehicle license plate is either 7 or 8.
             Example: ['1', '3', '5', '7', '9'].
    """

    type_: str | Unset = UNSET
    forbidden_characters: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        forbidden_characters: list[str] | Unset = UNSET
        if not isinstance(self.forbidden_characters, Unset):
            forbidden_characters = self.forbidden_characters

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if forbidden_characters is not UNSET:
            field_dict["forbiddenCharacters"] = forbidden_characters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type", UNSET)

        forbidden_characters = cast(list[str], d.pop("forbiddenCharacters", UNSET))

        license_plate_restriction = cls(
            type_=type_,
            forbidden_characters=forbidden_characters,
        )

        license_plate_restriction.additional_properties = d
        return license_plate_restriction

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
