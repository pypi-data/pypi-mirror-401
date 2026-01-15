from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.related_address_house_number_type import RelatedAddressHouseNumberType
from ..models.related_address_relationship import RelatedAddressRelationship
from ..models.related_address_result_type import RelatedAddressResultType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.basic_access_point import BasicAccessPoint
    from ..models.display_response_coordinate import DisplayResponseCoordinate
    from ..models.map_reference_section import MapReferenceSection
    from ..models.map_view import MapView
    from ..models.related_result_address import RelatedResultAddress


T = TypeVar("T", bound="RelatedAddress")


@_attrs_define
class RelatedAddress:
    """
    Attributes:
        relationship (RelatedAddressRelationship):

            Description of supported values:

            - **RESTRICTED** `MPA`: Micro Point Addresses related to a result items with
              `resultType` = `houseNumber` and `houseNumberType` = `PA`;
              for example, buildings, floors (levels) or suites (units)
              associated to this address. This type of relationship is
              only returned by the Lookup endpoint and the Geocode endpoint
              when the `showRelated=MPA` parameter is provided.
            - `intersection`: The Intersections nearest to the address. This type of relationship is
              only returned by Reverse Geocode, Geocode or Multi-Reverse Geocode
              endpoints when `showRelated=intersections` parameter is provided.
            - `nearbyAddress`: Nearby address on the same street of main result. This type of
              relationship is only returned by Reverse Geocode endpoint or
              Multi-Reverse Geocode endpoint when `showRelated=nearbyAddress`
              parameter is provided.
            - **RESTRICTED** `parentPA`: The Point Address to which the Micro Point Address
              belongs; for example the house number to which this
              suite is associated. This type of relationship is only
              returned by the Lookup, the Geocode and the (Multi) Reverse Geocode endpoints when
              the `showRelated=parentPA` parameter is provided.
        id (str): The ID of the related entity.
        title (str | Unset): The localized display name of this related entity.
        result_type (RelatedAddressResultType | Unset): The resultType of the related entity.
        house_number_type (RelatedAddressHouseNumberType | Unset): The houseNumberType of the related entity.

            Description of supported values:

            - **RESTRICTED** `MPA`: A Micro Point Address represents a secondary address for a Point
              Address; for example, building, floor (level) and suite (unit).
              Micro Point Addresses can be used to enhance Point Address with
              greater address detail and higher coordinate accuracy. This result
              type is only returned by Lookup, Geocode or (Multi) Reverse Geocode endpoints when
              `with=MPA` parameter is provided.
            - `PA`: A Point Address represents an individual address as a point object.
              Point Addresses are coming from trusted sources. There is a
              high certainty that the address exists at that position. A
              Point Address result contains two types of coordinates. One is the
              access point (or navigation coordinates), which is the point to
              start or end a drive. The other point is the position or display
              point. This point varies per source and country. The point can be
              the rooftop point, a point close to the building entry, or a point
              close to the building, driveway or parking lot that belongs to the
              building.
            - `interpolated`: An interpolated address. These are approximate positions as a
              result of a linear interpolation based on address ranges. Address
              ranges, especially in the USA, are typical per block. For
              interpolated addresses, we cannot say with confidence that the
              address exists in reality. But the interpolation provides a good
              location approximation that brings people in most use cases close
              to the target location. The access point of an interpolated address
              result is calculated based on the address range and the road
              geometry. The position (display) point is pre-configured offset
              from the street geometry. Compared to Point Addresses, interpolated
              addresses are less accurate.
        address (RelatedResultAddress | Unset):
        position (DisplayResponseCoordinate | Unset):
        access (list[BasicAccessPoint] | Unset): Coordinates of the response item on a HERE map navigable link (for
            example, for driving or walking).
        distance (int | Unset): The distance "as the crow flies" from the search center to this related address'
            position in meters.
            It is only returned by Reverse Geocode endpoint or Multi-Reverse Geocode endpoint.
        route_distance (int | Unset): The distance from routing position of the nearby address to the street result, the
            distance is
            calculated based on the underlying road geometry. It is only returned by Reverse Geocode endpoint or
            Multi-Reverse Geocode endpoint.
        bearing (int | Unset): Bearing (measured clockwise from true north) from the projected coordinate on the street
            to the
            display position of the related location. True clockwise degree, 0 is north. It is only returned by
            Reverse Geocode endpoint or Multi-Reverse Geocode endpoint.
        map_view (MapView | Unset):
        map_references (MapReferenceSection | Unset):
    """

    relationship: RelatedAddressRelationship
    id: str
    title: str | Unset = UNSET
    result_type: RelatedAddressResultType | Unset = UNSET
    house_number_type: RelatedAddressHouseNumberType | Unset = UNSET
    address: RelatedResultAddress | Unset = UNSET
    position: DisplayResponseCoordinate | Unset = UNSET
    access: list[BasicAccessPoint] | Unset = UNSET
    distance: int | Unset = UNSET
    route_distance: int | Unset = UNSET
    bearing: int | Unset = UNSET
    map_view: MapView | Unset = UNSET
    map_references: MapReferenceSection | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        relationship = self.relationship.value

        id = self.id

        title = self.title

        result_type: str | Unset = UNSET
        if not isinstance(self.result_type, Unset):
            result_type = self.result_type.value

        house_number_type: str | Unset = UNSET
        if not isinstance(self.house_number_type, Unset):
            house_number_type = self.house_number_type.value

        address: dict[str, Any] | Unset = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        position: dict[str, Any] | Unset = UNSET
        if not isinstance(self.position, Unset):
            position = self.position.to_dict()

        access: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.access, Unset):
            access = []
            for access_item_data in self.access:
                access_item = access_item_data.to_dict()
                access.append(access_item)

        distance = self.distance

        route_distance = self.route_distance

        bearing = self.bearing

        map_view: dict[str, Any] | Unset = UNSET
        if not isinstance(self.map_view, Unset):
            map_view = self.map_view.to_dict()

        map_references: dict[str, Any] | Unset = UNSET
        if not isinstance(self.map_references, Unset):
            map_references = self.map_references.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "relationship": relationship,
            "id": id,
        })
        if title is not UNSET:
            field_dict["title"] = title
        if result_type is not UNSET:
            field_dict["resultType"] = result_type
        if house_number_type is not UNSET:
            field_dict["houseNumberType"] = house_number_type
        if address is not UNSET:
            field_dict["address"] = address
        if position is not UNSET:
            field_dict["position"] = position
        if access is not UNSET:
            field_dict["access"] = access
        if distance is not UNSET:
            field_dict["distance"] = distance
        if route_distance is not UNSET:
            field_dict["routeDistance"] = route_distance
        if bearing is not UNSET:
            field_dict["bearing"] = bearing
        if map_view is not UNSET:
            field_dict["mapView"] = map_view
        if map_references is not UNSET:
            field_dict["mapReferences"] = map_references

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.basic_access_point import BasicAccessPoint
        from ..models.display_response_coordinate import DisplayResponseCoordinate
        from ..models.map_reference_section import MapReferenceSection
        from ..models.map_view import MapView
        from ..models.related_result_address import RelatedResultAddress

        d = dict(src_dict)
        relationship = RelatedAddressRelationship(d.pop("relationship"))

        id = d.pop("id")

        title = d.pop("title", UNSET)

        _result_type = d.pop("resultType", UNSET)
        result_type: RelatedAddressResultType | Unset
        if isinstance(_result_type, Unset):
            result_type = UNSET
        else:
            result_type = RelatedAddressResultType(_result_type)

        _house_number_type = d.pop("houseNumberType", UNSET)
        house_number_type: RelatedAddressHouseNumberType | Unset
        if isinstance(_house_number_type, Unset):
            house_number_type = UNSET
        else:
            house_number_type = RelatedAddressHouseNumberType(_house_number_type)

        _address = d.pop("address", UNSET)
        address: RelatedResultAddress | Unset
        if isinstance(_address, Unset):
            address = UNSET
        else:
            address = RelatedResultAddress.from_dict(_address)

        _position = d.pop("position", UNSET)
        position: DisplayResponseCoordinate | Unset
        if isinstance(_position, Unset):
            position = UNSET
        else:
            position = DisplayResponseCoordinate.from_dict(_position)

        _access = d.pop("access", UNSET)
        access: list[BasicAccessPoint] | Unset = UNSET
        if _access is not UNSET:
            access = []
            for access_item_data in _access:
                access_item = BasicAccessPoint.from_dict(access_item_data)

                access.append(access_item)

        distance = d.pop("distance", UNSET)

        route_distance = d.pop("routeDistance", UNSET)

        bearing = d.pop("bearing", UNSET)

        _map_view = d.pop("mapView", UNSET)
        map_view: MapView | Unset
        if isinstance(_map_view, Unset):
            map_view = UNSET
        else:
            map_view = MapView.from_dict(_map_view)

        _map_references = d.pop("mapReferences", UNSET)
        map_references: MapReferenceSection | Unset
        if isinstance(_map_references, Unset):
            map_references = UNSET
        else:
            map_references = MapReferenceSection.from_dict(_map_references)

        related_address = cls(
            relationship=relationship,
            id=id,
            title=title,
            result_type=result_type,
            house_number_type=house_number_type,
            address=address,
            position=position,
            access=access,
            distance=distance,
            route_distance=route_distance,
            bearing=bearing,
            map_view=map_view,
            map_references=map_references,
        )

        related_address.additional_properties = d
        return related_address

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
