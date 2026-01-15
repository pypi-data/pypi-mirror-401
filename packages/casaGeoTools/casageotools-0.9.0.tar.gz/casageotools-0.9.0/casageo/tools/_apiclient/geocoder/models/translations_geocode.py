from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.admin_names import AdminNames


T = TypeVar("T", bound="TranslationsGeocode")


@_attrs_define
class TranslationsGeocode:
    """
    Attributes:
        state_names (list[AdminNames] | Unset): The list of all state names and translations applicable to an address
            field, grouped by alternative views on it. For example, if subdivision of a country from administrative and
            postal views is different, some administrative levels may have two groups of names: from administrative and from
            postal views.
        county_names (list[AdminNames] | Unset): The list of all county names and translations applicable to an address
            field, grouped by alternative views on it. For example, if subdivision of a country from administrative and
            postal views is different, some administrative levels may have two groups of names: from administrative and from
            postal views.
        city_names (list[AdminNames] | Unset): The list of all city names and translations applicable to an address
            field, grouped by alternative views on it. For example, if subdivision of a country from administrative and
            postal views is different, some administrative levels may have two groups of names: from administrative and from
            postal views.
        district_names (list[AdminNames] | Unset): The list of all district names and translations applicable to an
            address field, grouped by alternative views on it. For example, if subdivision of a country from administrative
            and postal views is different, some administrative levels may have two groups of names: from administrative and
            from postal views.
    """

    state_names: list[AdminNames] | Unset = UNSET
    county_names: list[AdminNames] | Unset = UNSET
    city_names: list[AdminNames] | Unset = UNSET
    district_names: list[AdminNames] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state_names: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.state_names, Unset):
            state_names = []
            for state_names_item_data in self.state_names:
                state_names_item = state_names_item_data.to_dict()
                state_names.append(state_names_item)

        county_names: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.county_names, Unset):
            county_names = []
            for county_names_item_data in self.county_names:
                county_names_item = county_names_item_data.to_dict()
                county_names.append(county_names_item)

        city_names: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.city_names, Unset):
            city_names = []
            for city_names_item_data in self.city_names:
                city_names_item = city_names_item_data.to_dict()
                city_names.append(city_names_item)

        district_names: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.district_names, Unset):
            district_names = []
            for district_names_item_data in self.district_names:
                district_names_item = district_names_item_data.to_dict()
                district_names.append(district_names_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if state_names is not UNSET:
            field_dict["stateNames"] = state_names
        if county_names is not UNSET:
            field_dict["countyNames"] = county_names
        if city_names is not UNSET:
            field_dict["cityNames"] = city_names
        if district_names is not UNSET:
            field_dict["districtNames"] = district_names

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.admin_names import AdminNames

        d = dict(src_dict)
        _state_names = d.pop("stateNames", UNSET)
        state_names: list[AdminNames] | Unset = UNSET
        if _state_names is not UNSET:
            state_names = []
            for state_names_item_data in _state_names:
                state_names_item = AdminNames.from_dict(state_names_item_data)

                state_names.append(state_names_item)

        _county_names = d.pop("countyNames", UNSET)
        county_names: list[AdminNames] | Unset = UNSET
        if _county_names is not UNSET:
            county_names = []
            for county_names_item_data in _county_names:
                county_names_item = AdminNames.from_dict(county_names_item_data)

                county_names.append(county_names_item)

        _city_names = d.pop("cityNames", UNSET)
        city_names: list[AdminNames] | Unset = UNSET
        if _city_names is not UNSET:
            city_names = []
            for city_names_item_data in _city_names:
                city_names_item = AdminNames.from_dict(city_names_item_data)

                city_names.append(city_names_item)

        _district_names = d.pop("districtNames", UNSET)
        district_names: list[AdminNames] | Unset = UNSET
        if _district_names is not UNSET:
            district_names = []
            for district_names_item_data in _district_names:
                district_names_item = AdminNames.from_dict(district_names_item_data)

                district_names.append(district_names_item)

        translations_geocode = cls(
            state_names=state_names,
            county_names=county_names,
            city_names=city_names,
            district_names=district_names,
        )

        translations_geocode.additional_properties = d
        return translations_geocode

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
