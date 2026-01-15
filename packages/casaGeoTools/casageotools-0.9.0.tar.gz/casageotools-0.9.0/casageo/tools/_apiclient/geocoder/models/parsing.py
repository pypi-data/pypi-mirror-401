from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.match_info import MatchInfo


T = TypeVar("T", bound="Parsing")


@_attrs_define
class Parsing:
    """
    Attributes:
        place_name (list[MatchInfo] | Unset): Place name matches
        country (list[MatchInfo] | Unset): Country matches
        state (list[MatchInfo] | Unset): State matches
        county (list[MatchInfo] | Unset): County matches
        city (list[MatchInfo] | Unset): City matches
        district (list[MatchInfo] | Unset): District matches
        subdistrict (list[MatchInfo] | Unset): Subdistrict matches
        street (list[MatchInfo] | Unset): Street matches
        block (list[MatchInfo] | Unset): Block matches
        subblock (list[MatchInfo] | Unset): Subblock matches
        house_number (list[MatchInfo] | Unset): HouseNumber matches
        postal_code (list[MatchInfo] | Unset): PostalCode matches
        building (list[MatchInfo] | Unset): Building matches
        secondary_units (list[MatchInfo] | Unset): secondaryUnits matches
        additional_info (list[MatchInfo] | Unset): Additional information extracted from the query that do not
            correspond to any recognized address components in the map data.
    """

    place_name: list[MatchInfo] | Unset = UNSET
    country: list[MatchInfo] | Unset = UNSET
    state: list[MatchInfo] | Unset = UNSET
    county: list[MatchInfo] | Unset = UNSET
    city: list[MatchInfo] | Unset = UNSET
    district: list[MatchInfo] | Unset = UNSET
    subdistrict: list[MatchInfo] | Unset = UNSET
    street: list[MatchInfo] | Unset = UNSET
    block: list[MatchInfo] | Unset = UNSET
    subblock: list[MatchInfo] | Unset = UNSET
    house_number: list[MatchInfo] | Unset = UNSET
    postal_code: list[MatchInfo] | Unset = UNSET
    building: list[MatchInfo] | Unset = UNSET
    secondary_units: list[MatchInfo] | Unset = UNSET
    additional_info: list[MatchInfo] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        place_name: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.place_name, Unset):
            place_name = []
            for place_name_item_data in self.place_name:
                place_name_item = place_name_item_data.to_dict()
                place_name.append(place_name_item)

        country: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.country, Unset):
            country = []
            for country_item_data in self.country:
                country_item = country_item_data.to_dict()
                country.append(country_item)

        state: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.state, Unset):
            state = []
            for state_item_data in self.state:
                state_item = state_item_data.to_dict()
                state.append(state_item)

        county: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.county, Unset):
            county = []
            for county_item_data in self.county:
                county_item = county_item_data.to_dict()
                county.append(county_item)

        city: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.city, Unset):
            city = []
            for city_item_data in self.city:
                city_item = city_item_data.to_dict()
                city.append(city_item)

        district: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.district, Unset):
            district = []
            for district_item_data in self.district:
                district_item = district_item_data.to_dict()
                district.append(district_item)

        subdistrict: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.subdistrict, Unset):
            subdistrict = []
            for subdistrict_item_data in self.subdistrict:
                subdistrict_item = subdistrict_item_data.to_dict()
                subdistrict.append(subdistrict_item)

        street: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.street, Unset):
            street = []
            for street_item_data in self.street:
                street_item = street_item_data.to_dict()
                street.append(street_item)

        block: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.block, Unset):
            block = []
            for block_item_data in self.block:
                block_item = block_item_data.to_dict()
                block.append(block_item)

        subblock: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.subblock, Unset):
            subblock = []
            for subblock_item_data in self.subblock:
                subblock_item = subblock_item_data.to_dict()
                subblock.append(subblock_item)

        house_number: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.house_number, Unset):
            house_number = []
            for house_number_item_data in self.house_number:
                house_number_item = house_number_item_data.to_dict()
                house_number.append(house_number_item)

        postal_code: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.postal_code, Unset):
            postal_code = []
            for postal_code_item_data in self.postal_code:
                postal_code_item = postal_code_item_data.to_dict()
                postal_code.append(postal_code_item)

        building: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.building, Unset):
            building = []
            for building_item_data in self.building:
                building_item = building_item_data.to_dict()
                building.append(building_item)

        secondary_units: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.secondary_units, Unset):
            secondary_units = []
            for secondary_units_item_data in self.secondary_units:
                secondary_units_item = secondary_units_item_data.to_dict()
                secondary_units.append(secondary_units_item)

        additional_info: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.additional_info, Unset):
            additional_info = []
            for additional_info_item_data in self.additional_info:
                additional_info_item = additional_info_item_data.to_dict()
                additional_info.append(additional_info_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if place_name is not UNSET:
            field_dict["placeName"] = place_name
        if country is not UNSET:
            field_dict["country"] = country
        if state is not UNSET:
            field_dict["state"] = state
        if county is not UNSET:
            field_dict["county"] = county
        if city is not UNSET:
            field_dict["city"] = city
        if district is not UNSET:
            field_dict["district"] = district
        if subdistrict is not UNSET:
            field_dict["subdistrict"] = subdistrict
        if street is not UNSET:
            field_dict["street"] = street
        if block is not UNSET:
            field_dict["block"] = block
        if subblock is not UNSET:
            field_dict["subblock"] = subblock
        if house_number is not UNSET:
            field_dict["houseNumber"] = house_number
        if postal_code is not UNSET:
            field_dict["postalCode"] = postal_code
        if building is not UNSET:
            field_dict["building"] = building
        if secondary_units is not UNSET:
            field_dict["secondaryUnits"] = secondary_units
        if additional_info is not UNSET:
            field_dict["additionalInfo"] = additional_info

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.match_info import MatchInfo

        d = dict(src_dict)
        _place_name = d.pop("placeName", UNSET)
        place_name: list[MatchInfo] | Unset = UNSET
        if _place_name is not UNSET:
            place_name = []
            for place_name_item_data in _place_name:
                place_name_item = MatchInfo.from_dict(place_name_item_data)

                place_name.append(place_name_item)

        _country = d.pop("country", UNSET)
        country: list[MatchInfo] | Unset = UNSET
        if _country is not UNSET:
            country = []
            for country_item_data in _country:
                country_item = MatchInfo.from_dict(country_item_data)

                country.append(country_item)

        _state = d.pop("state", UNSET)
        state: list[MatchInfo] | Unset = UNSET
        if _state is not UNSET:
            state = []
            for state_item_data in _state:
                state_item = MatchInfo.from_dict(state_item_data)

                state.append(state_item)

        _county = d.pop("county", UNSET)
        county: list[MatchInfo] | Unset = UNSET
        if _county is not UNSET:
            county = []
            for county_item_data in _county:
                county_item = MatchInfo.from_dict(county_item_data)

                county.append(county_item)

        _city = d.pop("city", UNSET)
        city: list[MatchInfo] | Unset = UNSET
        if _city is not UNSET:
            city = []
            for city_item_data in _city:
                city_item = MatchInfo.from_dict(city_item_data)

                city.append(city_item)

        _district = d.pop("district", UNSET)
        district: list[MatchInfo] | Unset = UNSET
        if _district is not UNSET:
            district = []
            for district_item_data in _district:
                district_item = MatchInfo.from_dict(district_item_data)

                district.append(district_item)

        _subdistrict = d.pop("subdistrict", UNSET)
        subdistrict: list[MatchInfo] | Unset = UNSET
        if _subdistrict is not UNSET:
            subdistrict = []
            for subdistrict_item_data in _subdistrict:
                subdistrict_item = MatchInfo.from_dict(subdistrict_item_data)

                subdistrict.append(subdistrict_item)

        _street = d.pop("street", UNSET)
        street: list[MatchInfo] | Unset = UNSET
        if _street is not UNSET:
            street = []
            for street_item_data in _street:
                street_item = MatchInfo.from_dict(street_item_data)

                street.append(street_item)

        _block = d.pop("block", UNSET)
        block: list[MatchInfo] | Unset = UNSET
        if _block is not UNSET:
            block = []
            for block_item_data in _block:
                block_item = MatchInfo.from_dict(block_item_data)

                block.append(block_item)

        _subblock = d.pop("subblock", UNSET)
        subblock: list[MatchInfo] | Unset = UNSET
        if _subblock is not UNSET:
            subblock = []
            for subblock_item_data in _subblock:
                subblock_item = MatchInfo.from_dict(subblock_item_data)

                subblock.append(subblock_item)

        _house_number = d.pop("houseNumber", UNSET)
        house_number: list[MatchInfo] | Unset = UNSET
        if _house_number is not UNSET:
            house_number = []
            for house_number_item_data in _house_number:
                house_number_item = MatchInfo.from_dict(house_number_item_data)

                house_number.append(house_number_item)

        _postal_code = d.pop("postalCode", UNSET)
        postal_code: list[MatchInfo] | Unset = UNSET
        if _postal_code is not UNSET:
            postal_code = []
            for postal_code_item_data in _postal_code:
                postal_code_item = MatchInfo.from_dict(postal_code_item_data)

                postal_code.append(postal_code_item)

        _building = d.pop("building", UNSET)
        building: list[MatchInfo] | Unset = UNSET
        if _building is not UNSET:
            building = []
            for building_item_data in _building:
                building_item = MatchInfo.from_dict(building_item_data)

                building.append(building_item)

        _secondary_units = d.pop("secondaryUnits", UNSET)
        secondary_units: list[MatchInfo] | Unset = UNSET
        if _secondary_units is not UNSET:
            secondary_units = []
            for secondary_units_item_data in _secondary_units:
                secondary_units_item = MatchInfo.from_dict(secondary_units_item_data)

                secondary_units.append(secondary_units_item)

        _additional_info = d.pop("additionalInfo", UNSET)
        additional_info: list[MatchInfo] | Unset = UNSET
        if _additional_info is not UNSET:
            additional_info = []
            for additional_info_item_data in _additional_info:
                additional_info_item = MatchInfo.from_dict(additional_info_item_data)

                additional_info.append(additional_info_item)

        parsing = cls(
            place_name=place_name,
            country=country,
            state=state,
            county=county,
            city=city,
            district=district,
            subdistrict=subdistrict,
            street=street,
            block=block,
            subblock=subblock,
            house_number=house_number,
            postal_code=postal_code,
            building=building,
            secondary_units=secondary_units,
            additional_info=additional_info,
        )

        parsing.additional_properties = d
        return parsing

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
