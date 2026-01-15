from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VehicleRestrictionMaxWeight")


@_attrs_define
class VehicleRestrictionMaxWeight:
    """Contains the maximum permitted weight, specified in kilograms, along with the specific type of the maximum permitted
    weight restriction.

        Attributes:
            value (int | Unset):
            type_ (str | Unset): Extensible enum: `empty` `gross` `current` `unknown` `...`
                Represents the specific type of the maximum permitted weight restriction.
                * `empty`: Restriction is for empty weight of the vehicle combination.
                * `gross`: Restriction is for gross weight.
                * `current`: Restriction is for current weight.
                * `unknown`: Restriction may apply to gross or current weight. Specific `type` data for the restriction is not
                available.

                **NOTES:**
                * A restriction of type `unknown` may change to `gross` or `current` when data becomes available in future.
                * A restriction of type `gross` or `current` may also change to a different type if actual regulation changes.
    """

    value: int | Unset = UNSET
    type_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value", UNSET)

        type_ = d.pop("type", UNSET)

        vehicle_restriction_max_weight = cls(
            value=value,
            type_=type_,
        )

        vehicle_restriction_max_weight.additional_properties = d
        return vehicle_restriction_max_weight

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
