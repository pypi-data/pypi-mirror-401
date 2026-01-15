from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.match_info_qq import MatchInfoQq
from ..types import UNSET, Unset

T = TypeVar("T", bound="MatchInfo")


@_attrs_define
class MatchInfo:
    """
    Attributes:
        start (int): First index of the matched range (0-based indexing, inclusive)
        end (int): One past the last index of the matched range (0-based indexing, exclusive); The difference between
            end and start gives the length of the term
        value (str): Matched term in the input string
        qq (MatchInfoQq | Unset): The matched qualified query field type. If this is not returned, then matched value
            refers to the freetext query
    """

    start: int
    end: int
    value: str
    qq: MatchInfoQq | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start = self.start

        end = self.end

        value = self.value

        qq: str | Unset = UNSET
        if not isinstance(self.qq, Unset):
            qq = self.qq.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "start": start,
            "end": end,
            "value": value,
        })
        if qq is not UNSET:
            field_dict["qq"] = qq

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start = d.pop("start")

        end = d.pop("end")

        value = d.pop("value")

        _qq = d.pop("qq", UNSET)
        qq: MatchInfoQq | Unset
        if isinstance(_qq, Unset):
            qq = UNSET
        else:
            qq = MatchInfoQq(_qq)

        match_info = cls(
            start=start,
            end=end,
            value=value,
            qq=qq,
        )

        match_info.additional_properties = d
        return match_info

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
