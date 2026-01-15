from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.category_ref import CategoryRef
    from ..models.structured_opening_hours import StructuredOpeningHours


T = TypeVar("T", bound="OpeningHours")


@_attrs_define
class OpeningHours:
    """
    Attributes:
        text (list[str]):
        structured (list[StructuredOpeningHours]): List of iCalender-based structured representations of opening hours
        categories (list[CategoryRef] | Unset): The list of place categories, this set of opening hours refers to.
        is_open (bool | Unset):
    """

    text: list[str]
    structured: list[StructuredOpeningHours]
    categories: list[CategoryRef] | Unset = UNSET
    is_open: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        structured = []
        for structured_item_data in self.structured:
            structured_item = structured_item_data.to_dict()
            structured.append(structured_item)

        categories: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.to_dict()
                categories.append(categories_item)

        is_open = self.is_open

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "text": text,
            "structured": structured,
        })
        if categories is not UNSET:
            field_dict["categories"] = categories
        if is_open is not UNSET:
            field_dict["isOpen"] = is_open

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.category_ref import CategoryRef
        from ..models.structured_opening_hours import StructuredOpeningHours

        d = dict(src_dict)
        text = cast(list[str], d.pop("text"))

        structured = []
        _structured = d.pop("structured")
        for structured_item_data in _structured:
            structured_item = StructuredOpeningHours.from_dict(structured_item_data)

            structured.append(structured_item)

        _categories = d.pop("categories", UNSET)
        categories: list[CategoryRef] | Unset = UNSET
        if _categories is not UNSET:
            categories = []
            for categories_item_data in _categories:
                categories_item = CategoryRef.from_dict(categories_item_data)

                categories.append(categories_item)

        is_open = d.pop("isOpen", UNSET)

        opening_hours = cls(
            text=text,
            structured=structured,
            categories=categories,
            is_open=is_open,
        )

        opening_hours.additional_properties = d
        return opening_hours

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
