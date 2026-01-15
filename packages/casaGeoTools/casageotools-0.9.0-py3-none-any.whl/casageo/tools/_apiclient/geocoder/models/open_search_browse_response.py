from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.browse_result_item import BrowseResultItem


T = TypeVar("T", bound="OpenSearchBrowseResponse")


@_attrs_define
class OpenSearchBrowseResponse:
    """
    Attributes:
        items (list[BrowseResultItem]): If the `offset` request parameter is not set, `items` contains a *full list* of
            JSON objects with a payload relevant to the request.
            The ranking order is from most to least relevant and is based on the matched location criteria.

            If the `offset` request parameter is set, `items` contains a contiguous subset of objects from the *full list*
            described before: A page of `<count>` objects at a certain `<offset>` value from the beginning of the *full
            list*.
        offset (int | Unset): **ALPHA**

            The `offset` value from the full list from which the page is taken.

            This is expected to reflect the `offset` request parameter value
        next_offset (int | Unset): **ALPHA**

            The `offset` value of the next page. This element is omitted on the last page.

            This response element is only set when in pagination mode (when the query parameter `offset` is set).
        count (int | Unset): **ALPHA**

            The actual page size: The number of objects returned in the `items` array.

            This response element is only set when in pagination mode (when the query parameter `offset` is set).
        limit (int | Unset): **ALPHA**

            Maximum number of objects in `items` as specified in request.

            This response element is only set when in pagination mode (when the query parameter `offset` is set).
    """

    items: list[BrowseResultItem]
    offset: int | Unset = UNSET
    next_offset: int | Unset = UNSET
    count: int | Unset = UNSET
    limit: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        offset = self.offset

        next_offset = self.next_offset

        count = self.count

        limit = self.limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "items": items,
        })
        if offset is not UNSET:
            field_dict["offset"] = offset
        if next_offset is not UNSET:
            field_dict["nextOffset"] = next_offset
        if count is not UNSET:
            field_dict["count"] = count
        if limit is not UNSET:
            field_dict["limit"] = limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.browse_result_item import BrowseResultItem

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = BrowseResultItem.from_dict(items_item_data)

            items.append(items_item)

        offset = d.pop("offset", UNSET)

        next_offset = d.pop("nextOffset", UNSET)

        count = d.pop("count", UNSET)

        limit = d.pop("limit", UNSET)

        open_search_browse_response = cls(
            items=items,
            offset=offset,
            next_offset=next_offset,
            count=count,
            limit=limit,
        )

        open_search_browse_response.additional_properties = d
        return open_search_browse_response

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
