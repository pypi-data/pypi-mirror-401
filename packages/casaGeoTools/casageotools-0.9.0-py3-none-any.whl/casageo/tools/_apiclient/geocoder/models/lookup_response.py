from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.lookup_response_address_block_type import LookupResponseAddressBlockType
from ..models.lookup_response_administrative_area_type import (
    LookupResponseAdministrativeAreaType,
)
from ..models.lookup_response_closed_permanently import LookupResponseClosedPermanently
from ..models.lookup_response_house_number_type import LookupResponseHouseNumberType
from ..models.lookup_response_locality_type import LookupResponseLocalityType
from ..models.lookup_response_result_type import LookupResponseResultType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.access_restriction_attributes import AccessRestrictionAttributes
    from ..models.address import Address
    from ..models.address_usage import AddressUsage
    from ..models.category import Category
    from ..models.chain import Chain
    from ..models.contact_information import ContactInformation
    from ..models.country_info import CountryInfo
    from ..models.display_response_coordinate import DisplayResponseCoordinate
    from ..models.extended_access_point import ExtendedAccessPoint
    from ..models.extended_attribute import ExtendedAttribute
    from ..models.map_reference_section import MapReferenceSection
    from ..models.map_view import MapView
    from ..models.media import Media
    from ..models.navigation_attributes import NavigationAttributes
    from ..models.opening_hours import OpeningHours
    from ..models.phonemes_section import PhonemesSection
    from ..models.postal_code_details_japan_post import PostalCodeDetailsJapanPost
    from ..models.postal_code_details_usps_zip import PostalCodeDetailsUspsZip
    from ..models.postal_code_details_usps_zip_plus_4 import (
        PostalCodeDetailsUspsZipPlus4,
    )
    from ..models.related_address import RelatedAddress
    from ..models.street_info import StreetInfo
    from ..models.supplier_reference import SupplierReference
    from ..models.time_zone_info import TimeZoneInfo


T = TypeVar("T", bound="LookupResponse")


