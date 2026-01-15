from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.charging_action_action import ChargingActionAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChargingAction")


@_attrs_define
class ChargingAction:
    """An action to charge the vehicle.

    Attributes:
        action (ChargingActionAction): The type of the action.

            **NOTE:** The list of possible actions may be extended in the future. The client application should handle such
            a case gracefully.
        duration (int): Duration in seconds. Example: 198.
        instruction (str | Unset): Description of the action (e.g. Turn left onto Minna St.).
        consumable_power (float | Unset): Maximum charging power (in kW) available to the vehicle, based on the
            properties of the charging
            station and the vehicle.
        arrival_charge (float | Unset): Estimated vehicle battery charge before this action (in kWh).
        target_charge (float | Unset): Level to which vehicle battery should be charged by this action (in kWh).
    """

    action: ChargingActionAction
    duration: int
    instruction: str | Unset = UNSET
    consumable_power: float | Unset = UNSET
    arrival_charge: float | Unset = UNSET
    target_charge: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action.value

        duration = self.duration

        instruction = self.instruction

        consumable_power = self.consumable_power

        arrival_charge = self.arrival_charge

        target_charge = self.target_charge

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "action": action,
            "duration": duration,
        })
        if instruction is not UNSET:
            field_dict["instruction"] = instruction
        if consumable_power is not UNSET:
            field_dict["consumablePower"] = consumable_power
        if arrival_charge is not UNSET:
            field_dict["arrivalCharge"] = arrival_charge
        if target_charge is not UNSET:
            field_dict["targetCharge"] = target_charge

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action = ChargingActionAction(d.pop("action"))

        duration = d.pop("duration")

        instruction = d.pop("instruction", UNSET)

        consumable_power = d.pop("consumablePower", UNSET)

        arrival_charge = d.pop("arrivalCharge", UNSET)

        target_charge = d.pop("targetCharge", UNSET)

        charging_action = cls(
            action=action,
            duration=duration,
            instruction=instruction,
            consumable_power=consumable_power,
            arrival_charge=arrival_charge,
            target_charge=target_charge,
        )

        charging_action.additional_properties = d
        return charging_action

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
