from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EVPost")


@_attrs_define
class EVPost:
    """
    Attributes:
        preferred_brands (list[str] | Unset): An array of charging station brand IDs. If `makeReachable` is set to
            `true`, then charging stations from the specified brands
            will be preferred as potential charging stops, even if this makes the total route duration (travel time plus
            charging time) longer (up to 15 minutes per charging stop)

            Example of a parameter value preferring two charging station brands:
            ```
              {
                "preferredBrands": [
                  "6e1a148e8ddf06f613599134197b7c1c",
                  "6211c90a063d36429b599dda79ae85e3"
                ]
              }
              ```
        preferred_charge_point_operators (list[str] | Unset): An array of charge-point-operator identifiers. If
            `makeReachable` is set to `true`, then charging stations with one
            of the listed charge-point-operator ids will be preferred as potential charging stops, even if this makes the
            total
            route duration (travel time plus charging time) longer (up to 15 minutes per charging stop)

            Example with two preferred charge-point-operators specified:
              ```
              {
                "preferredChargePointOperators": [
                  "1f608648-cca5-11ed-bb1e-42010aa40002",
                  "1f90fdf0-cca5-11ed-be23-42010aa40002"
                ]
              }
              ```
    """

    preferred_brands: list[str] | Unset = UNSET
    preferred_charge_point_operators: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        preferred_brands: list[str] | Unset = UNSET
        if not isinstance(self.preferred_brands, Unset):
            preferred_brands = self.preferred_brands

        preferred_charge_point_operators: list[str] | Unset = UNSET
        if not isinstance(self.preferred_charge_point_operators, Unset):
            preferred_charge_point_operators = self.preferred_charge_point_operators

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if preferred_brands is not UNSET:
            field_dict["preferredBrands"] = preferred_brands
        if preferred_charge_point_operators is not UNSET:
            field_dict["preferredChargePointOperators"] = (
                preferred_charge_point_operators
            )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        preferred_brands = cast(list[str], d.pop("preferredBrands", UNSET))

        preferred_charge_point_operators = cast(
            list[str], d.pop("preferredChargePointOperators", UNSET)
        )

        ev_post = cls(
            preferred_brands=preferred_brands,
            preferred_charge_point_operators=preferred_charge_point_operators,
        )

        ev_post.additional_properties = d
        return ev_post

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
