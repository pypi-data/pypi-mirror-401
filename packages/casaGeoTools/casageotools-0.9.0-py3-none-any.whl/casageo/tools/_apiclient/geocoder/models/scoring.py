from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.field_score import FieldScore


T = TypeVar("T", bound="Scoring")


@_attrs_define
class Scoring:
    """
    Attributes:
        query_score (float | Unset): Indicates how good the input matches the returned address. It is equal to 1 if all
            input tokens are recognized and matched.
        field_score (FieldScore | Unset):
    """

    query_score: float | Unset = UNSET
    field_score: FieldScore | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query_score = self.query_score

        field_score: dict[str, Any] | Unset = UNSET
        if not isinstance(self.field_score, Unset):
            field_score = self.field_score.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if query_score is not UNSET:
            field_dict["queryScore"] = query_score
        if field_score is not UNSET:
            field_dict["fieldScore"] = field_score

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.field_score import FieldScore

        d = dict(src_dict)
        query_score = d.pop("queryScore", UNSET)

        _field_score = d.pop("fieldScore", UNSET)
        field_score: FieldScore | Unset
        if isinstance(_field_score, Unset):
            field_score = UNSET
        else:
            field_score = FieldScore.from_dict(_field_score)

        scoring = cls(
            query_score=query_score,
            field_score=field_score,
        )

        scoring.additional_properties = d
        return scoring

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
