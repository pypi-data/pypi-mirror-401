from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.charging_station_place_side_of_street import (
    ChargingStationPlaceSideOfStreet,
)
from ..models.charging_station_place_type import ChargingStationPlaceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.charge_point_operator import ChargePointOperator
    from ..models.charging_connector_attributes import ChargingConnectorAttributes
    from ..models.charging_station_brand import ChargingStationBrand
    from ..models.e_mobility_service_provider import EMobilityServiceProvider
    from ..models.location import Location


T = TypeVar("T", bound="ChargingStationPlace")


@_attrs_define
class ChargingStationPlace:
    """A charging station

    Example:
        {'type': 'place', 'location': {'lat': 50.339167, 'lng': 18.93}}

    Attributes:
        type_ (ChargingStationPlaceType): Place type. Each place type can have extra attributes.

            **NOTE:** The list of possible place types could be extended in the future.
            The client application is expected to handle such a case gracefully.
        location (Location): Location on the Earth Example: {'lat': 52.531677, 'lng': 13.381777}.
        name (str | Unset): Human readable name of this charging station
        waypoint (int | Unset): If present, this place corresponds to the `via` in the request with the same index.

            Example:

            If the request contains `via=<a>&via=<b>`
            * the place corresponding to `<a>` in the response will have `waypoint: 0`
            * the place corresponding to `<b>` in the response will have `waypoint: 1`.

            Notes:
            * `waypoint` is not present for `origin` and `destination` places. `origin` and `destination` waypoints can be
            trivially identified in the response as the `departure` of the first section and the `arrival` of the final
            section, respectively.
            * `waypoint` is not present for any stops that are added automatically by the router.
        original_location (Location | Unset): Location on the Earth Example: {'lat': 52.531677, 'lng': 13.381777}.
        display_location (Location | Unset): Location on the Earth Example: {'lat': 52.531677, 'lng': 13.381777}.
        side_of_street (ChargingStationPlaceSideOfStreet | Unset): Location of the waypoint or destination, relative to
            the driving direction on the street/road.

            **NOTE:** Based on the original waypoint position and `sideOfStreetHint` waypoint property.
             - If `sideOfStreetHint` property is specified, it takes priority in determining the side of street in the
            response.
             - Nothing is returned in the response in case the side of street is ambiguous (too close to the street),
               or if the position is too far from the street.

            * 'left`: The left side of the street in relation to the driving direction of the route.
            * `right`: The right side of the street in relation to the driving direction of the route.
        id (str | Unset): Identifier of this charging station
        attributes (ChargingConnectorAttributes | Unset): Details of the connector that is suggested to be used in the
            section's `postAction` for charging.
        brand (ChargingStationBrand | Unset): Information regarding the charging station brand
        charge_point_operator (ChargePointOperator | Unset): Information about the charging station charge-point-
            operator
        matching_e_mobility_service_providers (list[EMobilityServiceProvider] | Unset): List of matched E-Mobility
            Service Providers.
            Populated only when `ev[eMobilityServiceProviderPreferences]` parameter was
            passed in query.

            **Note**:
            * This list reflects the subset of E-Mobility Service Providers supported by the charging station, from the list
            specified in the request parameter `ev[eMobilityServiceProviderPreferences]`.
    """

    type_: ChargingStationPlaceType
    location: Location
    name: str | Unset = UNSET
    waypoint: int | Unset = UNSET
    original_location: Location | Unset = UNSET
    display_location: Location | Unset = UNSET
    side_of_street: ChargingStationPlaceSideOfStreet | Unset = UNSET
    id: str | Unset = UNSET
    attributes: ChargingConnectorAttributes | Unset = UNSET
    brand: ChargingStationBrand | Unset = UNSET
    charge_point_operator: ChargePointOperator | Unset = UNSET
    matching_e_mobility_service_providers: list[EMobilityServiceProvider] | Unset = (
        UNSET
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        location = self.location.to_dict()

        name = self.name

        waypoint = self.waypoint

        original_location: dict[str, Any] | Unset = UNSET
        if not isinstance(self.original_location, Unset):
            original_location = self.original_location.to_dict()

        display_location: dict[str, Any] | Unset = UNSET
        if not isinstance(self.display_location, Unset):
            display_location = self.display_location.to_dict()

        side_of_street: str | Unset = UNSET
        if not isinstance(self.side_of_street, Unset):
            side_of_street = self.side_of_street.value

        id = self.id

        attributes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        brand: dict[str, Any] | Unset = UNSET
        if not isinstance(self.brand, Unset):
            brand = self.brand.to_dict()

        charge_point_operator: dict[str, Any] | Unset = UNSET
        if not isinstance(self.charge_point_operator, Unset):
            charge_point_operator = self.charge_point_operator.to_dict()

        matching_e_mobility_service_providers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.matching_e_mobility_service_providers, Unset):
            matching_e_mobility_service_providers = []
            for (
                matching_e_mobility_service_providers_item_data
            ) in self.matching_e_mobility_service_providers:
                matching_e_mobility_service_providers_item = (
                    matching_e_mobility_service_providers_item_data.to_dict()
                )
                matching_e_mobility_service_providers.append(
                    matching_e_mobility_service_providers_item
                )

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "location": location,
        })
        if name is not UNSET:
            field_dict["name"] = name
        if waypoint is not UNSET:
            field_dict["waypoint"] = waypoint
        if original_location is not UNSET:
            field_dict["originalLocation"] = original_location
        if display_location is not UNSET:
            field_dict["displayLocation"] = display_location
        if side_of_street is not UNSET:
            field_dict["sideOfStreet"] = side_of_street
        if id is not UNSET:
            field_dict["id"] = id
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if brand is not UNSET:
            field_dict["brand"] = brand
        if charge_point_operator is not UNSET:
            field_dict["chargePointOperator"] = charge_point_operator
        if matching_e_mobility_service_providers is not UNSET:
            field_dict["matchingEMobilityServiceProviders"] = (
                matching_e_mobility_service_providers
            )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.charge_point_operator import ChargePointOperator
        from ..models.charging_connector_attributes import ChargingConnectorAttributes
        from ..models.charging_station_brand import ChargingStationBrand
        from ..models.e_mobility_service_provider import EMobilityServiceProvider
        from ..models.location import Location

        d = dict(src_dict)
        type_ = ChargingStationPlaceType(d.pop("type"))

        location = Location.from_dict(d.pop("location"))

        name = d.pop("name", UNSET)

        waypoint = d.pop("waypoint", UNSET)

        _original_location = d.pop("originalLocation", UNSET)
        original_location: Location | Unset
        if isinstance(_original_location, Unset):
            original_location = UNSET
        else:
            original_location = Location.from_dict(_original_location)

        _display_location = d.pop("displayLocation", UNSET)
        display_location: Location | Unset
        if isinstance(_display_location, Unset):
            display_location = UNSET
        else:
            display_location = Location.from_dict(_display_location)

        _side_of_street = d.pop("sideOfStreet", UNSET)
        side_of_street: ChargingStationPlaceSideOfStreet | Unset
        if isinstance(_side_of_street, Unset):
            side_of_street = UNSET
        else:
            side_of_street = ChargingStationPlaceSideOfStreet(_side_of_street)

        id = d.pop("id", UNSET)

        _attributes = d.pop("attributes", UNSET)
        attributes: ChargingConnectorAttributes | Unset
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = ChargingConnectorAttributes.from_dict(_attributes)

        _brand = d.pop("brand", UNSET)
        brand: ChargingStationBrand | Unset
        if isinstance(_brand, Unset):
            brand = UNSET
        else:
            brand = ChargingStationBrand.from_dict(_brand)

        _charge_point_operator = d.pop("chargePointOperator", UNSET)
        charge_point_operator: ChargePointOperator | Unset
        if isinstance(_charge_point_operator, Unset):
            charge_point_operator = UNSET
        else:
            charge_point_operator = ChargePointOperator.from_dict(
                _charge_point_operator
            )

        _matching_e_mobility_service_providers = d.pop(
            "matchingEMobilityServiceProviders", UNSET
        )
        matching_e_mobility_service_providers: (
            list[EMobilityServiceProvider] | Unset
        ) = UNSET
        if _matching_e_mobility_service_providers is not UNSET:
            matching_e_mobility_service_providers = []
            for (
                matching_e_mobility_service_providers_item_data
            ) in _matching_e_mobility_service_providers:
                matching_e_mobility_service_providers_item = (
                    EMobilityServiceProvider.from_dict(
                        matching_e_mobility_service_providers_item_data
                    )
                )

                matching_e_mobility_service_providers.append(
                    matching_e_mobility_service_providers_item
                )

        charging_station_place = cls(
            type_=type_,
            location=location,
            name=name,
            waypoint=waypoint,
            original_location=original_location,
            display_location=display_location,
            side_of_street=side_of_street,
            id=id,
            attributes=attributes,
            brand=brand,
            charge_point_operator=charge_point_operator,
            matching_e_mobility_service_providers=matching_e_mobility_service_providers,
        )

        charging_station_place.additional_properties = d
        return charging_station_place

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
