from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldScore")


@_attrs_define
class FieldScore:
    """
    Attributes:
        country (float | Unset): Indicates how good the result country name or [ISO 3166-1 alpha-3] country code matches
            to the freeform or qualified input.
        country_code (float | Unset): Indicates how good the result [ISO 3166-1 alpha-3] country code matches to the
            freeform or qualified input.
        state (float | Unset): Indicates how good the result state name matches to the freeform or qualified input.
        state_code (float | Unset): Indicates how good the result state code matches to the freeform or qualified input.
        county (float | Unset): Indicates how good the result county name matches to the freeform or qualified input.
        county_code (float | Unset): Indicates how good the result county code matches to the freeform or qualified
            input.
        city (float | Unset): Indicates how good the result city name matches to the freeform or qualified input.
        district (float | Unset): Indicates how good the result district name matches to the freeform or qualified
            input.
        subdistrict (float | Unset): Indicates how good the result sub-district name matches to the freeform or
            qualified input.
        streets (list[float] | Unset): Indicates how good the result street names match to the freeform or qualified
            input. If the input
            contains multiple street names, the field score is calculated and returned for each of them
            individually.
        block (float | Unset): Indicates how good the result block name matches to the freeform or qualified input.
        subblock (float | Unset): Indicates how good the result sub-block name matches to the freeform or qualified
            input.
        house_number (float | Unset): Indicates how good the result house number matches to the freeform or qualified
            input. It may
            happen, that the house number, which one is looking for, is not yet in the map data. For such cases,
            the Geocode endpoint returns the nearest known house number on the same street. This represents the
            numeric difference between the requested and the returned house numbers.
        postal_code (float | Unset): Indicates how good the result postal code matches to the freeform or qualified
            input.
        building (float | Unset): Indicates how good the result building name matches to the freeform or qualified
            input.
        unit (float | Unset): Indicates whether a secondary unit (such as building, floor or suite) has been recognized
            in the freeform or qualified input.
        place_name (float | Unset): Indicates how good the result place name matches to the freeform or qualified input.
        ontology_name (float | Unset): Indicates how good the result ontology name matches to the freeform or qualified
            input.
    """

    country: float | Unset = UNSET
    country_code: float | Unset = UNSET
    state: float | Unset = UNSET
    state_code: float | Unset = UNSET
    county: float | Unset = UNSET
    county_code: float | Unset = UNSET
    city: float | Unset = UNSET
    district: float | Unset = UNSET
    subdistrict: float | Unset = UNSET
    streets: list[float] | Unset = UNSET
    block: float | Unset = UNSET
    subblock: float | Unset = UNSET
    house_number: float | Unset = UNSET
    postal_code: float | Unset = UNSET
    building: float | Unset = UNSET
    unit: float | Unset = UNSET
    place_name: float | Unset = UNSET
    ontology_name: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        country = self.country

        country_code = self.country_code

        state = self.state

        state_code = self.state_code

        county = self.county

        county_code = self.county_code

        city = self.city

        district = self.district

        subdistrict = self.subdistrict

        streets: list[float] | Unset = UNSET
        if not isinstance(self.streets, Unset):
            streets = self.streets

        block = self.block

        subblock = self.subblock

        house_number = self.house_number

        postal_code = self.postal_code

        building = self.building

        unit = self.unit

        place_name = self.place_name

        ontology_name = self.ontology_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
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
        if streets is not UNSET:
            field_dict["streets"] = streets
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
        if unit is not UNSET:
            field_dict["unit"] = unit
        if place_name is not UNSET:
            field_dict["placeName"] = place_name
        if ontology_name is not UNSET:
            field_dict["ontologyName"] = ontology_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        country = d.pop("country", UNSET)

        country_code = d.pop("countryCode", UNSET)

        state = d.pop("state", UNSET)

        state_code = d.pop("stateCode", UNSET)

        county = d.pop("county", UNSET)

        county_code = d.pop("countyCode", UNSET)

        city = d.pop("city", UNSET)

        district = d.pop("district", UNSET)

        subdistrict = d.pop("subdistrict", UNSET)

        streets = cast(list[float], d.pop("streets", UNSET))

        block = d.pop("block", UNSET)

        subblock = d.pop("subblock", UNSET)

        house_number = d.pop("houseNumber", UNSET)

        postal_code = d.pop("postalCode", UNSET)

        building = d.pop("building", UNSET)

        unit = d.pop("unit", UNSET)

        place_name = d.pop("placeName", UNSET)

        ontology_name = d.pop("ontologyName", UNSET)

        field_score = cls(
            country=country,
            country_code=country_code,
            state=state,
            state_code=state_code,
            county=county,
            county_code=county_code,
            city=city,
            district=district,
            subdistrict=subdistrict,
            streets=streets,
            block=block,
            subblock=subblock,
            house_number=house_number,
            postal_code=postal_code,
            building=building,
            unit=unit,
            place_name=place_name,
            ontology_name=ontology_name,
        )

        field_score.additional_properties = d
        return field_score

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
