from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.truck_amenity_generic_type import TruckAmenityGenericType

T = TypeVar("T", bound="TruckAmenityGeneric")


@_attrs_define
class TruckAmenityGeneric:
    """
    Attributes:
        type_ (TruckAmenityGenericType): **BETA, RESTRICTED**

            The kind of amenity

            Description of supported values:

            - **BETA, RESTRICTED** `carWash`: car washing and/or detailing services
            - **BETA, RESTRICTED** `chemicalToiletDisposal`: a waste disposal station, for use in emptying and cleaning
            chemical toilets
            - **BETA, RESTRICTED** `convenienceStore`: a convenience store can be found at the location
            - **BETA, RESTRICTED** `highCanopy`: High canopy at fueling station/truck stop. This references the canopy
            height over the pumps being at a height for most trucks to enter.
            - **BETA, RESTRICTED** `idleReduction`: idle reduction system onsite
            - **BETA, RESTRICTED** `nightParkingOnly`: parking is restricted to night hours only
            - **BETA, RESTRICTED** `paidParking`: A fee is required to use the truck parking space.
            - **BETA, RESTRICTED** `parking`: truck parking onsite or nearby
            - **BETA, RESTRICTED** `powerSupply`: power supply, for use in maintaining the temperature of refrigerated
            trucks
            - **BETA, RESTRICTED** `reservableParking`: The truck parking space requires advance booking for a defined time
            interval.
            - **BETA, RESTRICTED** `secureParking`: secure parking location
            - **BETA, RESTRICTED** `truckScales`: truck scales onsite or nearby
            - **BETA, RESTRICTED** `truckService`: truck service onsite or nearby
            - **BETA, RESTRICTED** `truckStop`: a truck stop
            - **BETA, RESTRICTED** `truckWash`: truck wash onsite or nearby
            - **BETA, RESTRICTED** `wifi`: Wi-Fi access
        available (bool): **BETA, RESTRICTED**

            When set to:
            - `true` indicates that this amenity is available at this place
            - `false` indicates that this amenity is not available at this place
    """

    type_: TruckAmenityGenericType
    available: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        available = self.available

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "available": available,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = TruckAmenityGenericType(d.pop("type"))

        available = d.pop("available")

        truck_amenity_generic = cls(
            type_=type_,
            available=available,
        )

        truck_amenity_generic.additional_properties = d
        return truck_amenity_generic

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
