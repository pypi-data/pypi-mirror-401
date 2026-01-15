from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.fuel_station_fuel_types_item import FuelStationFuelTypesItem
from ..models.fuel_station_minimum_truck_class import FuelStationMinimumTruckClass
from ..types import UNSET, Unset

T = TypeVar("T", bound="FuelStation")


@_attrs_define
class FuelStation:
    """
    Attributes:
        minimum_truck_class (FuelStationMinimumTruckClass | Unset): **BETA, RESTRICTED**

            All place results returned with a category `700-7600-0116`, `700-7600-0000`, `700-7600-0444`, or `700-7900-0132`
            that serves truck fuel types with minimum supported truck class specified in this parameter.
            See the related [Appendix](https://www.here.com/docs/bundle/geocoding-and-search-api-developer-
            guide/page/topics-places/places-category-system-full.html#700-business-and-services)
            for details about those place category IDs.

            Caution: Note that this filter will be applied to place results regardless of the query intent.
            For example Places with both a gas station and a grocery category will be returned to a "grocery" query
            only if the place truck classes complies with the values of the query `fuelStation[minimumTruckClass]` values.

            Description of supported values:

            - **BETA, RESTRICTED** `heavy`: Medium and Heavy trucks are allowed to fuel in the gas station
            - **BETA, RESTRICTED** `medium`: Only medium size truck is allowed to fuel in the gas station Example: medium.
        fuel_types (list[FuelStationFuelTypesItem] | Unset): **BETA, RESTRICTED**

            All place results returned with a category `700-7600-0116`, `700-7600-0000`, `700-7600-0444`, or `700-7900-0132`
            serve at least one fuel type specified in the comma-separated values of this parameter.
            See the related [Appendix](https://www.here.com/docs/bundle/geocoding-and-search-api-developer-
            guide/page/topics-places/places-category-system-full.html#700-business-and-services)
            for details about those place category IDs.

            Caution: Note that this filter will be applied to place results regardless of the query intent.
            For example Places with both a gas station and a grocery category will be returned to a "grocery" query
            only if the place fuel types complies with the values of the query `fuelStation[fuelTypes]` values.

            Description of supported values:

            - **BETA, RESTRICTED** `biodiesel`: bio-diesel
            - **BETA, RESTRICTED** `cng`: compressed natural gas (CNG)
            - **BETA, RESTRICTED** `diesel`: diesel
            - **BETA, RESTRICTED** `diesel_with_additives`: diesel with additives
            - **BETA, RESTRICTED** `e10`: E10 (10% ethanol)
            - **BETA, RESTRICTED** `e20`: E20 (20% ethanol)
            - **BETA, RESTRICTED** `e85`: E85 (minimum 70% ethanol blended gasoline)
            - **BETA, RESTRICTED** `ethanol`: ethanol fuel (when specific type is not known, such as E10, E85)
            - **BETA, RESTRICTED** `ethanol_with_additives`: ethanol with additives
            - **BETA, RESTRICTED** `gasoline`: gasoline
            - **BETA, RESTRICTED** `hvo`: hydrotreated vegetable oil fuel
            - **BETA, RESTRICTED** `hydrogen`: hydrogen
            - **BETA, RESTRICTED** `lng`: liquefied natural gas (LNG)
            - **BETA, RESTRICTED** `lpg`: liquefied petroleum gas (LPG)
            - **BETA, RESTRICTED** `midgrade`: midgrade octane rating
            - **BETA, RESTRICTED** `octane_100`: fuel that consists of 100% octane
            - **BETA, RESTRICTED** `octane_87`: fuel that consists of an octane / gasoline blend with 87% octane / 13%
            gasoline
            - **BETA, RESTRICTED** `octane_89`: fuel that consists of an octane / gasoline blend with 89% octane / 11%
            gasoline
            - **BETA, RESTRICTED** `octane_90`: fuel that consists of an octane / gasoline blend with 90% octane / 10%
            gasoline
            - **BETA, RESTRICTED** `octane_91`: fuel that consists of an octane / gasoline blend with 91% octane / 9%
            gasoline
            - **BETA, RESTRICTED** `octane_92`: fuel that consists of an octane / gasoline blend with 92% octane / 8%
            gasoline
            - **BETA, RESTRICTED** `octane_93`: fuel that consists of octane / gasoline blend with 93% octane / 7% gasoline
            - **BETA, RESTRICTED** `octane_95`: fuel that consists of an octane / gasoline blend with 95% octane / 5%
            gasoline
            - **BETA, RESTRICTED** `octane_98`:  fuel that consists of an octane / gasoline blend with 98% octane / 2%
            gasoline
            - **BETA, RESTRICTED** `premium`: premium octane rating
            - **BETA, RESTRICTED** `regular`: regular octance rating
            - **BETA, RESTRICTED** `truck_cng`: compressed natural gas (CNG) fuel for truck
            - **BETA, RESTRICTED** `truck_diesel`: diesel fuel for truck
            - **BETA, RESTRICTED** `truck_hydrogen`: hydrogen fuel for truck
            - **BETA, RESTRICTED** `truck_lng`: liquefied natural gas (LNG) fuel for truck Example: ['biodiesel', 'diesel',
            'truck_diesel'].
    """

    minimum_truck_class: FuelStationMinimumTruckClass | Unset = UNSET
    fuel_types: list[FuelStationFuelTypesItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        minimum_truck_class: str | Unset = UNSET
        if not isinstance(self.minimum_truck_class, Unset):
            minimum_truck_class = self.minimum_truck_class.value

        fuel_types: list[str] | Unset = UNSET
        if not isinstance(self.fuel_types, Unset):
            fuel_types = []
            for fuel_types_item_data in self.fuel_types:
                fuel_types_item = fuel_types_item_data.value
                fuel_types.append(fuel_types_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if minimum_truck_class is not UNSET:
            field_dict["minimumTruckClass"] = minimum_truck_class
        if fuel_types is not UNSET:
            field_dict["fuelTypes"] = fuel_types

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _minimum_truck_class = d.pop("minimumTruckClass", UNSET)
        minimum_truck_class: FuelStationMinimumTruckClass | Unset
        if isinstance(_minimum_truck_class, Unset):
            minimum_truck_class = UNSET
        else:
            minimum_truck_class = FuelStationMinimumTruckClass(_minimum_truck_class)

        _fuel_types = d.pop("fuelTypes", UNSET)
        fuel_types: list[FuelStationFuelTypesItem] | Unset = UNSET
        if _fuel_types is not UNSET:
            fuel_types = []
            for fuel_types_item_data in _fuel_types:
                fuel_types_item = FuelStationFuelTypesItem(fuel_types_item_data)

                fuel_types.append(fuel_types_item)

        fuel_station = cls(
            minimum_truck_class=minimum_truck_class,
            fuel_types=fuel_types,
        )

        fuel_station.additional_properties = d
        return fuel_station

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
