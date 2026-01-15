from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Range")


@_attrs_define
class Range:
    """Ranges specified in terms of distance, travel time or energy consumption.

    Attributes:
        type_ (str): Specifies the type of range.

            Possible Values:
            - `distance` with units in meters with maximum value 1000000
            - `time` with units in seconds with maximum value 32400
            - `consumption` For fuel-based Vehicles : Static maximum value of 40000 with units in milliliters(ml) or
            grams(gms)
                            For EV : Maximum value of 650000 with units in Watt-hours (Wh). Dynamic limit up to the maximum
            value that allows the vehicle to travel a maximum of 900kms.
             Example: distance.
        values (str): A comma-separated list of ranges. The unit is defined by the `type` parameter. Example: 1000,2000.
    """

    type_: str
    values: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        values = self.values

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "values": values,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        values = d.pop("values")

        range_ = cls(
            type_=type_,
            values=values,
        )

        range_.additional_properties = d
        return range_

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
