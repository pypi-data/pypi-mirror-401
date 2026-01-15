from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ev_charging_point import EvChargingPoint
    from ..models.ev_name_id import EvNameId


T = TypeVar("T", bound="EvConnector")


@_attrs_define
class EvConnector:
    """
    Attributes:
        supplier_name (str | Unset): The EV charge point operator
        connector_type (EvNameId | Unset):
        fixed_cable (bool | Unset): Boolean indicating if a cable is provided for the connector group.If true, then
            there is a cable for the connector group at the station.
        max_power_level (float | Unset): Maximum charge power (in kilowatt) of connectors in connectors group.
        charging_point (EvChargingPoint | Unset):
    """

    supplier_name: str | Unset = UNSET
    connector_type: EvNameId | Unset = UNSET
    fixed_cable: bool | Unset = UNSET
    max_power_level: float | Unset = UNSET
    charging_point: EvChargingPoint | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        supplier_name = self.supplier_name

        connector_type: dict[str, Any] | Unset = UNSET
        if not isinstance(self.connector_type, Unset):
            connector_type = self.connector_type.to_dict()

        fixed_cable = self.fixed_cable

        max_power_level = self.max_power_level

        charging_point: dict[str, Any] | Unset = UNSET
        if not isinstance(self.charging_point, Unset):
            charging_point = self.charging_point.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if supplier_name is not UNSET:
            field_dict["supplierName"] = supplier_name
        if connector_type is not UNSET:
            field_dict["connectorType"] = connector_type
        if fixed_cable is not UNSET:
            field_dict["fixedCable"] = fixed_cable
        if max_power_level is not UNSET:
            field_dict["maxPowerLevel"] = max_power_level
        if charging_point is not UNSET:
            field_dict["chargingPoint"] = charging_point

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ev_charging_point import EvChargingPoint
        from ..models.ev_name_id import EvNameId

        d = dict(src_dict)
        supplier_name = d.pop("supplierName", UNSET)

        _connector_type = d.pop("connectorType", UNSET)
        connector_type: EvNameId | Unset
        if isinstance(_connector_type, Unset):
            connector_type = UNSET
        else:
            connector_type = EvNameId.from_dict(_connector_type)

        fixed_cable = d.pop("fixedCable", UNSET)

        max_power_level = d.pop("maxPowerLevel", UNSET)

        _charging_point = d.pop("chargingPoint", UNSET)
        charging_point: EvChargingPoint | Unset
        if isinstance(_charging_point, Unset):
            charging_point = UNSET
        else:
            charging_point = EvChargingPoint.from_dict(_charging_point)

        ev_connector = cls(
            supplier_name=supplier_name,
            connector_type=connector_type,
            fixed_cable=fixed_cable,
            max_power_level=max_power_level,
            charging_point=charging_point,
        )

        ev_connector.additional_properties = d
        return ev_connector

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
