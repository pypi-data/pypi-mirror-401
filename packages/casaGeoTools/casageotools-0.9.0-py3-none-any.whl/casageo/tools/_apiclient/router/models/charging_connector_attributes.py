from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChargingConnectorAttributes")


@_attrs_define
class ChargingConnectorAttributes:
    """Details of the connector that is suggested to be used in the section's `postAction` for charging.

    Attributes:
        power (float): Power supplied by the suggested connector in kW.
        supply_type (str): Extensible enum: `acSingle` `acThree` `dc` `...`
            Currently possible values are:

            * `acSingle` : Single phase Alternating Current supply
            * `acThree`: Three phase Alternating Current supply
            * `dc`: Direct Current supply
        connector_type (str): Extensible enum: `iec62196Type1Combo` `iec62196Type2Combo` `chademo` `tesla` `saeJ3400`
            `gbtDc` `unknown` `...`
            Currently supported connector types are:
            * `iec62196Type1Combo`:  Type 1 Combo connector, commonly called "CCS1"
            * `iec62196Type2Combo`:  Type 2 Combo connector, commonly called "CCS2"
            * `chademo`: CHAdeMO connector
            * `tesla`: North American Charging Standard (NACS) connector. This connector type is deprecated. Return value
            used instead of `saeJ3400` when the user specifies the deprecated value `tesla` in `ev[connectorTypes]`
            * `saeJ3400`: North American Charging System (NACS) connector
            * `gbtDc`: GB/T Guobiao GB/T 20234.3 DC connector
            * `unknown`: Connector type is not known, e.g., if station is provided by user in request
        current (float | Unset): Current of the suggested connector in Amperes.
        voltage (float | Unset): Voltage of the suggested connector in Volts.
    """

    power: float
    supply_type: str
    connector_type: str
    current: float | Unset = UNSET
    voltage: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        power = self.power

        supply_type = self.supply_type

        connector_type = self.connector_type

        current = self.current

        voltage = self.voltage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "power": power,
            "supplyType": supply_type,
            "connectorType": connector_type,
        })
        if current is not UNSET:
            field_dict["current"] = current
        if voltage is not UNSET:
            field_dict["voltage"] = voltage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        power = d.pop("power")

        supply_type = d.pop("supplyType")

        connector_type = d.pop("connectorType")

        current = d.pop("current", UNSET)

        voltage = d.pop("voltage", UNSET)

        charging_connector_attributes = cls(
            power=power,
            supply_type=supply_type,
            connector_type=connector_type,
            current=current,
            voltage=voltage,
        )

        charging_connector_attributes.additional_properties = d
        return charging_connector_attributes

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
