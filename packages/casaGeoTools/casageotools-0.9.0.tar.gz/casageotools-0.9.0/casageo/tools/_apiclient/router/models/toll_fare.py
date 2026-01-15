from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fare_pass import FarePass
    from ..models.range_price import RangePrice
    from ..models.single_price import SinglePrice
    from ..models.transponder_system import TransponderSystem


T = TypeVar("T", bound="TollFare")


@_attrs_define
class TollFare:
    """Contains information about a single toll fare needed for this section of the route.

    Attributes:
        id (str): Unique Fare id. Used to deduplicate fares that apply to multiple sections Example:
            carrideco-1753076078174759852-1749341260512683512.
        name (str): Name of a toll fare.

            **NOTE** This property is deprecated. A toll fare represents one of the various fares linked to the route
            section
            toll cost(`TollCost`) and for a toll cost associated with a single toll system the fare name is same as the
            toll system name. But for a toll cost associated with multiple toll systems this parameter will return the name
            of
            only one toll system. To get the names of all the toll systems associated with a toll cost use
            `TollCost.tollSystems`.
             Example: Carride Company.
        price (RangePrice | SinglePrice): Price of a fare
        converted_price (RangePrice | SinglePrice | Unset): Price of a fare
        reason (str | Unset): Extensible enum: `ride` `parking` `toll` `...`
            Reason for the cost described in this `Fare` element.
             Default: 'ride'.
        payment_methods (list[str] | Unset): Specifies the payment methods for which this fare is valid.
        pass_ (FarePass | Unset): Specifies whether this `Fare` is a multi-travel pass, and its characteristics
        applicable_times (str | Unset): Specifies date and time period during which the restriction applies. Value is a
            string in the Time
            Domain format. Time Domain is part of the GDF (Geographic Data Files) specification, which is an ISO standard.
            Current standard is GDF 5.1 which is [ISO 20524-1:2020](https://www.iso.org/standard/68244.html).

            For a detailed description of the Time Domain specification and usage in routing services, please refer to
            the documentation available in the [Time Domain](https://www.here.com/docs/bundle/routing-api-developer-
            guide-v8/page/concepts/time-domain.html) page of the Developer Guide.
             Example: -(d1){w1}(d3){d1}.
        transponders (list[TransponderSystem] | Unset): List of transponder systems for which this fare is applicable.
            Only available for transponder payment method
    """

    id: str
    name: str
    price: RangePrice | SinglePrice
    converted_price: RangePrice | SinglePrice | Unset = UNSET
    reason: str | Unset = "ride"
    payment_methods: list[str] | Unset = UNSET
    pass_: FarePass | Unset = UNSET
    applicable_times: str | Unset = UNSET
    transponders: list[TransponderSystem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.single_price import SinglePrice

        id = self.id

        name = self.name

        price: dict[str, Any]
        if isinstance(self.price, SinglePrice):
            price = self.price.to_dict()
        else:
            price = self.price.to_dict()

        converted_price: dict[str, Any] | Unset
        if isinstance(self.converted_price, Unset):
            converted_price = UNSET
        elif isinstance(self.converted_price, SinglePrice):
            converted_price = self.converted_price.to_dict()
        else:
            converted_price = self.converted_price.to_dict()

        reason = self.reason

        payment_methods: list[str] | Unset = UNSET
        if not isinstance(self.payment_methods, Unset):
            payment_methods = self.payment_methods

        pass_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.pass_, Unset):
            pass_ = self.pass_.to_dict()

        applicable_times = self.applicable_times

        transponders: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.transponders, Unset):
            transponders = []
            for transponders_item_data in self.transponders:
                transponders_item = transponders_item_data.to_dict()
                transponders.append(transponders_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
            "price": price,
        })
        if converted_price is not UNSET:
            field_dict["convertedPrice"] = converted_price
        if reason is not UNSET:
            field_dict["reason"] = reason
        if payment_methods is not UNSET:
            field_dict["paymentMethods"] = payment_methods
        if pass_ is not UNSET:
            field_dict["pass"] = pass_
        if applicable_times is not UNSET:
            field_dict["applicableTimes"] = applicable_times
        if transponders is not UNSET:
            field_dict["transponders"] = transponders

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fare_pass import FarePass
        from ..models.range_price import RangePrice
        from ..models.single_price import SinglePrice
        from ..models.transponder_system import TransponderSystem

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_price(data: object) -> RangePrice | SinglePrice:
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

        price = _parse_price(d.pop("price"))

        def _parse_converted_price(data: object) -> RangePrice | SinglePrice | Unset:
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

        converted_price = _parse_converted_price(d.pop("convertedPrice", UNSET))

        reason = d.pop("reason", UNSET)

        payment_methods = cast(list[str], d.pop("paymentMethods", UNSET))

        _pass_ = d.pop("pass", UNSET)
        pass_: FarePass | Unset
        if isinstance(_pass_, Unset):
            pass_ = UNSET
        else:
            pass_ = FarePass.from_dict(_pass_)

        applicable_times = d.pop("applicableTimes", UNSET)

        _transponders = d.pop("transponders", UNSET)
        transponders: list[TransponderSystem] | Unset = UNSET
        if _transponders is not UNSET:
            transponders = []
            for transponders_item_data in _transponders:
                transponders_item = TransponderSystem.from_dict(transponders_item_data)

                transponders.append(transponders_item)

        toll_fare = cls(
            id=id,
            name=name,
            price=price,
            converted_price=converted_price,
            reason=reason,
            payment_methods=payment_methods,
            pass_=pass_,
            applicable_times=applicable_times,
            transponders=transponders,
        )

        toll_fare.additional_properties = d
        return toll_fare

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
