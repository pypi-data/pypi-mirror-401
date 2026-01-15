from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.autocomplete_result_item_administrative_area_type import (
    AutocompleteResultItemAdministrativeAreaType,
)
from ..models.autocomplete_result_item_house_number_type import (
    AutocompleteResultItemHouseNumberType,
)
from ..models.autocomplete_result_item_locality_type import (
    AutocompleteResultItemLocalityType,
)
from ..models.autocomplete_result_item_result_type import (
    AutocompleteResultItemResultType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.address import Address
    from ..models.street_info import StreetInfo
    from ..models.title_and_address_highlighting import TitleAndAddressHighlighting


T = TypeVar("T", bound="AutocompleteResultItem")


@_attrs_define
class AutocompleteResultItem:
    """
    Attributes:
        title (str): The unified display name of this result item. The result title is composed so that the customer
            application can use it to highlight parts of the suggestions. It is following a consistent schema
            for all results, regardless of their location. The highlighting details are about the
            title field and each of the address fields, from the country name down to the address house number.
            It is also built out from address components identified by the end-user, who can choose a result.
            For example: "Germany, 32547, Bad Oeynhausen, Schulstraße 4"
        id (str): The unique identifier for the result item. This ID can be used for a Look Up by ID search as well.
        address (Address):
        language (str | Unset): The preferred language of address elements in the result.
        political_view (str | Unset): ISO3 country code of the item political view (default for international). This
            response element is populated when the politicalView parameter is set in the query
        result_type (AutocompleteResultItemResultType | Unset):
            Type of the result item.

            Note: `addressBlock` result item is either a block or subblock.

            `resultType` values can get added to the list without further notice.
        house_number_type (AutocompleteResultItemHouseNumberType | Unset): Indicates the address type which affects the
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
        estimated_point_address (bool | Unset): If true, indicates that the coordinates of `position` and `access`
            points of the Point Address are
            estimated.
            This field is visible only for result items with resultType `houseNumber` and houseNumberType `PA` and
            only when the value is `true`
        locality_type (AutocompleteResultItemLocalityType | Unset):
            Type of the locality result if the `resultType` field is set to `locality`.

            `localityType` values can get added to the list without further notice.
        administrative_area_type (AutocompleteResultItemAdministrativeAreaType | Unset):
            Type of the administrative area result if the `resultType` field is set to `administrativeArea`.

            `administrativeAreaType` values can get added to the list without further notice.
        distance (int | Unset): The distance "as the crow flies" from the search center to this result item in meters.
            For example: "172039".

            When searching along a route this is the distance along the route plus the distance from the route polyline to
            this result item. Example: 172039.
        highlights (TitleAndAddressHighlighting | Unset):
        has_related_mpa (bool | Unset): **ALPHA, RESTRICTED**

            `true`: Indicates that sub-premises (referred to as Micro Point Addresses in HERE terminology) are associated
            with the house number.

            `false`: Indicates that no sub-premises (referred to as Micro Point Addresses in HERE terminology) are
            associated with the house number.

            This field is visible only for result items with resultType `houseNumber` and houseNumberType `PA`.

            The field is rendered only if `show=hasRelatedMPA` is provided.
        street_info (list[StreetInfo] | Unset): Street Details (only rendered if `show=streetInfo` is provided.)
    """

    title: str
    id: str
    address: Address
    language: str | Unset = UNSET
    political_view: str | Unset = UNSET
    result_type: AutocompleteResultItemResultType | Unset = UNSET
    house_number_type: AutocompleteResultItemHouseNumberType | Unset = UNSET
    estimated_point_address: bool | Unset = UNSET
    locality_type: AutocompleteResultItemLocalityType | Unset = UNSET
    administrative_area_type: AutocompleteResultItemAdministrativeAreaType | Unset = (
        UNSET
    )
    distance: int | Unset = UNSET
    highlights: TitleAndAddressHighlighting | Unset = UNSET
    has_related_mpa: bool | Unset = UNSET
    street_info: list[StreetInfo] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        id = self.id

        address = self.address.to_dict()

        language = self.language

        political_view = self.political_view

        result_type: str | Unset = UNSET
        if not isinstance(self.result_type, Unset):
            result_type = self.result_type.value

        house_number_type: str | Unset = UNSET
        if not isinstance(self.house_number_type, Unset):
            house_number_type = self.house_number_type.value

        estimated_point_address = self.estimated_point_address

        locality_type: str | Unset = UNSET
        if not isinstance(self.locality_type, Unset):
            locality_type = self.locality_type.value

        administrative_area_type: str | Unset = UNSET
        if not isinstance(self.administrative_area_type, Unset):
            administrative_area_type = self.administrative_area_type.value

        distance = self.distance

        highlights: dict[str, Any] | Unset = UNSET
        if not isinstance(self.highlights, Unset):
            highlights = self.highlights.to_dict()

        has_related_mpa = self.has_related_mpa

        street_info: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.street_info, Unset):
            street_info = []
            for street_info_item_data in self.street_info:
                street_info_item = street_info_item_data.to_dict()
                street_info.append(street_info_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "title": title,
            "id": id,
            "address": address,
        })
        if language is not UNSET:
            field_dict["language"] = language
        if political_view is not UNSET:
            field_dict["politicalView"] = political_view
        if result_type is not UNSET:
            field_dict["resultType"] = result_type
        if house_number_type is not UNSET:
            field_dict["houseNumberType"] = house_number_type
        if estimated_point_address is not UNSET:
            field_dict["estimatedPointAddress"] = estimated_point_address
        if locality_type is not UNSET:
            field_dict["localityType"] = locality_type
        if administrative_area_type is not UNSET:
            field_dict["administrativeAreaType"] = administrative_area_type
        if distance is not UNSET:
            field_dict["distance"] = distance
        if highlights is not UNSET:
            field_dict["highlights"] = highlights
        if has_related_mpa is not UNSET:
            field_dict["hasRelatedMPA"] = has_related_mpa
        if street_info is not UNSET:
            field_dict["streetInfo"] = street_info

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address import Address
        from ..models.street_info import StreetInfo
        from ..models.title_and_address_highlighting import TitleAndAddressHighlighting

        d = dict(src_dict)
        title = d.pop("title")

        id = d.pop("id")

        address = Address.from_dict(d.pop("address"))

        language = d.pop("language", UNSET)

        political_view = d.pop("politicalView", UNSET)

        _result_type = d.pop("resultType", UNSET)
        result_type: AutocompleteResultItemResultType | Unset
        if isinstance(_result_type, Unset):
            result_type = UNSET
        else:
            result_type = AutocompleteResultItemResultType(_result_type)

        _house_number_type = d.pop("houseNumberType", UNSET)
        house_number_type: AutocompleteResultItemHouseNumberType | Unset
        if isinstance(_house_number_type, Unset):
            house_number_type = UNSET
        else:
            house_number_type = AutocompleteResultItemHouseNumberType(
                _house_number_type
            )

        estimated_point_address = d.pop("estimatedPointAddress", UNSET)

        _locality_type = d.pop("localityType", UNSET)
        locality_type: AutocompleteResultItemLocalityType | Unset
        if isinstance(_locality_type, Unset):
            locality_type = UNSET
        else:
            locality_type = AutocompleteResultItemLocalityType(_locality_type)

        _administrative_area_type = d.pop("administrativeAreaType", UNSET)
        administrative_area_type: AutocompleteResultItemAdministrativeAreaType | Unset
        if isinstance(_administrative_area_type, Unset):
            administrative_area_type = UNSET
        else:
            administrative_area_type = AutocompleteResultItemAdministrativeAreaType(
                _administrative_area_type
            )

        distance = d.pop("distance", UNSET)

        _highlights = d.pop("highlights", UNSET)
        highlights: TitleAndAddressHighlighting | Unset
        if isinstance(_highlights, Unset):
            highlights = UNSET
        else:
            highlights = TitleAndAddressHighlighting.from_dict(_highlights)

        has_related_mpa = d.pop("hasRelatedMPA", UNSET)

        _street_info = d.pop("streetInfo", UNSET)
        street_info: list[StreetInfo] | Unset = UNSET
        if _street_info is not UNSET:
            street_info = []
            for street_info_item_data in _street_info:
                street_info_item = StreetInfo.from_dict(street_info_item_data)

                street_info.append(street_info_item)

        autocomplete_result_item = cls(
            title=title,
            id=id,
            address=address,
            language=language,
            political_view=political_view,
            result_type=result_type,
            house_number_type=house_number_type,
            estimated_point_address=estimated_point_address,
            locality_type=locality_type,
            administrative_area_type=administrative_area_type,
            distance=distance,
            highlights=highlights,
            has_related_mpa=has_related_mpa,
            street_info=street_info,
        )

        autocomplete_result_item.additional_properties = d
        return autocomplete_result_item

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
