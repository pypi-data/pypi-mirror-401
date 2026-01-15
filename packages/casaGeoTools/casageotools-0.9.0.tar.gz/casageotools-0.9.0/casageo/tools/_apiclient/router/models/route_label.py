from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.route_label_label_type import RouteLabelLabelType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.localized_string import LocalizedString


T = TypeVar("T", bound="RouteLabel")


@_attrs_define
class RouteLabel:
    """Road name or route number distinguishing a route from other alternatives.

    Attributes:
        label_type (RouteLabelLabelType | Unset):
        name (LocalizedString | Unset): String with optional language code. Example: {'value': 'Invalidenstraße',
            'language': 'de'}.
    """

    label_type: RouteLabelLabelType | Unset = UNSET
    name: LocalizedString | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label_type: str | Unset = UNSET
        if not isinstance(self.label_type, Unset):
            label_type = self.label_type.value

        name: dict[str, Any] | Unset = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if label_type is not UNSET:
            field_dict["label_type"] = label_type
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.localized_string import LocalizedString

        d = dict(src_dict)
        _label_type = d.pop("label_type", UNSET)
        label_type: RouteLabelLabelType | Unset
        if isinstance(_label_type, Unset):
            label_type = UNSET
        else:
            label_type = RouteLabelLabelType(_label_type)

        _name = d.pop("name", UNSET)
        name: LocalizedString | Unset
        if isinstance(_name, Unset):
            name = UNSET
        else:
            name = LocalizedString.from_dict(_name)

        route_label = cls(
            label_type=label_type,
            name=name,
        )

        route_label.additional_properties = d
        return route_label

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
