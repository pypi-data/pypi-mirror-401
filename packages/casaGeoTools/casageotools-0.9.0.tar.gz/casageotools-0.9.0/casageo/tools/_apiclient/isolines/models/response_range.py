from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseRange")


@_attrs_define
class ResponseRange:
    """Range specified in terms of distance, travel time or energy consumption.

    Attributes:
        type_ (str): Specifies the type of range.

            Possible Values:
            - `distance` with units in meters
            - `time` with units in seconds
            - `consumption` with units in Watt-hours (Wh) for EV, or milliliters(ml) or grams(gms) for fuel-based vehicles,
            depending on `consumptionType`
        consumption_type (str | Unset): Specifies the consumption type. Returned only if range `type` is `consumption`.

            Possible Values:
              - `electric` : electric consumption type with units in Wh.
              - `diesel` : Diesel consumption type with units in ml.
              - `petrol` : Petrol/Gasoline consumption type with units in ml.
              - `lpg` : LPG consumption type with units in ml.
              - `cng` : CNG consumption type with units in gm.
        value (int | Unset): Range value. The unit is defined by the `type` parameter.
    """

    type_: str
    consumption_type: str | Unset = UNSET
    value: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        consumption_type = self.consumption_type

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
        })
        if consumption_type is not UNSET:
            field_dict["consumptionType"] = consumption_type
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        consumption_type = d.pop("consumptionType", UNSET)

        value = d.pop("value", UNSET)

        response_range = cls(
            type_=type_,
            consumption_type=consumption_type,
            value=value,
        )

        response_range.additional_properties = d
        return response_range

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
