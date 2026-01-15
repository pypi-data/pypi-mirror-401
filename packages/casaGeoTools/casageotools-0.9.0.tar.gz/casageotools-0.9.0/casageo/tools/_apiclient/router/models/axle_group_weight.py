from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AxleGroupWeight")


@_attrs_define
class AxleGroupWeight:
    """Contains the maximum allowed weight for an axle-group.

    Attributes:
        max_weight (int | Unset): Maximum weight of the axle-group-weight restriction, in kilograms.
        axle_group (str | Unset): Extensible enum: `single` `tandem` `triple` `quad` `quint` `...`
            Axle-group associated with the restriction.

            Possible values are:

            * single
            * tandem
            * triple
            * quad
            * quint
    """

    max_weight: int | Unset = UNSET
    axle_group: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_weight = self.max_weight

        axle_group = self.axle_group

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_weight is not UNSET:
            field_dict["maxWeight"] = max_weight
        if axle_group is not UNSET:
            field_dict["axleGroup"] = axle_group

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_weight = d.pop("maxWeight", UNSET)

        axle_group = d.pop("axleGroup", UNSET)

        axle_group_weight = cls(
            max_weight=max_weight,
            axle_group=axle_group,
        )

        axle_group_weight.additional_properties = d
        return axle_group_weight

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
