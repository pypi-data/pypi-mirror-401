from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.reverse_geocode_result_item import ReverseGeocodeResultItem


T = TypeVar("T", bound="OpenSearchMultiReverseGeocodeResponseItem")


@_attrs_define
class OpenSearchMultiReverseGeocodeResponseItem:
    """
    Attributes:
        id (str): The ID for the query provided by the client
        items (list[ReverseGeocodeResultItem]): The results are presented as a JSON list of candidates in ranked order
            (most-likely to least-likely) based on the matched location criteria.
    """

    id: str
    items: list[ReverseGeocodeResultItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "items": items,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reverse_geocode_result_item import ReverseGeocodeResultItem

        d = dict(src_dict)
        id = d.pop("id")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = ReverseGeocodeResultItem.from_dict(items_item_data)

            items.append(items_item)

        open_search_multi_reverse_geocode_response_item = cls(
            id=id,
            items=items,
        )

        open_search_multi_reverse_geocode_response_item.additional_properties = d
        return open_search_multi_reverse_geocode_response_item

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
