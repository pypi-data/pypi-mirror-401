from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.car_fuel_type import CarFuelType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fuel_additive import FuelAdditive
    from ..models.fuel_price import FuelPrice


T = TypeVar("T", bound="CarFuel")


@_attrs_define
class CarFuel:
    """
    Attributes:
        type_ (CarFuelType): **BETA, RESTRICTED**

            The type of car fuel

            Description of supported values:

            - **BETA, RESTRICTED** `biodiesel`: bio-diesel
            - **BETA, RESTRICTED** `cng`: compressed natural gas (CNG)
            - **BETA, RESTRICTED** `diesel`: diesel
            - **BETA, RESTRICTED** `diesel_with_additives`: diesel with additives
            - **BETA, RESTRICTED** `e10`: E10 (10% ethanol)
            - **BETA, RESTRICTED** `e20`: E20 (20% ethanol)
            - **BETA, RESTRICTED** `e85`: E85 (minimum 70% ethanol blended gasoline)
            - **BETA, RESTRICTED** `ethanol`: ethanol fuel (when specific type is not known, such as E10, E85)
            - **BETA, RESTRICTED** `ethanol_with_additives`: ethanol with additives
            - **BETA, RESTRICTED** `gasoline`: gasoline
            - **BETA, RESTRICTED** `hvo`: hydrotreated vegetable oil fuel
            - **BETA, RESTRICTED** `hydrogen`: hydrogen
            - **BETA, RESTRICTED** `lng`: liquefied natural gas (LNG)
            - **BETA, RESTRICTED** `lpg`: liquefied petroleum gas (LPG)
            - **BETA, RESTRICTED** `midgrade`: midgrade octane rating
            - **BETA, RESTRICTED** `octane_100`: fuel that consists of 100% octane
            - **BETA, RESTRICTED** `octane_87`: fuel that consists of an octane / gasoline blend with 87% octane / 13%
            gasoline
            - **BETA, RESTRICTED** `octane_89`: fuel that consists of an octane / gasoline blend with 89% octane / 11%
            gasoline
            - **BETA, RESTRICTED** `octane_90`: fuel that consists of an octane / gasoline blend with 90% octane / 10%
            gasoline
            - **BETA, RESTRICTED** `octane_91`: fuel that consists of an octane / gasoline blend with 91% octane / 9%
            gasoline
            - **BETA, RESTRICTED** `octane_92`: fuel that consists of an octane / gasoline blend with 92% octane / 8%
            gasoline
            - **BETA, RESTRICTED** `octane_93`: fuel that consists of octane / gasoline blend with 93% octane / 7% gasoline
            - **BETA, RESTRICTED** `octane_95`: fuel that consists of an octane / gasoline blend with 95% octane / 5%
            gasoline
            - **BETA, RESTRICTED** `octane_98`:  fuel that consists of an octane / gasoline blend with 98% octane / 2%
            gasoline
            - **BETA, RESTRICTED** `premium`: premium octane rating
            - **BETA, RESTRICTED** `regular`: regular octance rating
        available (bool): **BETA, RESTRICTED**

            When set to:
            - `true` indicates that this type of car fuel is available at this place
            - `false` indicates that this type of car fuel is not available at this place
        additives (list[FuelAdditive] | Unset): **BETA, RESTRICTED**

            A list of additional compound fluids sold at the location, related to the specific fuel type
        pressures (list[int] | Unset): **BETA, RESTRICTED**

            Indicates the pressure values in bar for hydrogen fuel at the location
        price (FuelPrice | Unset):
    """

    type_: CarFuelType
    available: bool
    additives: list[FuelAdditive] | Unset = UNSET
    pressures: list[int] | Unset = UNSET
    price: FuelPrice | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        available = self.available

        additives: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.additives, Unset):
            additives = []
            for additives_item_data in self.additives:
                additives_item = additives_item_data.to_dict()
                additives.append(additives_item)

        pressures: list[int] | Unset = UNSET
        if not isinstance(self.pressures, Unset):
            pressures = self.pressures

        price: dict[str, Any] | Unset = UNSET
        if not isinstance(self.price, Unset):
            price = self.price.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "available": available,
        })
        if additives is not UNSET:
            field_dict["additives"] = additives
        if pressures is not UNSET:
            field_dict["pressures"] = pressures
        if price is not UNSET:
            field_dict["price"] = price

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fuel_additive import FuelAdditive
        from ..models.fuel_price import FuelPrice

        d = dict(src_dict)
        type_ = CarFuelType(d.pop("type"))

        available = d.pop("available")

        _additives = d.pop("additives", UNSET)
        additives: list[FuelAdditive] | Unset = UNSET
        if _additives is not UNSET:
            additives = []
            for additives_item_data in _additives:
                additives_item = FuelAdditive.from_dict(additives_item_data)

                additives.append(additives_item)

        pressures = cast(list[int], d.pop("pressures", UNSET))

        _price = d.pop("price", UNSET)
        price: FuelPrice | Unset
        if isinstance(_price, Unset):
            price = UNSET
        else:
            price = FuelPrice.from_dict(_price)

        car_fuel = cls(
            type_=type_,
            available=available,
            additives=additives,
            pressures=pressures,
            price=price,
        )

        car_fuel.additional_properties = d
        return car_fuel

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
