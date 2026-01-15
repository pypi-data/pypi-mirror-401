from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.wait_action_action import WaitActionAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="WaitAction")


@_attrs_define
class WaitAction:
    """A wait operation to be performed at or during a specific portion of a section.

    Attributes:
        action (WaitActionAction): The type of the action.

            **NOTE:** The list of possible actions may be extended in the future. The client application should handle such
            a case gracefully.
        duration (int): Duration in seconds. Example: 198.
        instruction (str | Unset): Description of the action (e.g. Turn left onto Minna St.).
    """

    action: WaitActionAction
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
        action = WaitActionAction(d.pop("action"))

        duration = d.pop("duration")

        instruction = d.pop("instruction", UNSET)

        wait_action = cls(
            action=action,
            duration=duration,
            instruction=instruction,
        )

        wait_action.additional_properties = d
        return wait_action

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
