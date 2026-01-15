from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.range_ import Range


T = TypeVar("T", bound="TitleHighlighting")


@_attrs_define
class TitleHighlighting:
    """
    Attributes:
        title (list[Range] | Unset): Ranges of indexes that matched in the title attribute
    """

    title: list[Range] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.title, Unset):
            title = []
            for title_item_data in self.title:
                title_item = title_item_data.to_dict()
                title.append(title_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.range_ import Range

        d = dict(src_dict)
        _title = d.pop("title", UNSET)
        title: list[Range] | Unset = UNSET
        if _title is not UNSET:
            title = []
            for title_item_data in _title:
                title_item = Range.from_dict(title_item_data)

                title.append(title_item)

        title_highlighting = cls(
            title=title,
        )

        title_highlighting.additional_properties = d
        return title_highlighting

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
