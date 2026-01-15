from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.range_price import RangePrice
    from ..models.single_price import SinglePrice


T = TypeVar("T", bound="TollCountrySummary")


@_attrs_define
class TollCountrySummary:
    """
    Attributes:
        country_code (str | Unset): ISO-3166-1 alpha-3 code Example: FRA.
        price (RangePrice | SinglePrice | Unset): Price of a fare
    """

    country_code: str | Unset = UNSET
    price: RangePrice | SinglePrice | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.single_price import SinglePrice

        country_code = self.country_code

        price: dict[str, Any] | Unset
        if isinstance(self.price, Unset):
            price = UNSET
        elif isinstance(self.price, SinglePrice):
            price = self.price.to_dict()
        else:
            price = self.price.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code
        if price is not UNSET:
            field_dict["price"] = price

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.range_price import RangePrice
        from ..models.single_price import SinglePrice

        d = dict(src_dict)
        country_code = d.pop("countryCode", UNSET)

        def _parse_price(data: object) -> RangePrice | SinglePrice | Unset:
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

        price = _parse_price(d.pop("price", UNSET))

        toll_country_summary = cls(
            country_code=country_code,
            price=price,
        )

        toll_country_summary.additional_properties = d
        return toll_country_summary

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
