from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.parking_lot_place_side_of_street import ParkingLotPlaceSideOfStreet
from ..models.parking_lot_place_type import ParkingLotPlaceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.location import Location
    from ..models.time_restricted_price import TimeRestrictedPrice


T = TypeVar("T", bound="ParkingLotPlace")


@_attrs_define
class ParkingLotPlace:
    """A parking lot

    Example:
        {'type': 'place', 'location': {'lat': 50.339167, 'lng': 18.93}}

    Attributes:
        type_ (ParkingLotPlaceType): Place type. Each place type can have extra attributes.

            **NOTE:** The list of possible place types could be extended in the future.
            The client application is expected to handle such a case gracefully.
        location (Location): Location on the Earth Example: {'lat': 52.531677, 'lng': 13.381777}.
        name (str | Unset): Location name
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
        side_of_street (ParkingLotPlaceSideOfStreet | Unset): Location of the waypoint or destination, relative to the
            driving direction on the street/road.

            **NOTE:** Based on the original waypoint position and `sideOfStreetHint` waypoint property.
             - If `sideOfStreetHint` property is specified, it takes priority in determining the side of street in the
            response.
             - Nothing is returned in the response in case the side of street is ambiguous (too close to the street),
               or if the position is too far from the street.

            * 'left`: The left side of the street in relation to the driving direction of the route.
            * `right`: The right side of the street in relation to the driving direction of the route.
        id (str | Unset): Identifier of this parking lot
        attributes (list[str] | Unset): Attributes of a parking lot.
        rates (list[TimeRestrictedPrice] | Unset): List of possible parking rates for this facility. Different rates can
            apply depending on the day, time of the day or parking duration.
    """

    type_: ParkingLotPlaceType
    location: Location
    name: str | Unset = UNSET
    waypoint: int | Unset = UNSET
    original_location: Location | Unset = UNSET
    display_location: Location | Unset = UNSET
    side_of_street: ParkingLotPlaceSideOfStreet | Unset = UNSET
    id: str | Unset = UNSET
    attributes: list[str] | Unset = UNSET
    rates: list[TimeRestrictedPrice] | Unset = UNSET
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

        attributes: list[str] | Unset = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes

        rates: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.rates, Unset):
            rates = []
            for rates_item_data in self.rates:
                rates_item = rates_item_data.to_dict()
                rates.append(rates_item)

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
        if rates is not UNSET:
            field_dict["rates"] = rates

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.location import Location
        from ..models.time_restricted_price import TimeRestrictedPrice

        d = dict(src_dict)
        type_ = ParkingLotPlaceType(d.pop("type"))

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
        side_of_street: ParkingLotPlaceSideOfStreet | Unset
        if isinstance(_side_of_street, Unset):
            side_of_street = UNSET
        else:
            side_of_street = ParkingLotPlaceSideOfStreet(_side_of_street)

        id = d.pop("id", UNSET)

        attributes = cast(list[str], d.pop("attributes", UNSET))

        _rates = d.pop("rates", UNSET)
        rates: list[TimeRestrictedPrice] | Unset = UNSET
        if _rates is not UNSET:
            rates = []
            for rates_item_data in _rates:
                rates_item = TimeRestrictedPrice.from_dict(rates_item_data)

                rates.append(rates_item)

        parking_lot_place = cls(
            type_=type_,
            location=location,
            name=name,
            waypoint=waypoint,
            original_location=original_location,
            display_location=display_location,
            side_of_street=side_of_street,
            id=id,
            attributes=attributes,
            rates=rates,
        )

        parking_lot_place.additional_properties = d
        return parking_lot_place

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
