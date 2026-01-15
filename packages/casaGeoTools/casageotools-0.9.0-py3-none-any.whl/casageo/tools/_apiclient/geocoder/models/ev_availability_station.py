from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ev_availability_evse import EvAvailabilityEvse


T = TypeVar("T", bound="EvAvailabilityStation")


@_attrs_define
class EvAvailabilityStation:
    """
    Attributes:
        id (str | Unset): HERE ID of the station
        cpo_id (str | Unset): The unique ID of the location in the system of the CPO.
        evses (list[EvAvailabilityEvse] | Unset): List of EVSE (electric vehicle supply equipment) in the EV station
    """

    id: str | Unset = UNSET
    cpo_id: str | Unset = UNSET
    evses: list[EvAvailabilityEvse] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        cpo_id = self.cpo_id

        evses: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.evses, Unset):
            evses = []
            for evses_item_data in self.evses:
                evses_item = evses_item_data.to_dict()
                evses.append(evses_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if cpo_id is not UNSET:
            field_dict["cpoId"] = cpo_id
        if evses is not UNSET:
            field_dict["evses"] = evses

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ev_availability_evse import EvAvailabilityEvse

        d = dict(src_dict)
        id = d.pop("id", UNSET)

        cpo_id = d.pop("cpoId", UNSET)

        _evses = d.pop("evses", UNSET)
        evses: list[EvAvailabilityEvse] | Unset = UNSET
        if _evses is not UNSET:
            evses = []
            for evses_item_data in _evses:
                evses_item = EvAvailabilityEvse.from_dict(evses_item_data)

                evses.append(evses_item)

        ev_availability_station = cls(
            id=id,
            cpo_id=cpo_id,
            evses=evses,
        )

        ev_availability_station.additional_properties = d
        return ev_availability_station

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
