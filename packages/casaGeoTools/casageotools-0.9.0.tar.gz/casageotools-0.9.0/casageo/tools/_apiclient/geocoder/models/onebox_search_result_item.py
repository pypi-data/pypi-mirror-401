from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.onebox_search_result_item_address_block_type import (
    OneboxSearchResultItemAddressBlockType,
)
from ..models.onebox_search_result_item_administrative_area_type import (
    OneboxSearchResultItemAdministrativeAreaType,
)
from ..models.onebox_search_result_item_house_number_type import (
    OneboxSearchResultItemHouseNumberType,
)
from ..models.onebox_search_result_item_locality_type import (
    OneboxSearchResultItemLocalityType,
)
from ..models.onebox_search_result_item_result_type import (
    OneboxSearchResultItemResultType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.access_restriction_attributes import AccessRestrictionAttributes
    from ..models.address import Address
    from ..models.category import Category
    from ..models.chain import Chain
    from ..models.contact_information import ContactInformation
    from ..models.display_response_coordinate import DisplayResponseCoordinate
    from ..models.extended_access_point import ExtendedAccessPoint
    from ..models.extended_attribute import ExtendedAttribute
    from ..models.map_view import MapView
    from ..models.media import Media
    from ..models.opening_hours import OpeningHours
    from ..models.phonemes_section import PhonemesSection
    from ..models.street_info import StreetInfo
    from ..models.supplier_reference import SupplierReference
    from ..models.time_zone_info import TimeZoneInfo


T = TypeVar("T", bound="OneboxSearchResultItem")


@_attrs_define
class OneboxSearchResultItem:
    """
    Attributes:
        title (str): The localized display name of this result item.
        id (str): The unique identifier for the result item. This ID can be used for a Look Up by ID search as well.
        address (Address):
        political_view (str | Unset): ISO3 country code of the item political view (default for international). This
            response element is populated when the politicalView parameter is set in the query
        ontology_id (str | Unset): Related ontology ID
        result_type (OneboxSearchResultItemResultType | Unset):
            Type of the result item.

            Note: `addressBlock` result item is either a block or subblock.

            `resultType` values can get added to the list without further notice.
        house_number_type (OneboxSearchResultItemHouseNumberType | Unset): Indicates the address type which affects the
            precision of the address and the coordinate accuracy.

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
        address_block_type (OneboxSearchResultItemAddressBlockType | Unset):
            Type of the address block result if the `resultType` field is set to `addressBlock`.

            `addressBlockType` values can get added to the list without further notice.
        locality_type (OneboxSearchResultItemLocalityType | Unset):
            Type of the locality result if the `resultType` field is set to `locality`.

            `localityType` values can get added to the list without further notice.
        administrative_area_type (OneboxSearchResultItemAdministrativeAreaType | Unset):
            Type of the administrative area result if the `resultType` field is set to `administrativeArea`.

            `administrativeAreaType` values can get added to the list without further notice.
        position (DisplayResponseCoordinate | Unset):
        access (list[ExtendedAccessPoint] | Unset): Coordinates of the response item on a HERE map navigable link (for
            example, for driving or walking).

            When a response item is of type `"place"`, it can contain more than one access object.
            Each access object contains a position (`lat`, `lng`), with potentially a type (field `type`),
            a textual label (field `label`) and a `primary` boolean field set to true for the main access to the place.

            The first object in the `access` array is the primary access to the place.

            Response items of other types than `"place"` have a maximum of one access position.
        drive_through (bool | Unset): Set to `true` if the related business allows customers to purchase products
            (or use the service provided by the business) without leaving their cars.
        distance (int | Unset): The distance "as the crow flies" from the search center to this result item in meters.
            For example: "172039".

            When searching along a route this is the distance along the route plus the distance from the route polyline to
            this result item. Example: 172039.
        excursion_distance (int | Unset): Two times the distance from the polyline to this result item in meters while
            searching along the route
        map_view (MapView | Unset):
        categories (list[Category] | Unset): The list of categories assigned to this place.
        chains (list[Chain] | Unset): The list of chains assigned to this place.
        references (list[SupplierReference] | Unset): The list of supplier references available for this place.
        food_types (list[Category] | Unset): The list of food types assigned to this place.
        house_number_fallback (bool | Unset): If true, indicates that the requested house number was corrected to match
            the nearest known house number. This field is visible only when the value is true.
        contacts (list[ContactInformation] | Unset): Contact information like phone, email, WWW.
        opening_hours (list[OpeningHours] | Unset): A list of hours during which the place is open for business.
            This field is optional: When it is not present, it means that we are lacking data about the place opening hours.
            Days without opening hours have to be considered as closed.
        time_zone (TimeZoneInfo | Unset):
        extended (ExtendedAttribute | Unset):
        phonemes (PhonemesSection | Unset):
        media (Media | Unset):
        street_info (list[StreetInfo] | Unset): Street Details (only rendered if `show=streetInfo` is provided.)
        access_restrictions (list[AccessRestrictionAttributes] | Unset): A list of access restrictions related to a
            `place` result item.

            A place response item has a restricted access when the place is not publicly accessible without a specific
            authorization, membership or customer relationship.
            Examples: the place is for customers or visitors only.

            This field is optional: When it is not present, it means that the place response item has no known access
            restriction. Example: [{'categories': [{'id': '800-8500-0177'}], 'restricted': True}].
    """

    title: str
    id: str
    address: Address
    political_view: str | Unset = UNSET
    ontology_id: str | Unset = UNSET
    result_type: OneboxSearchResultItemResultType | Unset = UNSET
    house_number_type: OneboxSearchResultItemHouseNumberType | Unset = UNSET
    address_block_type: OneboxSearchResultItemAddressBlockType | Unset = UNSET
    locality_type: OneboxSearchResultItemLocalityType | Unset = UNSET
    administrative_area_type: OneboxSearchResultItemAdministrativeAreaType | Unset = (
        UNSET
    )
    position: DisplayResponseCoordinate | Unset = UNSET
    access: list[ExtendedAccessPoint] | Unset = UNSET
    drive_through: bool | Unset = UNSET
    distance: int | Unset = UNSET
    excursion_distance: int | Unset = UNSET
    map_view: MapView | Unset = UNSET
    categories: list[Category] | Unset = UNSET
    chains: list[Chain] | Unset = UNSET
    references: list[SupplierReference] | Unset = UNSET
    food_types: list[Category] | Unset = UNSET
    house_number_fallback: bool | Unset = UNSET
    contacts: list[ContactInformation] | Unset = UNSET
    opening_hours: list[OpeningHours] | Unset = UNSET
    time_zone: TimeZoneInfo | Unset = UNSET
    extended: ExtendedAttribute | Unset = UNSET
    phonemes: PhonemesSection | Unset = UNSET
    media: Media | Unset = UNSET
    street_info: list[StreetInfo] | Unset = UNSET
    access_restrictions: list[AccessRestrictionAttributes] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        id = self.id

        address = self.address.to_dict()

        political_view = self.political_view

        ontology_id = self.ontology_id

        result_type: str | Unset = UNSET
        if not isinstance(self.result_type, Unset):
            result_type = self.result_type.value

        house_number_type: str | Unset = UNSET
        if not isinstance(self.house_number_type, Unset):
            house_number_type = self.house_number_type.value

        address_block_type: str | Unset = UNSET
        if not isinstance(self.address_block_type, Unset):
            address_block_type = self.address_block_type.value

        locality_type: str | Unset = UNSET
        if not isinstance(self.locality_type, Unset):
            locality_type = self.locality_type.value

        administrative_area_type: str | Unset = UNSET
        if not isinstance(self.administrative_area_type, Unset):
            administrative_area_type = self.administrative_area_type.value

        position: dict[str, Any] | Unset = UNSET
        if not isinstance(self.position, Unset):
            position = self.position.to_dict()

        access: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.access, Unset):
            access = []
            for access_item_data in self.access:
                access_item = access_item_data.to_dict()
                access.append(access_item)

        drive_through = self.drive_through

        distance = self.distance

        excursion_distance = self.excursion_distance

        map_view: dict[str, Any] | Unset = UNSET
        if not isinstance(self.map_view, Unset):
            map_view = self.map_view.to_dict()

        categories: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.to_dict()
                categories.append(categories_item)

        chains: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.chains, Unset):
            chains = []
            for chains_item_data in self.chains:
                chains_item = chains_item_data.to_dict()
                chains.append(chains_item)

        references: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.references, Unset):
            references = []
            for references_item_data in self.references:
                references_item = references_item_data.to_dict()
                references.append(references_item)

        food_types: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.food_types, Unset):
            food_types = []
            for food_types_item_data in self.food_types:
                food_types_item = food_types_item_data.to_dict()
                food_types.append(food_types_item)

        house_number_fallback = self.house_number_fallback

        contacts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.contacts, Unset):
            contacts = []
            for contacts_item_data in self.contacts:
                contacts_item = contacts_item_data.to_dict()
                contacts.append(contacts_item)

        opening_hours: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.opening_hours, Unset):
            opening_hours = []
            for opening_hours_item_data in self.opening_hours:
                opening_hours_item = opening_hours_item_data.to_dict()
                opening_hours.append(opening_hours_item)

        time_zone: dict[str, Any] | Unset = UNSET
        if not isinstance(self.time_zone, Unset):
            time_zone = self.time_zone.to_dict()

        extended: dict[str, Any] | Unset = UNSET
        if not isinstance(self.extended, Unset):
            extended = self.extended.to_dict()

        phonemes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.phonemes, Unset):
            phonemes = self.phonemes.to_dict()

        media: dict[str, Any] | Unset = UNSET
        if not isinstance(self.media, Unset):
            media = self.media.to_dict()

        street_info: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.street_info, Unset):
            street_info = []
            for street_info_item_data in self.street_info:
                street_info_item = street_info_item_data.to_dict()
                street_info.append(street_info_item)

        access_restrictions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.access_restrictions, Unset):
            access_restrictions = []
            for access_restrictions_item_data in self.access_restrictions:
                access_restrictions_item = access_restrictions_item_data.to_dict()
                access_restrictions.append(access_restrictions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "title": title,
            "id": id,
            "address": address,
        })
        if political_view is not UNSET:
            field_dict["politicalView"] = political_view
        if ontology_id is not UNSET:
            field_dict["ontologyId"] = ontology_id
        if result_type is not UNSET:
            field_dict["resultType"] = result_type
        if house_number_type is not UNSET:
            field_dict["houseNumberType"] = house_number_type
        if address_block_type is not UNSET:
            field_dict["addressBlockType"] = address_block_type
        if locality_type is not UNSET:
            field_dict["localityType"] = locality_type
        if administrative_area_type is not UNSET:
            field_dict["administrativeAreaType"] = administrative_area_type
        if position is not UNSET:
            field_dict["position"] = position
        if access is not UNSET:
            field_dict["access"] = access
        if drive_through is not UNSET:
            field_dict["driveThrough"] = drive_through
        if distance is not UNSET:
            field_dict["distance"] = distance
        if excursion_distance is not UNSET:
            field_dict["excursionDistance"] = excursion_distance
        if map_view is not UNSET:
            field_dict["mapView"] = map_view
        if categories is not UNSET:
            field_dict["categories"] = categories
        if chains is not UNSET:
            field_dict["chains"] = chains
        if references is not UNSET:
            field_dict["references"] = references
        if food_types is not UNSET:
            field_dict["foodTypes"] = food_types
        if house_number_fallback is not UNSET:
            field_dict["houseNumberFallback"] = house_number_fallback
        if contacts is not UNSET:
            field_dict["contacts"] = contacts
        if opening_hours is not UNSET:
            field_dict["openingHours"] = opening_hours
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone
        if extended is not UNSET:
            field_dict["extended"] = extended
        if phonemes is not UNSET:
            field_dict["phonemes"] = phonemes
        if media is not UNSET:
            field_dict["media"] = media
        if street_info is not UNSET:
            field_dict["streetInfo"] = street_info
        if access_restrictions is not UNSET:
            field_dict["accessRestrictions"] = access_restrictions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.access_restriction_attributes import AccessRestrictionAttributes
        from ..models.address import Address
        from ..models.category import Category
        from ..models.chain import Chain
        from ..models.contact_information import ContactInformation
        from ..models.display_response_coordinate import DisplayResponseCoordinate
        from ..models.extended_access_point import ExtendedAccessPoint
        from ..models.extended_attribute import ExtendedAttribute
        from ..models.map_view import MapView
        from ..models.media import Media
        from ..models.opening_hours import OpeningHours
        from ..models.phonemes_section import PhonemesSection
        from ..models.street_info import StreetInfo
        from ..models.supplier_reference import SupplierReference
        from ..models.time_zone_info import TimeZoneInfo

        d = dict(src_dict)
        title = d.pop("title")

        id = d.pop("id")

        address = Address.from_dict(d.pop("address"))

        political_view = d.pop("politicalView", UNSET)

        ontology_id = d.pop("ontologyId", UNSET)

        _result_type = d.pop("resultType", UNSET)
        result_type: OneboxSearchResultItemResultType | Unset
        if isinstance(_result_type, Unset):
            result_type = UNSET
        else:
            result_type = OneboxSearchResultItemResultType(_result_type)

        _house_number_type = d.pop("houseNumberType", UNSET)
        house_number_type: OneboxSearchResultItemHouseNumberType | Unset
        if isinstance(_house_number_type, Unset):
            house_number_type = UNSET
        else:
            house_number_type = OneboxSearchResultItemHouseNumberType(
                _house_number_type
            )

        _address_block_type = d.pop("addressBlockType", UNSET)
        address_block_type: OneboxSearchResultItemAddressBlockType | Unset
        if isinstance(_address_block_type, Unset):
            address_block_type = UNSET
        else:
            address_block_type = OneboxSearchResultItemAddressBlockType(
                _address_block_type
            )

        _locality_type = d.pop("localityType", UNSET)
        locality_type: OneboxSearchResultItemLocalityType | Unset
        if isinstance(_locality_type, Unset):
            locality_type = UNSET
        else:
            locality_type = OneboxSearchResultItemLocalityType(_locality_type)

        _administrative_area_type = d.pop("administrativeAreaType", UNSET)
        administrative_area_type: OneboxSearchResultItemAdministrativeAreaType | Unset
        if isinstance(_administrative_area_type, Unset):
            administrative_area_type = UNSET
        else:
            administrative_area_type = OneboxSearchResultItemAdministrativeAreaType(
                _administrative_area_type
            )

        _position = d.pop("position", UNSET)
        position: DisplayResponseCoordinate | Unset
        if isinstance(_position, Unset):
            position = UNSET
        else:
            position = DisplayResponseCoordinate.from_dict(_position)

        _access = d.pop("access", UNSET)
        access: list[ExtendedAccessPoint] | Unset = UNSET
        if _access is not UNSET:
            access = []
            for access_item_data in _access:
                access_item = ExtendedAccessPoint.from_dict(access_item_data)

                access.append(access_item)

        drive_through = d.pop("driveThrough", UNSET)

        distance = d.pop("distance", UNSET)

        excursion_distance = d.pop("excursionDistance", UNSET)

        _map_view = d.pop("mapView", UNSET)
        map_view: MapView | Unset
        if isinstance(_map_view, Unset):
            map_view = UNSET
        else:
            map_view = MapView.from_dict(_map_view)

        _categories = d.pop("categories", UNSET)
        categories: list[Category] | Unset = UNSET
        if _categories is not UNSET:
            categories = []
            for categories_item_data in _categories:
                categories_item = Category.from_dict(categories_item_data)

                categories.append(categories_item)

        _chains = d.pop("chains", UNSET)
        chains: list[Chain] | Unset = UNSET
        if _chains is not UNSET:
            chains = []
            for chains_item_data in _chains:
                chains_item = Chain.from_dict(chains_item_data)

                chains.append(chains_item)

        _references = d.pop("references", UNSET)
        references: list[SupplierReference] | Unset = UNSET
        if _references is not UNSET:
            references = []
            for references_item_data in _references:
                references_item = SupplierReference.from_dict(references_item_data)

                references.append(references_item)

        _food_types = d.pop("foodTypes", UNSET)
        food_types: list[Category] | Unset = UNSET
        if _food_types is not UNSET:
            food_types = []
            for food_types_item_data in _food_types:
                food_types_item = Category.from_dict(food_types_item_data)

                food_types.append(food_types_item)

        house_number_fallback = d.pop("houseNumberFallback", UNSET)

        _contacts = d.pop("contacts", UNSET)
        contacts: list[ContactInformation] | Unset = UNSET
        if _contacts is not UNSET:
            contacts = []
            for contacts_item_data in _contacts:
                contacts_item = ContactInformation.from_dict(contacts_item_data)

                contacts.append(contacts_item)

        _opening_hours = d.pop("openingHours", UNSET)
        opening_hours: list[OpeningHours] | Unset = UNSET
        if _opening_hours is not UNSET:
            opening_hours = []
            for opening_hours_item_data in _opening_hours:
                opening_hours_item = OpeningHours.from_dict(opening_hours_item_data)

                opening_hours.append(opening_hours_item)

        _time_zone = d.pop("timeZone", UNSET)
        time_zone: TimeZoneInfo | Unset
        if isinstance(_time_zone, Unset):
            time_zone = UNSET
        else:
            time_zone = TimeZoneInfo.from_dict(_time_zone)

        _extended = d.pop("extended", UNSET)
        extended: ExtendedAttribute | Unset
        if isinstance(_extended, Unset):
            extended = UNSET
        else:
            extended = ExtendedAttribute.from_dict(_extended)

        _phonemes = d.pop("phonemes", UNSET)
        phonemes: PhonemesSection | Unset
        if isinstance(_phonemes, Unset):
            phonemes = UNSET
        else:
            phonemes = PhonemesSection.from_dict(_phonemes)

        _media = d.pop("media", UNSET)
        media: Media | Unset
        if isinstance(_media, Unset):
            media = UNSET
        else:
            media = Media.from_dict(_media)

        _street_info = d.pop("streetInfo", UNSET)
        street_info: list[StreetInfo] | Unset = UNSET
        if _street_info is not UNSET:
            street_info = []
            for street_info_item_data in _street_info:
                street_info_item = StreetInfo.from_dict(street_info_item_data)

                street_info.append(street_info_item)

        _access_restrictions = d.pop("accessRestrictions", UNSET)
        access_restrictions: list[AccessRestrictionAttributes] | Unset = UNSET
        if _access_restrictions is not UNSET:
            access_restrictions = []
            for access_restrictions_item_data in _access_restrictions:
                access_restrictions_item = AccessRestrictionAttributes.from_dict(
                    access_restrictions_item_data
                )

                access_restrictions.append(access_restrictions_item)

        onebox_search_result_item = cls(
            title=title,
            id=id,
            address=address,
            political_view=political_view,
            ontology_id=ontology_id,
            result_type=result_type,
            house_number_type=house_number_type,
            address_block_type=address_block_type,
            locality_type=locality_type,
            administrative_area_type=administrative_area_type,
            position=position,
            access=access,
            drive_through=drive_through,
            distance=distance,
            excursion_distance=excursion_distance,
            map_view=map_view,
            categories=categories,
            chains=chains,
            references=references,
            food_types=food_types,
            house_number_fallback=house_number_fallback,
            contacts=contacts,
            opening_hours=opening_hours,
            time_zone=time_zone,
            extended=extended,
            phonemes=phonemes,
            media=media,
            street_info=street_info,
            access_restrictions=access_restrictions,
        )

        onebox_search_result_item.additional_properties = d
        return onebox_search_result_item

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
