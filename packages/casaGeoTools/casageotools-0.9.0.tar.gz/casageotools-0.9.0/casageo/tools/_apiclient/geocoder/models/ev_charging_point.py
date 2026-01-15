from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EvChargingPoint")


@_attrs_define
class EvChargingPoint:
    """
    Attributes:
        number_of_connectors (int | Unset): Number of physical connectors in the connectors group
        volts_range (str | Unset): Voltage provided by the connectors group Example: 100-120V AC.
        phases (int | Unset): Number of phases provided by the connectors group
        amps_range (str | Unset): Amperage provided by the connectors group Example: 12A-80A.
        number_of_available (int | Unset): Number of available physical connectors in the connectors group (i.e not
            being used to charge a vehicle, out of service, etc)
        number_of_in_use (int | Unset): Number of occupied physical connectors in the connectors group.
        number_of_out_of_service (int | Unset): Number of physical connectors that are out of service at the charge
            point.
        number_of_reserved (int | Unset): Number of physical connectors that are reserved at the charge point.
        last_update_timestamp (str | Unset):
            Information about when the `numberOfAvailable` and `numberOfInUse` fields were last updated, in ISO 8601 format.
            If the time is UTC, a Z is added.
            If the time is not UTC , then the offset is added as a ±[hh][mm] value.
             Example: 2013-12-31T12:00:00.000Z.
    """

    number_of_connectors: int | Unset = UNSET
    volts_range: str | Unset = UNSET
    phases: int | Unset = UNSET
    amps_range: str | Unset = UNSET
    number_of_available: int | Unset = UNSET
    number_of_in_use: int | Unset = UNSET
    number_of_out_of_service: int | Unset = UNSET
    number_of_reserved: int | Unset = UNSET
    last_update_timestamp: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        number_of_connectors = self.number_of_connectors

        volts_range = self.volts_range

        phases = self.phases

        amps_range = self.amps_range

        number_of_available = self.number_of_available

        number_of_in_use = self.number_of_in_use

        number_of_out_of_service = self.number_of_out_of_service

        number_of_reserved = self.number_of_reserved

        last_update_timestamp = self.last_update_timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if number_of_connectors is not UNSET:
            field_dict["numberOfConnectors"] = number_of_connectors
        if volts_range is not UNSET:
            field_dict["voltsRange"] = volts_range
        if phases is not UNSET:
            field_dict["phases"] = phases
        if amps_range is not UNSET:
            field_dict["ampsRange"] = amps_range
        if number_of_available is not UNSET:
            field_dict["numberOfAvailable"] = number_of_available
        if number_of_in_use is not UNSET:
            field_dict["numberOfInUse"] = number_of_in_use
        if number_of_out_of_service is not UNSET:
            field_dict["numberOfOutOfService"] = number_of_out_of_service
        if number_of_reserved is not UNSET:
            field_dict["numberOfReserved"] = number_of_reserved
        if last_update_timestamp is not UNSET:
            field_dict["lastUpdateTimestamp"] = last_update_timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        number_of_connectors = d.pop("numberOfConnectors", UNSET)

        volts_range = d.pop("voltsRange", UNSET)

        phases = d.pop("phases", UNSET)

        amps_range = d.pop("ampsRange", UNSET)

        number_of_available = d.pop("numberOfAvailable", UNSET)

        number_of_in_use = d.pop("numberOfInUse", UNSET)

        number_of_out_of_service = d.pop("numberOfOutOfService", UNSET)

        number_of_reserved = d.pop("numberOfReserved", UNSET)

        last_update_timestamp = d.pop("lastUpdateTimestamp", UNSET)

        ev_charging_point = cls(
            number_of_connectors=number_of_connectors,
            volts_range=volts_range,
            phases=phases,
            amps_range=amps_range,
            number_of_available=number_of_available,
            number_of_in_use=number_of_in_use,
            number_of_out_of_service=number_of_out_of_service,
            number_of_reserved=number_of_reserved,
            last_update_timestamp=last_update_timestamp,
        )

        ev_charging_point.additional_properties = d
        return ev_charging_point

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
