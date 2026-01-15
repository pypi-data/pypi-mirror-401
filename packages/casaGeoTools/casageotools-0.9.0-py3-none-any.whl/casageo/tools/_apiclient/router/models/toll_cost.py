from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.toll_collection_location import TollCollectionLocation
    from ..models.toll_fare import TollFare


T = TypeVar("T", bound="TollCost")


@_attrs_define
class TollCost:
    """Information for a single toll payment.

    Attributes:
        toll_system (str): The name of the toll system collecting the toll.

            **NOTE** This property is deprecated. For a toll cost associated with multiple toll systems this parameter will
            return only one toll system name. Use `tollSystems` property to get all the systems.
        toll_system_ref (int): Reference index of the affected toll system in the `tollSystems` array.

            **NOTE** This property is deprecated. For a toll cost associated with multiple systems this parameter will
            return only one system. Use `tollSystems` property to get all the systems.
        fares (list[TollFare]): The list of possible `Fare`s represents the various fares that may apply for the tolls.
            The specific fares can vary based on factors such as the time of day, payment method, and vehicle
            characteristics.

            **Note**: The router presents the relevant fare options based on the original query, on a best effort basis.
            The `Fare` object for tolls will always be of type `SinglePrice`, indicating a single price for the toll.
        toll_systems (list[int] | Unset): Reference indices of the associated toll system(s). These indices correspond
            to the `tollSystems` array in the enclosing section.

            A toll cost may be associated with multiple systems. For details, refer to this Developer Guide
            [tutorial](https://www.here.com/docs/bundle/routing-api-developer-guide-v8/page/tutorials/tolls-multiple-
            systems.html).
        country_code (str | Unset): ISO-3166-1 alpha-3 code Example: FRA.
        toll_collection_locations (list[TollCollectionLocation] | Unset): The toll places represent the location(s)
            where the fare is collected. For tolls measured by distance, both the entry and exit toll locations are
            returned. It's important to note that while both entry and exit toll locations are provided, the payment is
            typically made at only one of these places, which is usually the exit toll location.
    """

    toll_system: str
    toll_system_ref: int
    fares: list[TollFare]
    toll_systems: list[int] | Unset = UNSET
    country_code: str | Unset = UNSET
    toll_collection_locations: list[TollCollectionLocation] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        toll_system = self.toll_system

        toll_system_ref = self.toll_system_ref

        fares = []
        for fares_item_data in self.fares:
            fares_item = fares_item_data.to_dict()
            fares.append(fares_item)

        toll_systems: list[int] | Unset = UNSET
        if not isinstance(self.toll_systems, Unset):
            toll_systems = self.toll_systems

        country_code = self.country_code

        toll_collection_locations: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.toll_collection_locations, Unset):
            toll_collection_locations = []
            for toll_collection_locations_item_data in self.toll_collection_locations:
                toll_collection_locations_item = (
                    toll_collection_locations_item_data.to_dict()
                )
                toll_collection_locations.append(toll_collection_locations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "tollSystem": toll_system,
            "tollSystemRef": toll_system_ref,
            "fares": fares,
        })
        if toll_systems is not UNSET:
            field_dict["tollSystems"] = toll_systems
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code
        if toll_collection_locations is not UNSET:
            field_dict["tollCollectionLocations"] = toll_collection_locations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.toll_collection_location import TollCollectionLocation
        from ..models.toll_fare import TollFare

        d = dict(src_dict)
        toll_system = d.pop("tollSystem")

        toll_system_ref = d.pop("tollSystemRef")

        fares = []
        _fares = d.pop("fares")
        for fares_item_data in _fares:
            fares_item = TollFare.from_dict(fares_item_data)

            fares.append(fares_item)

        toll_systems = cast(list[int], d.pop("tollSystems", UNSET))

        country_code = d.pop("countryCode", UNSET)

        _toll_collection_locations = d.pop("tollCollectionLocations", UNSET)
        toll_collection_locations: list[TollCollectionLocation] | Unset = UNSET
        if _toll_collection_locations is not UNSET:
            toll_collection_locations = []
            for toll_collection_locations_item_data in _toll_collection_locations:
                toll_collection_locations_item = TollCollectionLocation.from_dict(
                    toll_collection_locations_item_data
                )

                toll_collection_locations.append(toll_collection_locations_item)

        toll_cost = cls(
            toll_system=toll_system,
            toll_system_ref=toll_system_ref,
            fares=fares,
            toll_systems=toll_systems,
            country_code=country_code,
            toll_collection_locations=toll_collection_locations,
        )

        toll_cost.additional_properties = d
        return toll_cost

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
