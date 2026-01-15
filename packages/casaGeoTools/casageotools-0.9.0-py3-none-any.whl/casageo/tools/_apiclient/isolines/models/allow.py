from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Allow")


@_attrs_define
class Allow:
    """Explicitly allow features that require users to opt in.

    Attributes:
        hov (bool | Unset): This parameter specifies whether HOV lanes can be used in the calculation.

            An HOV (High occupancy Vehicle) lane or carpool lane is reserved for carpool usage.
            Carpool lane requires a minimum number of passengers in order for the car to use the
            carpool lane.

            **Notes**:
              - This parameter can't be used with 'vehicle[hovOccupancy]'.
              - This parameter should be used with `vehicle[occupancy]`. If `vehicle[occupancy]` is set, then only HOV lanes
            allowing this number of occupants will be allowed. If `vehicle[occupancy]` is not set, occupancy requirements
            are always considered fulfilled.
              - In case of violation, `violatedCarpool` notice will be returned.
             Default: False.
        hot (bool | Unset): This parameter specifies whether HOT lanes can be used in the calculation.

            HOT (high-occupancy toll) lanes are HOV lanes where vehicles that do not qualify as high-occupancy are allowed
            to pass by paying a toll.

            **Notes**:
              - This parameter can't be used with 'vehicle[hovOccupancy]'.
              - This parameter can be used with `allow[hov]`.
              - In case of violation, `violatedCarpool` notice will be returned.
              - No toll information is returned for HOT lanes since it is dynamic information.
             Default: False.
    """

    hov: bool | Unset = False
    hot: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hov = self.hov

        hot = self.hot

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if hov is not UNSET:
            field_dict["hov"] = hov
        if hot is not UNSET:
            field_dict["hot"] = hot

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        hov = d.pop("hov", UNSET)

        hot = d.pop("hot", UNSET)

        allow = cls(
            hov=hov,
            hot=hot,
        )

        allow.additional_properties = d
        return allow

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
