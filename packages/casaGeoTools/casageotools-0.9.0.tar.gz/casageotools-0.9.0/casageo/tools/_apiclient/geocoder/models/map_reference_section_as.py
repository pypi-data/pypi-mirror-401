from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.admin_id_section import AdminIdSection
    from ..models.point_address_section import PointAddressSection
    from ..models.segment import Segment


T = TypeVar("T", bound="MapReferenceSectionAS")


@_attrs_define
class MapReferenceSectionAS:
    """
    Attributes:
        point_address (PointAddressSection | Unset):
        segments (list[Segment] | Unset): The section containing the segment references
        country (AdminIdSection | Unset):
        state (AdminIdSection | Unset):
        county (AdminIdSection | Unset):
        city (AdminIdSection | Unset):
        district (AdminIdSection | Unset):
        subdistrict (AdminIdSection | Unset):
    """

    point_address: PointAddressSection | Unset = UNSET
    segments: list[Segment] | Unset = UNSET
    country: AdminIdSection | Unset = UNSET
    state: AdminIdSection | Unset = UNSET
    county: AdminIdSection | Unset = UNSET
    city: AdminIdSection | Unset = UNSET
    district: AdminIdSection | Unset = UNSET
    subdistrict: AdminIdSection | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        point_address: dict[str, Any] | Unset = UNSET
        if not isinstance(self.point_address, Unset):
            point_address = self.point_address.to_dict()

        segments: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.segments, Unset):
            segments = []
            for segments_item_data in self.segments:
                segments_item = segments_item_data.to_dict()
                segments.append(segments_item)

        country: dict[str, Any] | Unset = UNSET
        if not isinstance(self.country, Unset):
            country = self.country.to_dict()

        state: dict[str, Any] | Unset = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.to_dict()

        county: dict[str, Any] | Unset = UNSET
        if not isinstance(self.county, Unset):
            county = self.county.to_dict()

        city: dict[str, Any] | Unset = UNSET
        if not isinstance(self.city, Unset):
            city = self.city.to_dict()

        district: dict[str, Any] | Unset = UNSET
        if not isinstance(self.district, Unset):
            district = self.district.to_dict()

        subdistrict: dict[str, Any] | Unset = UNSET
        if not isinstance(self.subdistrict, Unset):
            subdistrict = self.subdistrict.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if point_address is not UNSET:
            field_dict["pointAddress"] = point_address
        if segments is not UNSET:
            field_dict["segments"] = segments
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.admin_id_section import AdminIdSection
        from ..models.point_address_section import PointAddressSection
        from ..models.segment import Segment

        d = dict(src_dict)
        _point_address = d.pop("pointAddress", UNSET)
        point_address: PointAddressSection | Unset
        if isinstance(_point_address, Unset):
            point_address = UNSET
        else:
            point_address = PointAddressSection.from_dict(_point_address)

        _segments = d.pop("segments", UNSET)
        segments: list[Segment] | Unset = UNSET
        if _segments is not UNSET:
            segments = []
            for segments_item_data in _segments:
                segments_item = Segment.from_dict(segments_item_data)

                segments.append(segments_item)

        _country = d.pop("country", UNSET)
        country: AdminIdSection | Unset
        if isinstance(_country, Unset):
            country = UNSET
        else:
            country = AdminIdSection.from_dict(_country)

        _state = d.pop("state", UNSET)
        state: AdminIdSection | Unset
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = AdminIdSection.from_dict(_state)

        _county = d.pop("county", UNSET)
        county: AdminIdSection | Unset
        if isinstance(_county, Unset):
            county = UNSET
        else:
            county = AdminIdSection.from_dict(_county)

        _city = d.pop("city", UNSET)
        city: AdminIdSection | Unset
        if isinstance(_city, Unset):
            city = UNSET
        else:
            city = AdminIdSection.from_dict(_city)

        _district = d.pop("district", UNSET)
        district: AdminIdSection | Unset
        if isinstance(_district, Unset):
            district = UNSET
        else:
            district = AdminIdSection.from_dict(_district)

        _subdistrict = d.pop("subdistrict", UNSET)
        subdistrict: AdminIdSection | Unset
        if isinstance(_subdistrict, Unset):
            subdistrict = UNSET
        else:
            subdistrict = AdminIdSection.from_dict(_subdistrict)

        map_reference_section_as = cls(
            point_address=point_address,
            segments=segments,
            country=country,
            state=state,
            county=county,
            city=city,
            district=district,
            subdistrict=subdistrict,
        )

        map_reference_section_as.additional_properties = d
        return map_reference_section_as

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
