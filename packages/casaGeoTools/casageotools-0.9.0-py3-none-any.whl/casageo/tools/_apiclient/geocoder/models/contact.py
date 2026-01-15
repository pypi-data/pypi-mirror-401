from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.category_ref import CategoryRef


T = TypeVar("T", bound="Contact")


@_attrs_define
class Contact:
    """
    Attributes:
        value (str): Contact information, as specified by the contact type.
        label (str | Unset): Optional label for the contact string, such as "Customer Service" or "Pharmacy Fax".
        categories (list[CategoryRef] | Unset): The list of place categories this contact refers to.
    """

    value: str
    label: str | Unset = UNSET
    categories: list[CategoryRef] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        label = self.label

        categories: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.to_dict()
                categories.append(categories_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "value": value,
        })
        if label is not UNSET:
            field_dict["label"] = label
        if categories is not UNSET:
            field_dict["categories"] = categories

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.category_ref import CategoryRef

        d = dict(src_dict)
        value = d.pop("value")

        label = d.pop("label", UNSET)

        _categories = d.pop("categories", UNSET)
        categories: list[CategoryRef] | Unset = UNSET
        if _categories is not UNSET:
            categories = []
            for categories_item_data in _categories:
                categories_item = CategoryRef.from_dict(categories_item_data)

                categories.append(categories_item)

        contact = cls(
            value=value,
            label=label,
            categories=categories,
        )

        contact.additional_properties = d
        return contact

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
