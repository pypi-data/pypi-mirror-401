from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="QueryTermResultItem")


@_attrs_define
class QueryTermResultItem:
    """
    Attributes:
        term (str): The term that will be suggested to the user.
        replaces (str): The sub-string of the original query that is replaced by this Query Term.
        start (int): The start index in codepoints (inclusive) of the text replaced in the original query.
        end (int): The end index in codepoints (exclusive) of the text replaced in the original query.
    """

    term: str
    replaces: str
    start: int
    end: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        term = self.term

        replaces = self.replaces

        start = self.start

        end = self.end

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "term": term,
            "replaces": replaces,
            "start": start,
            "end": end,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        term = d.pop("term")

        replaces = d.pop("replaces")

        start = d.pop("start")

        end = d.pop("end")

        query_term_result_item = cls(
            term=term,
            replaces=replaces,
            start=start,
            end=end,
        )

        query_term_result_item.additional_properties = d
        return query_term_result_item

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
