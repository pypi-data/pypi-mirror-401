from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EvAvailabilityConnector")


@_attrs_define
class EvAvailabilityConnector:
    """
    Attributes:
        id (str | Unset): HERE ID of the connector.
        cpo_id (str | Unset): CPO ID of the connector.
        type_id (str | Unset): Connector type ID. For more information on the current connector types,
            see [resource-type-connector-types.html](https://www.here.com/docs/bundle/ev-charge-points-api-developer-
            guide/page/topics/resource-type-connector-types.html)
        max_power_level (float | Unset): Maximum charge power of connector in kilowatts.
    """

    id: str | Unset = UNSET
    cpo_id: str | Unset = UNSET
    type_id: str | Unset = UNSET
    max_power_level: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        cpo_id = self.cpo_id

        type_id = self.type_id

        max_power_level = self.max_power_level

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if cpo_id is not UNSET:
            field_dict["cpoId"] = cpo_id
        if type_id is not UNSET:
            field_dict["typeId"] = type_id
        if max_power_level is not UNSET:
            field_dict["maxPowerLevel"] = max_power_level

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        cpo_id = d.pop("cpoId", UNSET)

        type_id = d.pop("typeId", UNSET)

        max_power_level = d.pop("maxPowerLevel", UNSET)

        ev_availability_connector = cls(
            id=id,
            cpo_id=cpo_id,
            type_id=type_id,
            max_power_level=max_power_level,
        )

        ev_availability_connector.additional_properties = d
        return ev_availability_connector

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
