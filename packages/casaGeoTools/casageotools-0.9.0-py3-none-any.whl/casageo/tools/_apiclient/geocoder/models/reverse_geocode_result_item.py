from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.reverse_geocode_result_item_address_block_type import (
    ReverseGeocodeResultItemAddressBlockType,
)
from ..models.reverse_geocode_result_item_administrative_area_type import (
    ReverseGeocodeResultItemAdministrativeAreaType,
)
from ..models.reverse_geocode_result_item_house_number_type import (
    ReverseGeocodeResultItemHouseNumberType,
)
from ..models.reverse_geocode_result_item_locality_type import (
    ReverseGeocodeResultItemLocalityType,
)
from ..models.reverse_geocode_result_item_result_type import (
    ReverseGeocodeResultItemResultType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.address_usage import AddressUsage
    from ..models.basic_access_point import BasicAccessPoint
    from ..models.category import Category
    from ..models.country_info import CountryInfo
    from ..models.display_response_coordinate import DisplayResponseCoordinate
    from ..models.map_reference_section import MapReferenceSection
    from ..models.map_view import MapView
    from ..models.navigation_attributes import NavigationAttributes
    from ..models.postal_code_details_usps_zip import PostalCodeDetailsUspsZip
    from ..models.postal_code_details_usps_zip_plus_4 import (
        PostalCodeDetailsUspsZipPlus4,
    )
    from ..models.related_address import RelatedAddress
    from ..models.rgc_address import RgcAddress
    from ..models.street_info import StreetInfo
    from ..models.time_zone_info import TimeZoneInfo


T = TypeVar("T", bound="ReverseGeocodeResultItem")


@_attrs_define
class ReverseGeocodeResultItem:
    """
    Attributes:
        title (str): The localized display name of this result item.
        id (str): The unique identifier for the result item. This ID can be used for a Look Up by ID search as well.
        address (RgcAddress):
        political_view (str | Unset): ISO3 country code of the item political view (default for international). This
            response element is populated when the politicalView parameter is set in the query
        result_type (ReverseGeocodeResultItemResultType | Unset):
            Type of the result item.

            Note: `addressBlock` result item is either a block or subblock.

            `resultType` values can get added to the list without further notice.
        house_number_type (ReverseGeocodeResultItemHouseNumberType | Unset): Indicates the address type which affects
            the precision of the address and the coordinate accuracy.

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
        address_block_type (ReverseGeocodeResultItemAddressBlockType | Unset):
            Type of the address block result if the `resultType` field is set to `addressBlock`.

            `addressBlockType` values can get added to the list without further notice.
        locality_type (ReverseGeocodeResultItemLocalityType | Unset):
            Type of the locality result if the `resultType` field is set to `locality`.

            `localityType` values can get added to the list without further notice.
        administrative_area_type (ReverseGeocodeResultItemAdministrativeAreaType | Unset):
            Type of the administrative area result if the `resultType` field is set to `administrativeArea`.

            `administrativeAreaType` values can get added to the list without further notice.
        postal_code_details (list[PostalCodeDetailsUspsZip | PostalCodeDetailsUspsZipPlus4] | Unset): Additional
            information for `postalCodePoint` results (only rendered if `show=postalCodeDetails` is
            provided and only in the countries which are using ZIP codes - USA, PRI, VIR, GUM, MNP, ASM and JPN)
        position (DisplayResponseCoordinate | Unset):
        access (list[BasicAccessPoint] | Unset): Coordinates of the response item on a HERE map navigable link (for
            example, for driving or walking).
        distance (int | Unset): The distance "as the crow flies" from the search center to this result item in meters.
            For example: "172039" Example: 172039.
        map_view (MapView | Unset):
        categories (list[Category] | Unset): The list of categories assigned to this place.
        food_types (list[Category] | Unset): The list of food types assigned to this place.
        house_number_fallback (bool | Unset): If true, indicates that the requested house number was corrected to match
            the nearest known house number. This field is visible only when the value is true.
        estimated_point_address (bool | Unset): If true, indicates that the coordinates of `position` and `access`
            points of the Point Address are
            estimated.
            This field is visible only for result items with resultType `houseNumber` and houseNumberType `PA` and
            only when the value is `true`
        time_zone (TimeZoneInfo | Unset):
        street_info (list[StreetInfo] | Unset): Street Details (only rendered if `show=streetInfo` is provided.)
        country_info (CountryInfo | Unset):
        estimated_area_fallback (bool | Unset): **ALPHA**

            Indicates that the admin result is not retrieved from a carto shape but from the closest street.
            (Only rendered, if `with=estimatedAreaFallback` is provided.)
        map_references (MapReferenceSection | Unset):
        related (list[RelatedAddress] | Unset): List of related objects
        navigation_attributes (NavigationAttributes | Unset):
    """

    title: str
    id: str
    address: RgcAddress
    political_view: str | Unset = UNSET
    result_type: ReverseGeocodeResultItemResultType | Unset = UNSET
    house_number_type: ReverseGeocodeResultItemHouseNumberType | Unset = UNSET
    address_usage: AddressUsage | Unset = UNSET
    address_block_type: ReverseGeocodeResultItemAddressBlockType | Unset = UNSET
    locality_type: ReverseGeocodeResultItemLocalityType | Unset = UNSET
    administrative_area_type: ReverseGeocodeResultItemAdministrativeAreaType | Unset = (
        UNSET
    )
    postal_code_details: (
        list[PostalCodeDetailsUspsZip | PostalCodeDetailsUspsZipPlus4] | Unset
    ) = UNSET
    position: DisplayResponseCoordinate | Unset = UNSET
    access: list[BasicAccessPoint] | Unset = UNSET
    distance: int | Unset = UNSET
    map_view: MapView | Unset = UNSET
    categories: list[Category] | Unset = UNSET
    food_types: list[Category] | Unset = UNSET
    house_number_fallback: bool | Unset = UNSET
    estimated_point_address: bool | Unset = UNSET
    time_zone: TimeZoneInfo | Unset = UNSET
    street_info: list[StreetInfo] | Unset = UNSET
    country_info: CountryInfo | Unset = UNSET
    estimated_area_fallback: bool | Unset = UNSET
    map_references: MapReferenceSection | Unset = UNSET
    related: list[RelatedAddress] | Unset = UNSET
    navigation_attributes: NavigationAttributes | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.postal_code_details_usps_zip import PostalCodeDetailsUspsZip

        title = self.title

        id = self.id

        address = self.address.to_dict()

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

        postal_code_details: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.postal_code_details, Unset):
            postal_code_details = []
            for postal_code_details_item_data in self.postal_code_details:
                postal_code_details_item: dict[str, Any]
                if isinstance(postal_code_details_item_data, PostalCodeDetailsUspsZip):
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

        distance = self.distance

        map_view: dict[str, Any] | Unset = UNSET
        if not isinstance(self.map_view, Unset):
            map_view = self.map_view.to_dict()

        categories: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.to_dict()
                categories.append(categories_item)

        food_types: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.food_types, Unset):
            food_types = []
            for food_types_item_data in self.food_types:
                food_types_item = food_types_item_data.to_dict()
                food_types.append(food_types_item)

        house_number_fallback = self.house_number_fallback

        estimated_point_address = self.estimated_point_address

        time_zone: dict[str, Any] | Unset = UNSET
        if not isinstance(self.time_zone, Unset):
            time_zone = self.time_zone.to_dict()

        street_info: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.street_info, Unset):
            street_info = []
            for street_info_item_data in self.street_info:
                street_info_item = street_info_item_data.to_dict()
                street_info.append(street_info_item)

        country_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.country_info, Unset):
            country_info = self.country_info.to_dict()

        estimated_area_fallback = self.estimated_area_fallback

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "title": title,
            "id": id,
            "address": address,
        })
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
        if postal_code_details is not UNSET:
            field_dict["postalCodeDetails"] = postal_code_details
        if position is not UNSET:
            field_dict["position"] = position
        if access is not UNSET:
            field_dict["access"] = access
        if distance is not UNSET:
            field_dict["distance"] = distance
        if map_view is not UNSET:
            field_dict["mapView"] = map_view
        if categories is not UNSET:
            field_dict["categories"] = categories
        if food_types is not UNSET:
            field_dict["foodTypes"] = food_types
        if house_number_fallback is not UNSET:
            field_dict["houseNumberFallback"] = house_number_fallback
        if estimated_point_address is not UNSET:
            field_dict["estimatedPointAddress"] = estimated_point_address
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone
        if street_info is not UNSET:
            field_dict["streetInfo"] = street_info
        if country_info is not UNSET:
            field_dict["countryInfo"] = country_info
        if estimated_area_fallback is not UNSET:
            field_dict["estimatedAreaFallback"] = estimated_area_fallback
        if map_references is not UNSET:
            field_dict["mapReferences"] = map_references
        if related is not UNSET:
            field_dict["related"] = related
        if navigation_attributes is not UNSET:
            field_dict["navigationAttributes"] = navigation_attributes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_usage import AddressUsage
        from ..models.basic_access_point import BasicAccessPoint
        from ..models.category import Category
        from ..models.country_info import CountryInfo
        from ..models.display_response_coordinate import DisplayResponseCoordinate
        from ..models.map_reference_section import MapReferenceSection
        from ..models.map_view import MapView
        from ..models.navigation_attributes import NavigationAttributes
        from ..models.postal_code_details_usps_zip import PostalCodeDetailsUspsZip
        from ..models.postal_code_details_usps_zip_plus_4 import (
            PostalCodeDetailsUspsZipPlus4,
        )
        from ..models.related_address import RelatedAddress
        from ..models.rgc_address import RgcAddress
        from ..models.street_info import StreetInfo
        from ..models.time_zone_info import TimeZoneInfo

        d = dict(src_dict)
        title = d.pop("title")

        id = d.pop("id")

        address = RgcAddress.from_dict(d.pop("address"))

        political_view = d.pop("politicalView", UNSET)

        _result_type = d.pop("resultType", UNSET)
        result_type: ReverseGeocodeResultItemResultType | Unset
        if isinstance(_result_type, Unset):
            result_type = UNSET
        else:
            result_type = ReverseGeocodeResultItemResultType(_result_type)

        _house_number_type = d.pop("houseNumberType", UNSET)
        house_number_type: ReverseGeocodeResultItemHouseNumberType | Unset
        if isinstance(_house_number_type, Unset):
            house_number_type = UNSET
        else:
            house_number_type = ReverseGeocodeResultItemHouseNumberType(
                _house_number_type
            )

        _address_usage = d.pop("addressUsage", UNSET)
        address_usage: AddressUsage | Unset
        if isinstance(_address_usage, Unset):
            address_usage = UNSET
        else:
            address_usage = AddressUsage.from_dict(_address_usage)

        _address_block_type = d.pop("addressBlockType", UNSET)
        address_block_type: ReverseGeocodeResultItemAddressBlockType | Unset
        if isinstance(_address_block_type, Unset):
            address_block_type = UNSET
        else:
            address_block_type = ReverseGeocodeResultItemAddressBlockType(
                _address_block_type
            )

        _locality_type = d.pop("localityType", UNSET)
        locality_type: ReverseGeocodeResultItemLocalityType | Unset
        if isinstance(_locality_type, Unset):
            locality_type = UNSET
        else:
            locality_type = ReverseGeocodeResultItemLocalityType(_locality_type)

        _administrative_area_type = d.pop("administrativeAreaType", UNSET)
        administrative_area_type: ReverseGeocodeResultItemAdministrativeAreaType | Unset
        if isinstance(_administrative_area_type, Unset):
            administrative_area_type = UNSET
        else:
            administrative_area_type = ReverseGeocodeResultItemAdministrativeAreaType(
                _administrative_area_type
            )

        _postal_code_details = d.pop("postalCodeDetails", UNSET)
        postal_code_details: (
            list[PostalCodeDetailsUspsZip | PostalCodeDetailsUspsZipPlus4] | Unset
        ) = UNSET
        if _postal_code_details is not UNSET:
            postal_code_details = []
            for postal_code_details_item_data in _postal_code_details:

                def _parse_postal_code_details_item(
                    data: object,
                ) -> PostalCodeDetailsUspsZip | PostalCodeDetailsUspsZipPlus4:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        postal_code_details_item_type_0 = (
                            PostalCodeDetailsUspsZip.from_dict(data)
                        )

                        return postal_code_details_item_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    postal_code_details_item_type_1 = (
                        PostalCodeDetailsUspsZipPlus4.from_dict(data)
                    )

                    return postal_code_details_item_type_1

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
        access: list[BasicAccessPoint] | Unset = UNSET
        if _access is not UNSET:
            access = []
            for access_item_data in _access:
                access_item = BasicAccessPoint.from_dict(access_item_data)

                access.append(access_item)

        distance = d.pop("distance", UNSET)

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

        _food_types = d.pop("foodTypes", UNSET)
        food_types: list[Category] | Unset = UNSET
        if _food_types is not UNSET:
            food_types = []
            for food_types_item_data in _food_types:
                food_types_item = Category.from_dict(food_types_item_data)

                food_types.append(food_types_item)

        house_number_fallback = d.pop("houseNumberFallback", UNSET)

        estimated_point_address = d.pop("estimatedPointAddress", UNSET)

        _time_zone = d.pop("timeZone", UNSET)
        time_zone: TimeZoneInfo | Unset
        if isinstance(_time_zone, Unset):
            time_zone = UNSET
        else:
            time_zone = TimeZoneInfo.from_dict(_time_zone)

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

        estimated_area_fallback = d.pop("estimatedAreaFallback", UNSET)

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

        reverse_geocode_result_item = cls(
            title=title,
            id=id,
            address=address,
            political_view=political_view,
            result_type=result_type,
            house_number_type=house_number_type,
            address_usage=address_usage,
            address_block_type=address_block_type,
            locality_type=locality_type,
            administrative_area_type=administrative_area_type,
            postal_code_details=postal_code_details,
            position=position,
            access=access,
            distance=distance,
            map_view=map_view,
            categories=categories,
            food_types=food_types,
            house_number_fallback=house_number_fallback,
            estimated_point_address=estimated_point_address,
            time_zone=time_zone,
            street_info=street_info,
            country_info=country_info,
            estimated_area_fallback=estimated_area_fallback,
            map_references=map_references,
            related=related,
            navigation_attributes=navigation_attributes,
        )

        reverse_geocode_result_item.additional_properties = d
        return reverse_geocode_result_item

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
