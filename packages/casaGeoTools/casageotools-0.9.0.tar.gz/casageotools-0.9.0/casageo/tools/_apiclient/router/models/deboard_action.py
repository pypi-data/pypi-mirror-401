from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.deboard_action_action import DeboardActionAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeboardAction")


@_attrs_define
class DeboardAction:
    """An action to disembark a ferry.

    Attributes:
        action (DeboardActionAction): The type of the action.

            **NOTE:** The list of possible actions may be extended in the future. The client application should handle such
            a case gracefully.
        duration (int): Duration in seconds. Example: 198.
        instruction (str | Unset): Description of the action (e.g. Turn left onto Minna St.).
    """

    action: DeboardActionAction
    duration: int
    instruction: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action.value

        duration = self.duration

        instruction = self.instruction

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "action": action,
            "duration": duration,
        })
        if instruction is not UNSET:
            field_dict["instruction"] = instruction

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action = DeboardActionAction(d.pop("action"))

        duration = d.pop("duration")

        instruction = d.pop("instruction", UNSET)

        deboard_action = cls(
            action=action,
            duration=duration,
            instruction=instruction,
        )

        deboard_action.additional_properties = d
        return deboard_action

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
