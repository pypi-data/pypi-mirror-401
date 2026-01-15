from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.range_ import Range


T = TypeVar("T", bound="AddressHighlightingInformation")


@_attrs_define
class AddressHighlightingInformation:
    """
    Attributes:
        label (list[Range] | Unset): Indicates matched substrings in the address label.
        country (list[Range] | Unset): Indicates matched substrings in the Country field.
        country_code (list[Range] | Unset): Indicates matched substrings in the Country Code field.
        state (list[Range] | Unset): Indicates matched substrings in the State field.
        state_code (list[Range] | Unset): Indicates matched substrings in the State Code field.
        county (list[Range] | Unset): Indicates matched substrings in the County field.
        county_code (list[Range] | Unset): Indicates matched substrings in the County Code field.
        city (list[Range] | Unset): Indicates matched substrings in the City field.
        district (list[Range] | Unset): Indicates matched substrings in the District field.
        subdistrict (list[Range] | Unset): Indicates matched substrings in the Sub-District field.
        block (list[Range] | Unset): Indicates matched substrings in the Block field.
        subblock (list[Range] | Unset): Indicates matched substrings in the Sub-Block field.
        street (list[Range] | Unset): Indicates matched substrings in the Street field.
        streets (list[list[Range]] | Unset): Indicates matched substrings in the Streets field.
        postal_code (list[Range] | Unset): Indicates matched substrings in the Postal Code field.
        house_number (list[Range] | Unset): Indicates matched substrings in the House Number field.
        building (list[Range] | Unset): Indicates matched substrings in the Building field.
    """

    label: list[Range] | Unset = UNSET
    country: list[Range] | Unset = UNSET
    country_code: list[Range] | Unset = UNSET
    state: list[Range] | Unset = UNSET
    state_code: list[Range] | Unset = UNSET
    county: list[Range] | Unset = UNSET
    county_code: list[Range] | Unset = UNSET
    city: list[Range] | Unset = UNSET
    district: list[Range] | Unset = UNSET
    subdistrict: list[Range] | Unset = UNSET
    block: list[Range] | Unset = UNSET
    subblock: list[Range] | Unset = UNSET
    street: list[Range] | Unset = UNSET
    streets: list[list[Range]] | Unset = UNSET
    postal_code: list[Range] | Unset = UNSET
    house_number: list[Range] | Unset = UNSET
    building: list[Range] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.label, Unset):
            label = []
            for label_item_data in self.label:
                label_item = label_item_data.to_dict()
                label.append(label_item)

        country: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.country, Unset):
            country = []
            for country_item_data in self.country:
                country_item = country_item_data.to_dict()
                country.append(country_item)

        country_code: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.country_code, Unset):
            country_code = []
            for country_code_item_data in self.country_code:
                country_code_item = country_code_item_data.to_dict()
                country_code.append(country_code_item)

        state: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.state, Unset):
            state = []
            for state_item_data in self.state:
                state_item = state_item_data.to_dict()
                state.append(state_item)

        state_code: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.state_code, Unset):
            state_code = []
            for state_code_item_data in self.state_code:
                state_code_item = state_code_item_data.to_dict()
                state_code.append(state_code_item)

        county: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.county, Unset):
            county = []
            for county_item_data in self.county:
                county_item = county_item_data.to_dict()
                county.append(county_item)

        county_code: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.county_code, Unset):
            county_code = []
            for county_code_item_data in self.county_code:
                county_code_item = county_code_item_data.to_dict()
                county_code.append(county_code_item)

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

        street: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.street, Unset):
            street = []
            for street_item_data in self.street:
                street_item = street_item_data.to_dict()
                street.append(street_item)

        streets: list[list[dict[str, Any]]] | Unset = UNSET
        if not isinstance(self.streets, Unset):
            streets = []
            for streets_item_data in self.streets:
                streets_item = []
                for streets_item_item_data in streets_item_data:
                    streets_item_item = streets_item_item_data.to_dict()
                    streets_item.append(streets_item_item)

                streets.append(streets_item)

        postal_code: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.postal_code, Unset):
            postal_code = []
            for postal_code_item_data in self.postal_code:
                postal_code_item = postal_code_item_data.to_dict()
                postal_code.append(postal_code_item)

        house_number: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.house_number, Unset):
            house_number = []
            for house_number_item_data in self.house_number:
                house_number_item = house_number_item_data.to_dict()
                house_number.append(house_number_item)

        building: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.building, Unset):
            building = []
            for building_item_data in self.building:
                building_item = building_item_data.to_dict()
                building.append(building_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if country is not UNSET:
            field_dict["country"] = country
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code
        if state is not UNSET:
            field_dict["state"] = state
        if state_code is not UNSET:
            field_dict["stateCode"] = state_code
        if county is not UNSET:
            field_dict["county"] = county
        if county_code is not UNSET:
            field_dict["countyCode"] = county_code
        if city is not UNSET:
            field_dict["city"] = city
        if district is not UNSET:
            field_dict["district"] = district
        if subdistrict is not UNSET:
            field_dict["subdistrict"] = subdistrict
        if block is not UNSET:
            field_dict["block"] = block
        if subblock is not UNSET:
            field_dict["subblock"] = subblock
        if street is not UNSET:
            field_dict["street"] = street
        if streets is not UNSET:
            field_dict["streets"] = streets
        if postal_code is not UNSET:
            field_dict["postalCode"] = postal_code
        if house_number is not UNSET:
            field_dict["houseNumber"] = house_number
        if building is not UNSET:
            field_dict["building"] = building

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.range_ import Range

        d = dict(src_dict)
        _label = d.pop("label", UNSET)
        label: list[Range] | Unset = UNSET
        if _label is not UNSET:
            label = []
            for label_item_data in _label:
                label_item = Range.from_dict(label_item_data)

                label.append(label_item)

        _country = d.pop("country", UNSET)
        country: list[Range] | Unset = UNSET
        if _country is not UNSET:
            country = []
            for country_item_data in _country:
                country_item = Range.from_dict(country_item_data)

                country.append(country_item)

        _country_code = d.pop("countryCode", UNSET)
        country_code: list[Range] | Unset = UNSET
        if _country_code is not UNSET:
            country_code = []
            for country_code_item_data in _country_code:
                country_code_item = Range.from_dict(country_code_item_data)

                country_code.append(country_code_item)

        _state = d.pop("state", UNSET)
        state: list[Range] | Unset = UNSET
        if _state is not UNSET:
            state = []
            for state_item_data in _state:
                state_item = Range.from_dict(state_item_data)

                state.append(state_item)

        _state_code = d.pop("stateCode", UNSET)
        state_code: list[Range] | Unset = UNSET
        if _state_code is not UNSET:
            state_code = []
            for state_code_item_data in _state_code:
                state_code_item = Range.from_dict(state_code_item_data)

                state_code.append(state_code_item)

        _county = d.pop("county", UNSET)
        county: list[Range] | Unset = UNSET
        if _county is not UNSET:
            county = []
            for county_item_data in _county:
                county_item = Range.from_dict(county_item_data)

                county.append(county_item)

        _county_code = d.pop("countyCode", UNSET)
        county_code: list[Range] | Unset = UNSET
        if _county_code is not UNSET:
            county_code = []
            for county_code_item_data in _county_code:
                county_code_item = Range.from_dict(county_code_item_data)

                county_code.append(county_code_item)

        _city = d.pop("city", UNSET)
        city: list[Range] | Unset = UNSET
        if _city is not UNSET:
            city = []
            for city_item_data in _city:
                city_item = Range.from_dict(city_item_data)

                city.append(city_item)

        _district = d.pop("district", UNSET)
        district: list[Range] | Unset = UNSET
        if _district is not UNSET:
            district = []
            for district_item_data in _district:
                district_item = Range.from_dict(district_item_data)

                district.append(district_item)

        _subdistrict = d.pop("subdistrict", UNSET)
        subdistrict: list[Range] | Unset = UNSET
        if _subdistrict is not UNSET:
            subdistrict = []
            for subdistrict_item_data in _subdistrict:
                subdistrict_item = Range.from_dict(subdistrict_item_data)

                subdistrict.append(subdistrict_item)

        _block = d.pop("block", UNSET)
        block: list[Range] | Unset = UNSET
        if _block is not UNSET:
            block = []
            for block_item_data in _block:
                block_item = Range.from_dict(block_item_data)

                block.append(block_item)

        _subblock = d.pop("subblock", UNSET)
        subblock: list[Range] | Unset = UNSET
        if _subblock is not UNSET:
            subblock = []
            for subblock_item_data in _subblock:
                subblock_item = Range.from_dict(subblock_item_data)

                subblock.append(subblock_item)

        _street = d.pop("street", UNSET)
        street: list[Range] | Unset = UNSET
        if _street is not UNSET:
            street = []
            for street_item_data in _street:
                street_item = Range.from_dict(street_item_data)

                street.append(street_item)

        _streets = d.pop("streets", UNSET)
        streets: list[list[Range]] | Unset = UNSET
        if _streets is not UNSET:
            streets = []
            for streets_item_data in _streets:
                streets_item = []
                _streets_item = streets_item_data
                for streets_item_item_data in _streets_item:
                    streets_item_item = Range.from_dict(streets_item_item_data)

                    streets_item.append(streets_item_item)

                streets.append(streets_item)

        _postal_code = d.pop("postalCode", UNSET)
        postal_code: list[Range] | Unset = UNSET
        if _postal_code is not UNSET:
            postal_code = []
            for postal_code_item_data in _postal_code:
                postal_code_item = Range.from_dict(postal_code_item_data)

                postal_code.append(postal_code_item)

        _house_number = d.pop("houseNumber", UNSET)
        house_number: list[Range] | Unset = UNSET
        if _house_number is not UNSET:
            house_number = []
            for house_number_item_data in _house_number:
                house_number_item = Range.from_dict(house_number_item_data)

                house_number.append(house_number_item)

        _building = d.pop("building", UNSET)
        building: list[Range] | Unset = UNSET
        if _building is not UNSET:
            building = []
            for building_item_data in _building:
                building_item = Range.from_dict(building_item_data)

                building.append(building_item)

        address_highlighting_information = cls(
            label=label,
            country=country,
            country_code=country_code,
            state=state,
            state_code=state_code,
            county=county,
            county_code=county_code,
            city=city,
            district=district,
            subdistrict=subdistrict,
            block=block,
            subblock=subblock,
            street=street,
            streets=streets,
            postal_code=postal_code,
            house_number=house_number,
            building=building,
        )

        address_highlighting_information.additional_properties = d
        return address_highlighting_information

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
