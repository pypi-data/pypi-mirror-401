from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.phoneme import Phoneme


T = TypeVar("T", bound="PhonemesSection")


@_attrs_define
class PhonemesSection:
    """
    Attributes:
        place_name (list[Phoneme] | Unset): Phonemes for the name of the place.
        country_name (list[Phoneme] | Unset): Phonemes for the county name.
        state (list[Phoneme] | Unset): Phonemes for the state name.
        county (list[Phoneme] | Unset): Phonemes for the county name.
        city (list[Phoneme] | Unset): Phonemes for the city name.
        district (list[Phoneme] | Unset): Phonemes for the district name.
        subdistrict (list[Phoneme] | Unset): Phonemes for the subdistrict name.
        street (list[Phoneme] | Unset): Phonemes for the street name.
        block (list[Phoneme] | Unset): Phonemes for the block.
        subblock (list[Phoneme] | Unset): Phonemes for the sub-block.
    """

    place_name: list[Phoneme] | Unset = UNSET
    country_name: list[Phoneme] | Unset = UNSET
    state: list[Phoneme] | Unset = UNSET
    county: list[Phoneme] | Unset = UNSET
    city: list[Phoneme] | Unset = UNSET
    district: list[Phoneme] | Unset = UNSET
    subdistrict: list[Phoneme] | Unset = UNSET
    street: list[Phoneme] | Unset = UNSET
    block: list[Phoneme] | Unset = UNSET
    subblock: list[Phoneme] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        place_name: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.place_name, Unset):
            place_name = []
            for place_name_item_data in self.place_name:
                place_name_item = place_name_item_data.to_dict()
                place_name.append(place_name_item)

        country_name: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.country_name, Unset):
            country_name = []
            for country_name_item_data in self.country_name:
                country_name_item = country_name_item_data.to_dict()
                country_name.append(country_name_item)

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if place_name is not UNSET:
            field_dict["placeName"] = place_name
        if country_name is not UNSET:
            field_dict["countryName"] = country_name
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.phoneme import Phoneme

        d = dict(src_dict)
        _place_name = d.pop("placeName", UNSET)
        place_name: list[Phoneme] | Unset = UNSET
        if _place_name is not UNSET:
            place_name = []
            for place_name_item_data in _place_name:
                place_name_item = Phoneme.from_dict(place_name_item_data)

                place_name.append(place_name_item)

        _country_name = d.pop("countryName", UNSET)
        country_name: list[Phoneme] | Unset = UNSET
        if _country_name is not UNSET:
            country_name = []
            for country_name_item_data in _country_name:
                country_name_item = Phoneme.from_dict(country_name_item_data)

                country_name.append(country_name_item)

        _state = d.pop("state", UNSET)
        state: list[Phoneme] | Unset = UNSET
        if _state is not UNSET:
            state = []
            for state_item_data in _state:
                state_item = Phoneme.from_dict(state_item_data)

                state.append(state_item)

        _county = d.pop("county", UNSET)
        county: list[Phoneme] | Unset = UNSET
        if _county is not UNSET:
            county = []
            for county_item_data in _county:
                county_item = Phoneme.from_dict(county_item_data)

                county.append(county_item)

        _city = d.pop("city", UNSET)
        city: list[Phoneme] | Unset = UNSET
        if _city is not UNSET:
            city = []
            for city_item_data in _city:
                city_item = Phoneme.from_dict(city_item_data)

                city.append(city_item)

        _district = d.pop("district", UNSET)
        district: list[Phoneme] | Unset = UNSET
        if _district is not UNSET:
            district = []
            for district_item_data in _district:
                district_item = Phoneme.from_dict(district_item_data)

                district.append(district_item)

        _subdistrict = d.pop("subdistrict", UNSET)
        subdistrict: list[Phoneme] | Unset = UNSET
        if _subdistrict is not UNSET:
            subdistrict = []
            for subdistrict_item_data in _subdistrict:
                subdistrict_item = Phoneme.from_dict(subdistrict_item_data)

                subdistrict.append(subdistrict_item)

        _street = d.pop("street", UNSET)
        street: list[Phoneme] | Unset = UNSET
        if _street is not UNSET:
            street = []
            for street_item_data in _street:
                street_item = Phoneme.from_dict(street_item_data)

                street.append(street_item)

        _block = d.pop("block", UNSET)
        block: list[Phoneme] | Unset = UNSET
        if _block is not UNSET:
            block = []
            for block_item_data in _block:
                block_item = Phoneme.from_dict(block_item_data)

                block.append(block_item)

        _subblock = d.pop("subblock", UNSET)
        subblock: list[Phoneme] | Unset = UNSET
        if _subblock is not UNSET:
            subblock = []
            for subblock_item_data in _subblock:
                subblock_item = Phoneme.from_dict(subblock_item_data)

                subblock.append(subblock_item)

        phonemes_section = cls(
            place_name=place_name,
            country_name=country_name,
            state=state,
            county=county,
            city=city,
            district=district,
            subdistrict=subdistrict,
            street=street,
            block=block,
            subblock=subblock,
        )

        phonemes_section.additional_properties = d
        return phonemes_section

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
