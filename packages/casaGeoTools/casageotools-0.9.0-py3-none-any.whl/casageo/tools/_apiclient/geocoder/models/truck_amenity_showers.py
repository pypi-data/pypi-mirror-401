from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.truck_amenity_showers_type import TruckAmenityShowersType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TruckAmenityShowers")


@_attrs_define
class TruckAmenityShowers:
    """
    Attributes:
        type_ (TruckAmenityShowersType): **BETA, RESTRICTED**

            The kind of amenity

            Description of supported values:

            - **BETA, RESTRICTED** `showers`: showers onsite
        available (bool): **BETA, RESTRICTED**

            When set to:
            - `true` indicates that this amenity is available at this place
            - `false` indicates that this amenity is not available at this place
        number_of_showers (int | Unset): **BETA, RESTRICTED**

            Indicates the number of showers existing at the location.
    """

    type_: TruckAmenityShowersType
    available: bool
    number_of_showers: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        available = self.available

        number_of_showers = self.number_of_showers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "available": available,
        })
        if number_of_showers is not UNSET:
            field_dict["numberOfShowers"] = number_of_showers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = TruckAmenityShowersType(d.pop("type"))

        available = d.pop("available")

        number_of_showers = d.pop("numberOfShowers", UNSET)

        truck_amenity_showers = cls(
            type_=type_,
            available=available,
            number_of_showers=number_of_showers,
        )

        truck_amenity_showers.additional_properties = d
        return truck_amenity_showers

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
