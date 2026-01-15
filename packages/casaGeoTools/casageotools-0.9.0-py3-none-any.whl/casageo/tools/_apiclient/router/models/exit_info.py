from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.localized_string import LocalizedString


T = TypeVar("T", bound="ExitInfo")


@_attrs_define
class ExitInfo:
    """Exit information attached to an offset action

    Example:
        {'exit': {'number': [{'value': '15', 'language': 'de'}]}}

    Attributes:
        number (list[LocalizedString] | Unset): Number of the exit (e.g. '18')
    """

    number: list[LocalizedString] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        number: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.number, Unset):
            number = []
            for number_item_data in self.number:
                number_item = number_item_data.to_dict()
                number.append(number_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if number is not UNSET:
            field_dict["number"] = number

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.localized_string import LocalizedString

        d = dict(src_dict)
        _number = d.pop("number", UNSET)
        number: list[LocalizedString] | Unset = UNSET
        if _number is not UNSET:
            number = []
            for number_item_data in _number:
                number_item = LocalizedString.from_dict(number_item_data)

                number.append(number_item)

        exit_info = cls(
            number=number,
        )

        exit_info.additional_properties = d
        return exit_info

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
