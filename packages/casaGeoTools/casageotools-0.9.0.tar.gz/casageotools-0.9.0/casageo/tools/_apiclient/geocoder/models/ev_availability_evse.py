from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ev_availability_evse_state import EvAvailabilityEvseState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ev_availability_connector import EvAvailabilityConnector


T = TypeVar("T", bound="EvAvailabilityEvse")


@_attrs_define
class EvAvailabilityEvse:
    """
    Attributes:
        id (str | Unset): HERE ID of the EVSE
        cpo_id (str | Unset): The unique ID of an EVSE in the system of the CPO.
             This ID is unique in the system of the CPO but not necessarily globally unique.
             The format will differ between different CPOs. This ID is always provided.
        cpo_evse_emi3_id (str | Unset): Identifier in eMI3 format of the EVSE within the Charge Point Operator (CPO)
            platform.
            This ID is not always present. Example of ID format: "`DE*ICT*E0001897`".
        state (EvAvailabilityEvseState | Unset): EVSE status

            Description of supported values:

            - `AVAILABLE`: The EVSE is able to start a new charging session.
            - `OCCUPIED`: The EVSE is in use
            - `OFFLINE`: No status information available. (Also used when offline)
            - `OTHER`: No status information available. (Also used when offline)
            - `OUT_OF_SERVICE`: The EVSE is currently out of order.
            - `RESERVED`: The EVSE has been reserved for a particular EV driver and is unavailable for other drivers
            - `UNAVAILABLE`: The EVSE is not available because of a physical barrier, for example a car
        last_updated (str | Unset): Last update of the dynamic connector availability information reflected in the
            connectorStatus elements,
            in ISO 8601 format. If the time is UTC, a Z is added.
            An example of this kind of timestamp value is "`2013-12-31T12:00:00.000Z`". If the time is not UTC ,
            then the offset is added as a ±[hh][mm] value (for example, "`2014-01-14T10:00:00.000+0100`").
        connectors (list[EvAvailabilityConnector] | Unset): List of connectors of this EVSE.
    """

    id: str | Unset = UNSET
    cpo_id: str | Unset = UNSET
    cpo_evse_emi3_id: str | Unset = UNSET
    state: EvAvailabilityEvseState | Unset = UNSET
    last_updated: str | Unset = UNSET
    connectors: list[EvAvailabilityConnector] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        cpo_id = self.cpo_id

        cpo_evse_emi3_id = self.cpo_evse_emi3_id

        state: str | Unset = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        last_updated = self.last_updated

        connectors: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.connectors, Unset):
            connectors = []
            for connectors_item_data in self.connectors:
                connectors_item = connectors_item_data.to_dict()
                connectors.append(connectors_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if cpo_id is not UNSET:
            field_dict["cpoId"] = cpo_id
        if cpo_evse_emi3_id is not UNSET:
            field_dict["cpoEvseEMI3Id"] = cpo_evse_emi3_id
        if state is not UNSET:
            field_dict["state"] = state
        if last_updated is not UNSET:
            field_dict["last_updated"] = last_updated
        if connectors is not UNSET:
            field_dict["connectors"] = connectors

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ev_availability_connector import EvAvailabilityConnector

        d = dict(src_dict)
        id = d.pop("id", UNSET)

        cpo_id = d.pop("cpoId", UNSET)

        cpo_evse_emi3_id = d.pop("cpoEvseEMI3Id", UNSET)

        _state = d.pop("state", UNSET)
        state: EvAvailabilityEvseState | Unset
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = EvAvailabilityEvseState(_state)

        last_updated = d.pop("last_updated", UNSET)

        _connectors = d.pop("connectors", UNSET)
        connectors: list[EvAvailabilityConnector] | Unset = UNSET
        if _connectors is not UNSET:
            connectors = []
            for connectors_item_data in _connectors:
                connectors_item = EvAvailabilityConnector.from_dict(
                    connectors_item_data
                )

                connectors.append(connectors_item)

        ev_availability_evse = cls(
            id=id,
            cpo_id=cpo_id,
            cpo_evse_emi3_id=cpo_evse_emi3_id,
            state=state,
            last_updated=last_updated,
            connectors=connectors,
        )

        ev_availability_evse.additional_properties = d
        return ev_availability_evse

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
