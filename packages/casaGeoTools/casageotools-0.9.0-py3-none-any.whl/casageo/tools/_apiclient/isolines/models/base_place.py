from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.base_place_side_of_street import BasePlaceSideOfStreet
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.location import Location


T = TypeVar("T", bound="BasePlace")


@_attrs_define
class BasePlace:
    """
    Example:
        {'type': 'place', 'location': {'lat': 50.339167, 'lng': 18.93}}

    Attributes:
        type_ (str): Place type. Each place type can have extra attributes.

            **NOTE:** The list of possible place types could be extended in the future.
            The client application is expected to handle such a case gracefully.
        location (Location): Location on the Earth Example: {'lat': 52.531677, 'lng': 13.381777}.
        name (str | Unset): Location name
        original_location (Location | Unset): Location on the Earth Example: {'lat': 52.531677, 'lng': 13.381777}.
        display_location (Location | Unset): Location on the Earth Example: {'lat': 52.531677, 'lng': 13.381777}.
        side_of_street (BasePlaceSideOfStreet | Unset): Location of the waypoint or destination, relative to the driving
            direction on the street/road.

            **NOTE:** Based on the original waypoint position and `sideOfStreetHint` waypoint property.
             - If `sideOfStreetHint` property is specified, it takes priority in determining the side of street in the
            response.
             - Nothing is returned in the response in case the side of street is ambiguous (too close to the street),
               or if the position is too far from the street.

            * 'left`: The left side of the street in relation to the driving direction of the route.
            * `right`: The right side of the street in relation to the driving direction of the route.
    """

    type_: str
    location: Location
    name: str | Unset = UNSET
    original_location: Location | Unset = UNSET
    display_location: Location | Unset = UNSET
    side_of_street: BasePlaceSideOfStreet | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        location = self.location.to_dict()

        name = self.name

        original_location: dict[str, Any] | Unset = UNSET
        if not isinstance(self.original_location, Unset):
            original_location = self.original_location.to_dict()

        display_location: dict[str, Any] | Unset = UNSET
        if not isinstance(self.display_location, Unset):
            display_location = self.display_location.to_dict()

        side_of_street: str | Unset = UNSET
        if not isinstance(self.side_of_street, Unset):
            side_of_street = self.side_of_street.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "location": location,
        })
        if name is not UNSET:
            field_dict["name"] = name
        if original_location is not UNSET:
            field_dict["originalLocation"] = original_location
        if display_location is not UNSET:
            field_dict["displayLocation"] = display_location
        if side_of_street is not UNSET:
            field_dict["sideOfStreet"] = side_of_street

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.location import Location

        d = dict(src_dict)
        type_ = d.pop("type")

        location = Location.from_dict(d.pop("location"))

        name = d.pop("name", UNSET)

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
        side_of_street: BasePlaceSideOfStreet | Unset
        if isinstance(_side_of_street, Unset):
            side_of_street = UNSET
        else:
            side_of_street = BasePlaceSideOfStreet(_side_of_street)

        base_place = cls(
            type_=type_,
            location=location,
            name=name,
            original_location=original_location,
            display_location=display_location,
            side_of_street=side_of_street,
        )

        base_place.additional_properties = d
        return base_place

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
