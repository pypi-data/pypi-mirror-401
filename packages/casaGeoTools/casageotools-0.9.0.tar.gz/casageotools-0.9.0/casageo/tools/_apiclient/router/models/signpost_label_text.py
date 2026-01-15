from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.localized_string import LocalizedString


T = TypeVar("T", bound="SignpostLabelText")


@_attrs_define
class SignpostLabelText:
    """Text on a signpost label.

    Attributes:
        name (LocalizedString | Unset): String with optional language code. Example: {'value': 'Invalidenstraße',
            'language': 'de'}.
    """

    name: LocalizedString | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: dict[str, Any] | Unset = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.localized_string import LocalizedString

        d = dict(src_dict)
        _name = d.pop("name", UNSET)
        name: LocalizedString | Unset
        if isinstance(_name, Unset):
            name = UNSET
        else:
            name = LocalizedString.from_dict(_name)

        signpost_label_text = cls(
            name=name,
        )

        signpost_label_text.additional_properties = d
        return signpost_label_text

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