@_attrs_define
class LookupResponse:
    """
    Attributes:
        title (str): The localized display name of this result item.
        id (str): The unique identifier for the result item. This ID can be used for a Look Up by ID search as well.
        address (Address):
        closed_permanently (LookupResponseClosedPermanently | Unset): **ALPHA**


            * `maybe`: The place has diminished confidence in the source data and is likely to be closed.
            * `yes`: The place is actually closed.
        political_view (str | Unset): ISO3 country code of the item political view (default for international). This
            response element is populated when the politicalView parameter is set in the query
        result_type (LookupResponseResultType | Unset):
            Type of the result item.

            Note: `addressBlock` result item is either a block or subblock.

            `resultType` values can get added to the list without further notice.
        house_number_type (LookupResponseHouseNumberType | Unset): Indicates the address type which affects the
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
        address_usage (AddressUsage | Unset):
        address_block_type (LookupResponseAddressBlockType | Unset):
            Type of the address block result if the `resultType` field is set to `addressBlock`.

            `addressBlockType` values can get added to the list without further notice.
        locality_type (LookupResponseLocalityType | Unset):
            Type of the locality result if the `resultType` field is set to `locality`.

            `localityType` values can get added to the list without further notice.
        administrative_area_type (LookupResponseAdministrativeAreaType | Unset):
            Type of the administrative area result if the `resultType` field is set to `administrativeArea`.

            `administrativeAreaType` values can get added to the list without further notice.
        house_number_fallback (bool | Unset): If true, indicates that the requested house number was corrected to match
            the nearest known house number. This field is visible only when the value is true.
        estimated_point_address (bool | Unset): If true, indicates that the coordinates of `position` and `access`
            points of the Point Address are
            estimated.
            This field is visible only for result items with resultType `houseNumber` and houseNumberType `PA` and
            only when the value is `true`
        postal_code_details (list[PostalCodeDetailsJapanPost | PostalCodeDetailsUspsZip | PostalCodeDetailsUspsZipPlus4]
            | Unset): Additional information for `postalCodePoint` results (only rendered if `show=postalCodeDetails` is
            provided and only in the countries which are using ZIP codes - USA, PRI, VIR, GUM, MNP, ASM and JPN)
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
        map_view (MapView | Unset):
        categories (list[Category] | Unset): The list of categories assigned to this place.
        chains (list[Chain] | Unset): The list of chains assigned to this place.
        references (list[SupplierReference] | Unset): The list of supplier references available for this place.
        food_types (list[Category] | Unset): The list of food types assigned to this place.
        contacts (list[ContactInformation] | Unset): Contact information like phone, email, WWW.
        opening_hours (list[OpeningHours] | Unset): A list of hours during which the place is open for business.
            This field is optional: When it is not present, it means that we are lacking data about the place opening hours.
            Days without opening hours have to be considered as closed.
        time_zone (TimeZoneInfo | Unset):
        media (Media | Unset):
        extended (ExtendedAttribute | Unset):
        phonemes (PhonemesSection | Unset):
        street_info (list[StreetInfo] | Unset): Street Details (only rendered if `show=streetInfo` is provided.)
        country_info (CountryInfo | Unset):
        map_references (MapReferenceSection | Unset):
        related (list[RelatedAddress] | Unset): List of related objects
        navigation_attributes (NavigationAttributes | Unset):
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
    closed_permanently: LookupResponseClosedPermanently | Unset = UNSET
    political_view: str | Unset = UNSET
    result_type: LookupResponseResultType | Unset = UNSET
    house_number_type: LookupResponseHouseNumberType | Unset = UNSET
    address_usage: AddressUsage | Unset = UNSET
    address_block_type: LookupResponseAddressBlockType | Unset = UNSET
    locality_type: LookupResponseLocalityType | Unset = UNSET
    administrative_area_type: LookupResponseAdministrativeAreaType | Unset = UNSET
    house_number_fallback: bool | Unset = UNSET
    estimated_point_address: bool | Unset = UNSET
    postal_code_details: (
        list[
            PostalCodeDetailsJapanPost
            | PostalCodeDetailsUspsZip
            | PostalCodeDetailsUspsZipPlus4
        ]
        | Unset
    ) = UNSET
    position: DisplayResponseCoordinate | Unset = UNSET
    access: list[ExtendedAccessPoint] | Unset = UNSET
    drive_through: bool | Unset = UNSET
    map_view: MapView | Unset = UNSET
    categories: list[Category] | Unset = UNSET
    chains: list[Chain] | Unset = UNSET
    references: list[SupplierReference] | Unset = UNSET
    food_types: list[Category] | Unset = UNSET
    contacts: list[ContactInformation] | Unset = UNSET
    opening_hours: list[OpeningHours] | Unset = UNSET
    time_zone: TimeZoneInfo | Unset = UNSET
    media: Media | Unset = UNSET
    extended: ExtendedAttribute | Unset = UNSET
    phonemes: PhonemesSection | Unset = UNSET
    street_info: list[StreetInfo] | Unset = UNSET
    country_info: CountryInfo | Unset = UNSET
    map_references: MapReferenceSection | Unset = UNSET
    related: list[RelatedAddress] | Unset = UNSET
    navigation_attributes: NavigationAttributes | Unset = UNSET
    access_restrictions: list[AccessRestrictionAttributes] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.postal_code_details_japan_post import PostalCodeDetailsJapanPost
        from ..models.postal_code_details_usps_zip import PostalCodeDetailsUspsZip

        title = self.title

        id = self.id

        address = self.address.to_dict()

        closed_permanently: str | Unset = UNSET
        if not isinstance(self.closed_permanently, Unset):
            closed_permanently = self.closed_permanently.value

        political_view = self.political_view

        result_type: str | Unset = UNSET
        if not isinstance(self.result_type, Unset):
            result_type = self.result_type.value

        house_number_type: str | Unset = UNSET
        if not isinstance(self.house_number_type, Unset):
            house_number_type = self.house_number_type.value

        address_usage: dict[str, Any] | Unset = UNSET
        if not isinstance(self.address_usage, Unset):
            address_usage = self.address_usage.to_dict()

        address_block_type: str | Unset = UNSET
        if not isinstance(self.address_block_type, Unset):
            address_block_type = self.address_block_type.value

        locality_type: str | Unset = UNSET
        if not isinstance(self.locality_type, Unset):
            locality_type = self.locality_type.value

        administrative_area_type: str | Unset = UNSET
        if not isinstance(self.administrative_area_type, Unset):
            administrative_area_type = self.administrative_area_type.value

        house_number_fallback = self.house_number_fallback

        estimated_point_address = self.estimated_point_address

        postal_code_details: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.postal_code_details, Unset):
            postal_code_details = []
            for postal_code_details_item_data in self.postal_code_details:
                postal_code_details_item: dict[str, Any]
                if isinstance(
                    postal_code_details_item_data, PostalCodeDetailsJapanPost
                ):
                    postal_code_details_item = postal_code_details_item_data.to_dict()
                elif isinstance(
                    postal_code_details_item_data, PostalCodeDetailsUspsZip
                ):
                    postal_code_details_item = postal_code_details_item_data.to_dict()
                else:
                    postal_code_details_item = postal_code_details_item_data.to_dict()

                postal_code_details.append(postal_code_details_item)

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

        media: dict[str, Any] | Unset = UNSET
        if not isinstance(self.media, Unset):
            media = self.media.to_dict()

        extended: dict[str, Any] | Unset = UNSET
        if not isinstance(self.extended, Unset):
            extended = self.extended.to_dict()

        phonemes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.phonemes, Unset):
            phonemes = self.phonemes.to_dict()

        street_info: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.street_info, Unset):
            street_info = []
            for street_info_item_data in self.street_info:
                street_info_item = street_info_item_data.to_dict()
                street_info.append(street_info_item)

        country_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.country_info, Unset):
            country_info = self.country_info.to_dict()

        map_references: dict[str, Any] | Unset = UNSET
        if not isinstance(self.map_references, Unset):
            map_references = self.map_references.to_dict()

        related: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.related, Unset):
            related = []
            for related_item_data in self.related:
                related_item = related_item_data.to_dict()
                related.append(related_item)

        navigation_attributes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.navigation_attributes, Unset):
            navigation_attributes = self.navigation_attributes.to_dict()

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
        if closed_permanently is not UNSET:
            field_dict["closedPermanently"] = closed_permanently
        if political_view is not UNSET:
            field_dict["politicalView"] = political_view
        if result_type is not UNSET:
            field_dict["resultType"] = result_type
        if house_number_type is not UNSET:
            field_dict["houseNumberType"] = house_number_type
        if address_usage is not UNSET:
            field_dict["addressUsage"] = address_usage
        if address_block_type is not UNSET:
            field_dict["addressBlockType"] = address_block_type
        if locality_type is not UNSET:
            field_dict["localityType"] = locality_type
        if administrative_area_type is not UNSET:
            field_dict["administrativeAreaType"] = administrative_area_type
        if house_number_fallback is not UNSET:
            field_dict["houseNumberFallback"] = house_number_fallback
        if estimated_point_address is not UNSET:
            field_dict["estimatedPointAddress"] = estimated_point_address
        if postal_code_details is not UNSET:
            field_dict["postalCodeDetails"] = postal_code_details
        if position is not UNSET:
            field_dict["position"] = position
        if access is not UNSET:
            field_dict["access"] = access
        if drive_through is not UNSET:
            field_dict["driveThrough"] = drive_through
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
        if contacts is not UNSET:
            field_dict["contacts"] = contacts
        if opening_hours is not UNSET:
            field_dict["openingHours"] = opening_hours
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone
        if media is not UNSET:
            field_dict["media"] = media
        if extended is not UNSET:
            field_dict["extended"] = extended
        if phonemes is not UNSET:
            field_dict["phonemes"] = phonemes
        if street_info is not UNSET:
            field_dict["streetInfo"] = street_info
        if country_info is not UNSET:
            field_dict["countryInfo"] = country_info
        if map_references is not UNSET:
            field_dict["mapReferences"] = map_references
        if related is not UNSET:
            field_dict["related"] = related
        if navigation_attributes is not UNSET:
            field_dict["navigationAttributes"] = navigation_attributes
        if access_restrictions is not UNSET:
            field_dict["accessRestrictions"] = access_restrictions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.access_restriction_attributes import AccessRestrictionAttributes
        from ..models.address import Address
        from ..models.address_usage import AddressUsage
        from ..models.category import Category
        from ..models.chain import Chain
        from ..models.contact_information import ContactInformation
        from ..models.country_info import CountryInfo
        from ..models.display_response_coordinate import DisplayResponseCoordinate
        from ..models.extended_access_point import ExtendedAccessPoint
        from ..models.extended_attribute import ExtendedAttribute
        from ..models.map_reference_section import MapReferenceSection
        from ..models.map_view import MapView
        from ..models.media import Media
        from ..models.navigation_attributes import NavigationAttributes
        from ..models.opening_hours import OpeningHours
        from ..models.phonemes_section import PhonemesSection
        from ..models.postal_code_details_japan_post import PostalCodeDetailsJapanPost
        from ..models.postal_code_details_usps_zip import PostalCodeDetailsUspsZip
        from ..models.postal_code_details_usps_zip_plus_4 import (
            PostalCodeDetailsUspsZipPlus4,
        )
        from ..models.related_address import RelatedAddress
        from ..models.street_info import StreetInfo
        from ..models.supplier_reference import SupplierReference
        from ..models.time_zone_info import TimeZoneInfo

        d = dict(src_dict)
        title = d.pop("title")

        id = d.pop("id")

        address = Address.from_dict(d.pop("address"))

        _closed_permanently = d.pop("closedPermanently", UNSET)
        closed_permanently: LookupResponseClosedPermanently | Unset
        if isinstance(_closed_permanently, Unset):
            closed_permanently = UNSET
        else:
            closed_permanently = LookupResponseClosedPermanently(_closed_permanently)

        political_view = d.pop("politicalView", UNSET)

        _result_type = d.pop("resultType", UNSET)
        result_type: LookupResponseResultType | Unset
        if isinstance(_result_type, Unset):
            result_type = UNSET
        else:
            result_type = LookupResponseResultType(_result_type)

        _house_number_type = d.pop("houseNumberType", UNSET)
        house_number_type: LookupResponseHouseNumberType | Unset
        if isinstance(_house_number_type, Unset):
            house_number_type = UNSET
        else:
            house_number_type = LookupResponseHouseNumberType(_house_number_type)

        _address_usage = d.pop("addressUsage", UNSET)
        address_usage: AddressUsage | Unset
        if isinstance(_address_usage, Unset):
            address_usage = UNSET
        else:
            address_usage = AddressUsage.from_dict(_address_usage)

        _address_block_type = d.pop("addressBlockType", UNSET)
        address_block_type: LookupResponseAddressBlockType | Unset
        if isinstance(_address_block_type, Unset):
            address_block_type = UNSET
        else:
            address_block_type = LookupResponseAddressBlockType(_address_block_type)

        _locality_type = d.pop("localityType", UNSET)
        locality_type: LookupResponseLocalityType | Unset
        if isinstance(_locality_type, Unset):
            locality_type = UNSET
        else:
            locality_type = LookupResponseLocalityType(_locality_type)

        _administrative_area_type = d.pop("administrativeAreaType", UNSET)
        administrative_area_type: LookupResponseAdministrativeAreaType | Unset
        if isinstance(_administrative_area_type, Unset):
            administrative_area_type = UNSET
        else:
            administrative_area_type = LookupResponseAdministrativeAreaType(
                _administrative_area_type
            )

        house_number_fallback = d.pop("houseNumberFallback", UNSET)

        estimated_point_address = d.pop("estimatedPointAddress", UNSET)

        _postal_code_details = d.pop("postalCodeDetails", UNSET)
        postal_code_details: (
            list[
                PostalCodeDetailsJapanPost
                | PostalCodeDetailsUspsZip
                | PostalCodeDetailsUspsZipPlus4
            ]
            | Unset
        ) = UNSET
        if _postal_code_details is not UNSET:
            postal_code_details = []
            for postal_code_details_item_data in _postal_code_details:

                def _parse_postal_code_details_item(
                    data: object,
                ) -> (
                    PostalCodeDetailsJapanPost
                    | PostalCodeDetailsUspsZip
                    | PostalCodeDetailsUspsZipPlus4
                ):
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        postal_code_details_item_type_0 = (
                            PostalCodeDetailsJapanPost.from_dict(data)
                        )

                        return postal_code_details_item_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        postal_code_details_item_type_1 = (
                            PostalCodeDetailsUspsZip.from_dict(data)
                        )

                        return postal_code_details_item_type_1
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    postal_code_details_item_type_2 = (
                        PostalCodeDetailsUspsZipPlus4.from_dict(data)
                    )

                    return postal_code_details_item_type_2

                postal_code_details_item = _parse_postal_code_details_item(
                    postal_code_details_item_data
                )

                postal_code_details.append(postal_code_details_item)

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

        _media = d.pop("media", UNSET)
        media: Media | Unset
        if isinstance(_media, Unset):
            media = UNSET
        else:
            media = Media.from_dict(_media)

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

        _street_info = d.pop("streetInfo", UNSET)
        street_info: list[StreetInfo] | Unset = UNSET
        if _street_info is not UNSET:
            street_info = []
            for street_info_item_data in _street_info:
                street_info_item = StreetInfo.from_dict(street_info_item_data)

                street_info.append(street_info_item)

        _country_info = d.pop("countryInfo", UNSET)
        country_info: CountryInfo | Unset
        if isinstance(_country_info, Unset):
            country_info = UNSET
        else:
            country_info = CountryInfo.from_dict(_country_info)

        _map_references = d.pop("mapReferences", UNSET)
        map_references: MapReferenceSection | Unset
        if isinstance(_map_references, Unset):
            map_references = UNSET
        else:
            map_references = MapReferenceSection.from_dict(_map_references)

        _related = d.pop("related", UNSET)
        related: list[RelatedAddress] | Unset = UNSET
        if _related is not UNSET:
            related = []
            for related_item_data in _related:
                related_item = RelatedAddress.from_dict(related_item_data)

                related.append(related_item)

        _navigation_attributes = d.pop("navigationAttributes", UNSET)
        navigation_attributes: NavigationAttributes | Unset
        if isinstance(_navigation_attributes, Unset):
            navigation_attributes = UNSET
        else:
            navigation_attributes = NavigationAttributes.from_dict(
                _navigation_attributes
            )

        _access_restrictions = d.pop("accessRestrictions", UNSET)
        access_restrictions: list[AccessRestrictionAttributes] | Unset = UNSET
        if _access_restrictions is not UNSET:
            access_restrictions = []
            for access_restrictions_item_data in _access_restrictions:
                access_restrictions_item = AccessRestrictionAttributes.from_dict(
                    access_restrictions_item_data
                )

                access_restrictions.append(access_restrictions_item)

        lookup_response = cls(
            title=title,
            id=id,
            address=address,
            closed_permanently=closed_permanently,
            political_view=political_view,
            result_type=result_type,
            house_number_type=house_number_type,
            address_usage=address_usage,
            address_block_type=address_block_type,
            locality_type=locality_type,
            administrative_area_type=administrative_area_type,
            house_number_fallback=house_number_fallback,
            estimated_point_address=estimated_point_address,
            postal_code_details=postal_code_details,
            position=position,
            access=access,
            drive_through=drive_through,
            map_view=map_view,
            categories=categories,
            chains=chains,
            references=references,
            food_types=food_types,
            contacts=contacts,
            opening_hours=opening_hours,
            time_zone=time_zone,
            media=media,
            extended=extended,
            phonemes=phonemes,
            street_info=street_info,
            country_info=country_info,
            map_references=map_references,
            related=related,
            navigation_attributes=navigation_attributes,
            access_restrictions=access_restrictions,
        )

        lookup_response.additional_properties = d
        return lookup_response

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
