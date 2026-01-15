from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.autosuggest_query_result_item_result_type import (
    AutosuggestQueryResultItemResultType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.title_highlighting import TitleHighlighting


T = TypeVar("T", bound="AutosuggestQueryResultItem")


@_attrs_define
class AutosuggestQueryResultItem:
    """
    Attributes:
        title (str): The localized display name of this result item.
        id (str): The unique identifier for the result item. The identifier of an `AutosuggestQueryResultItem` cannot be
            used for a Lookup by ID search.
        result_type (AutosuggestQueryResultItemResultType | Unset):
            Type of the result item.

            Note: `addressBlock` result item is either a block or subblock.

            `resultType` values can get added to the list without further notice.
        no_result_on_follow_up (bool | Unset): `noResultOnFollowUp` is added with a value `true` when the `chainQuery`
            response item is providing a
            follow-up `href` likely to not lead to any result. If `noResultOnFollowUp` is not added, it is likely the
            follow-up `href` leads to places near the search center.
            Customers can use the `noResultOnFollowUp`, for example to not expose the `chainQuery` response item in their
            application, or
            signal where there is "no nearby result for the chain query".
        href (str | Unset): URL of the follow-up query
        highlights (TitleHighlighting | Unset):
    """

    title: str
    id: str
    result_type: AutosuggestQueryResultItemResultType | Unset = UNSET
    no_result_on_follow_up: bool | Unset = UNSET
    href: str | Unset = UNSET
    highlights: TitleHighlighting | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        id = self.id

        result_type: str | Unset = UNSET
        if not isinstance(self.result_type, Unset):
            result_type = self.result_type.value

        no_result_on_follow_up = self.no_result_on_follow_up

        href = self.href

        highlights: dict[str, Any] | Unset = UNSET
        if not isinstance(self.highlights, Unset):
            highlights = self.highlights.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "title": title,
            "id": id,
        })
        if result_type is not UNSET:
            field_dict["resultType"] = result_type
        if no_result_on_follow_up is not UNSET:
            field_dict["noResultOnFollowUp"] = no_result_on_follow_up
        if href is not UNSET:
            field_dict["href"] = href
        if highlights is not UNSET:
            field_dict["highlights"] = highlights

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.title_highlighting import TitleHighlighting

        d = dict(src_dict)
        title = d.pop("title")

        id = d.pop("id")

        _result_type = d.pop("resultType", UNSET)
        result_type: AutosuggestQueryResultItemResultType | Unset
        if isinstance(_result_type, Unset):
            result_type = UNSET
        else:
            result_type = AutosuggestQueryResultItemResultType(_result_type)

        no_result_on_follow_up = d.pop("noResultOnFollowUp", UNSET)

        href = d.pop("href", UNSET)

        _highlights = d.pop("highlights", UNSET)
        highlights: TitleHighlighting | Unset
        if isinstance(_highlights, Unset):
            highlights = UNSET
        else:
            highlights = TitleHighlighting.from_dict(_highlights)

        autosuggest_query_result_item = cls(
            title=title,
            id=id,
            result_type=result_type,
            no_result_on_follow_up=no_result_on_follow_up,
            href=href,
            highlights=highlights,
        )

        autosuggest_query_result_item.additional_properties = d
        return autosuggest_query_result_item

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
