from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.range_price import RangePrice
    from ..models.single_price import SinglePrice
    from ..models.toll_country_summary import TollCountrySummary
    from ..models.toll_system_summary import TollSystemSummary


T = TypeVar("T", bound="TollSummary")


@_attrs_define
class TollSummary:
    """The summary of the tolls grouped by criteria (total, per system, per country).

    Attributes:
        total (RangePrice | SinglePrice | Unset): Price of a fare
        total_by_system (list[TollSystemSummary] | Unset): Categorizes toll fees based on the different toll systems
            applicable along the route or section. Each toll system has its own set of charges and payment rules. The
            summary provides a breakdown of toll costs for each individual toll system encountered.
        total_by_country (list[TollCountrySummary] | Unset): Groups toll fees based on the countries traversed during
            the route or section. It provides a breakdown of toll charges specific to each country.
    """

    total: RangePrice | SinglePrice | Unset = UNSET
    total_by_system: list[TollSystemSummary] | Unset = UNSET
    total_by_country: list[TollCountrySummary] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.single_price import SinglePrice

        total: dict[str, Any] | Unset
        if isinstance(self.total, Unset):
            total = UNSET
        elif isinstance(self.total, SinglePrice):
            total = self.total.to_dict()
        else:
            total = self.total.to_dict()

        total_by_system: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.total_by_system, Unset):
            total_by_system = []
            for total_by_system_item_data in self.total_by_system:
                total_by_system_item = total_by_system_item_data.to_dict()
                total_by_system.append(total_by_system_item)

        total_by_country: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.total_by_country, Unset):
            total_by_country = []
            for total_by_country_item_data in self.total_by_country:
                total_by_country_item = total_by_country_item_data.to_dict()
                total_by_country.append(total_by_country_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total is not UNSET:
            field_dict["total"] = total
        if total_by_system is not UNSET:
            field_dict["totalBySystem"] = total_by_system
        if total_by_country is not UNSET:
            field_dict["totalByCountry"] = total_by_country

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.range_price import RangePrice
        from ..models.single_price import SinglePrice
        from ..models.toll_country_summary import TollCountrySummary
        from ..models.toll_system_summary import TollSystemSummary

        d = dict(src_dict)

        def _parse_total(data: object) -> RangePrice | SinglePrice | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_fare_price_type_0 = SinglePrice.from_dict(data)

                return componentsschemas_fare_price_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_fare_price_type_1 = RangePrice.from_dict(data)

            return componentsschemas_fare_price_type_1

        total = _parse_total(d.pop("total", UNSET))

        _total_by_system = d.pop("totalBySystem", UNSET)
        total_by_system: list[TollSystemSummary] | Unset = UNSET
        if _total_by_system is not UNSET:
            total_by_system = []
            for total_by_system_item_data in _total_by_system:
                total_by_system_item = TollSystemSummary.from_dict(
                    total_by_system_item_data
                )

                total_by_system.append(total_by_system_item)

        _total_by_country = d.pop("totalByCountry", UNSET)
        total_by_country: list[TollCountrySummary] | Unset = UNSET
        if _total_by_country is not UNSET:
            total_by_country = []
            for total_by_country_item_data in _total_by_country:
                total_by_country_item = TollCountrySummary.from_dict(
                    total_by_country_item_data
                )

                total_by_country.append(total_by_country_item)

        toll_summary = cls(
            total=total,
            total_by_system=total_by_system,
            total_by_country=total_by_country,
        )

        toll_summary.additional_properties = d
        return toll_summary

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
