from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RgcAddress")


@_attrs_define
class RgcAddress:
    """
    Attributes:
        label (str | Unset): Assembled address value built out of the address components according to the regional
            postal rules.
            These are the same rules for all endpoints. It may not include all the input terms. For example:
            "Schulstraße 4, 32547 Bad Oeynhausen, Germany"
        country_code (str | Unset): A three-letter country code. For example: "DEU"
        country_name (str | Unset): The localised country name. For example: "Deutschland"
        state_code (str | Unset): A state code or state name abbreviation – country specific. For example, in the United
            States it is the two letter state abbreviation: "CA" for California.
        state (str | Unset): The state division of a country. For example: "North Rhine-Westphalia"
        county_code (str | Unset): A county code or county name abbreviation – country specific. For example, for Italy
            it is the province abbreviation: "RM" for Rome.
        county (str | Unset): A division of a state; typically, a secondary-level administrative division of a country
            or equivalent.
        city (str | Unset): The name of the primary locality of the place. For example: "Bad Oyenhausen"
        district (str | Unset): A division of city; typically an administrative unit within a larger city or a customary
            name of a city's neighborhood. For example: "Bad Oyenhausen"
        subdistrict (str | Unset): A subdivision of a district. For example: "Minden-Lübbecke"
        street (str | Unset): Name of street. For example: "Schulstrasse"
        block (str | Unset): Name of block.
        subblock (str | Unset): Name of sub-block.
        postal_code (str | Unset): An alphanumeric string included in a postal address to facilitate mail sorting, such
            as post code, postcode, or ZIP code. For example: "32547"
        house_number (str | Unset): House number. For example: "4"
        building (str | Unset): Name of building.
        unit (str | Unset): Secondary unit information. It may include building, floor (level), and suite (unit)
            details. This field is returned by Geocode, (Multi) Reverse Geocode and Lookup endpoints only.
    """

    label: str | Unset = UNSET
    country_code: str | Unset = UNSET
    country_name: str | Unset = UNSET
    state_code: str | Unset = UNSET
    state: str | Unset = UNSET
    county_code: str | Unset = UNSET
    county: str | Unset = UNSET
    city: str | Unset = UNSET
    district: str | Unset = UNSET
    subdistrict: str | Unset = UNSET
    street: str | Unset = UNSET
    block: str | Unset = UNSET
    subblock: str | Unset = UNSET
    postal_code: str | Unset = UNSET
    house_number: str | Unset = UNSET
    building: str | Unset = UNSET
    unit: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        country_code = self.country_code

        country_name = self.country_name

        state_code = self.state_code

        state = self.state

        county_code = self.county_code

        county = self.county

        city = self.city

        district = self.district

        subdistrict = self.subdistrict

        street = self.street

        block = self.block

        subblock = self.subblock

        postal_code = self.postal_code

        house_number = self.house_number

        building = self.building

        unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code
        if country_name is not UNSET:
            field_dict["countryName"] = country_name
        if state_code is not UNSET:
            field_dict["stateCode"] = state_code
        if state is not UNSET:
            field_dict["state"] = state
        if county_code is not UNSET:
            field_dict["countyCode"] = county_code
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
        if postal_code is not UNSET:
            field_dict["postalCode"] = postal_code
        if house_number is not UNSET:
            field_dict["houseNumber"] = house_number
        if building is not UNSET:
            field_dict["building"] = building
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label", UNSET)

        country_code = d.pop("countryCode", UNSET)

        country_name = d.pop("countryName", UNSET)

        state_code = d.pop("stateCode", UNSET)

        state = d.pop("state", UNSET)

        county_code = d.pop("countyCode", UNSET)

        county = d.pop("county", UNSET)

        city = d.pop("city", UNSET)

        district = d.pop("district", UNSET)

        subdistrict = d.pop("subdistrict", UNSET)

        street = d.pop("street", UNSET)

        block = d.pop("block", UNSET)

        subblock = d.pop("subblock", UNSET)

        postal_code = d.pop("postalCode", UNSET)

        house_number = d.pop("houseNumber", UNSET)

        building = d.pop("building", UNSET)

        unit = d.pop("unit", UNSET)

        rgc_address = cls(
            label=label,
            country_code=country_code,
            country_name=country_name,
            state_code=state_code,
            state=state,
            county_code=county_code,
            county=county,
            city=city,
            district=district,
            subdistrict=subdistrict,
            street=street,
            block=block,
            subblock=subblock,
            postal_code=postal_code,
            house_number=house_number,
            building=building,
            unit=unit,
        )

        rgc_address.additional_properties = d
        return rgc_address

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
