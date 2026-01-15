from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.continue_action_action import ContinueActionAction
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.exit_info import ExitInfo
    from ..models.localized_string import LocalizedString
    from ..models.road_info import RoadInfo
    from ..models.signpost_info import SignpostInfo


T = TypeVar("T", bound="ContinueAction")


@_attrs_define
class ContinueAction:
    """A continue operation to be performed at or during a specific portion of a section.

    Attributes:
        action (ContinueActionAction): The type of the action.

            **NOTE:** The list of possible actions may be extended in the future. The client application should handle such
            a case gracefully.
        duration (int): Duration in seconds. Example: 198.
        instruction (str | Unset): Description of the action (e.g. Turn left onto Minna St.).
        offset (int | Unset): Offset of a coordinate in the section's polyline.
        length (int | Unset): Distance in meters. Example: 189.
        current_road (RoadInfo | Unset): Road information attached to an offset action Example: {'fennstrasse': {'type':
            'street', 'name': [{'value': 'Fennstraße', 'language': 'de'}], 'number': [{'value': 'B96', 'language': 'de'}],
            'toward': [{'value': 'Reinickendorf', 'language': 'de'}]}}.
        next_road (RoadInfo | Unset): Road information attached to an offset action Example: {'fennstrasse': {'type':
            'street', 'name': [{'value': 'Fennstraße', 'language': 'de'}], 'number': [{'value': 'B96', 'language': 'de'}],
            'toward': [{'value': 'Reinickendorf', 'language': 'de'}]}}.
        exit_sign (ExitInfo | Unset): Exit information attached to an offset action Example: {'exit': {'number':
            [{'value': '15', 'language': 'de'}]}}.
        signpost (SignpostInfo | Unset): Signpost information attached to an offset action.
             Example: {'$ref': '#/components/examples/routeResponseManeuverSignpostInfoExample'}.
        intersection_name (list[LocalizedString] | Unset): Name of the intersection where the turn takes place, if
            available.
    """

    action: ContinueActionAction
    duration: int
    instruction: str | Unset = UNSET
    offset: int | Unset = UNSET
    length: int | Unset = UNSET
    current_road: RoadInfo | Unset = UNSET
    next_road: RoadInfo | Unset = UNSET
    exit_sign: ExitInfo | Unset = UNSET
    signpost: SignpostInfo | Unset = UNSET
    intersection_name: list[LocalizedString] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action.value

        duration = self.duration

        instruction = self.instruction

        offset = self.offset

        length = self.length

        current_road: dict[str, Any] | Unset = UNSET
        if not isinstance(self.current_road, Unset):
            current_road = self.current_road.to_dict()

        next_road: dict[str, Any] | Unset = UNSET
        if not isinstance(self.next_road, Unset):
            next_road = self.next_road.to_dict()

        exit_sign: dict[str, Any] | Unset = UNSET
        if not isinstance(self.exit_sign, Unset):
            exit_sign = self.exit_sign.to_dict()

        signpost: dict[str, Any] | Unset = UNSET
        if not isinstance(self.signpost, Unset):
            signpost = self.signpost.to_dict()

        intersection_name: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.intersection_name, Unset):
            intersection_name = []
            for intersection_name_item_data in self.intersection_name:
                intersection_name_item = intersection_name_item_data.to_dict()
                intersection_name.append(intersection_name_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "action": action,
            "duration": duration,
        })
        if instruction is not UNSET:
            field_dict["instruction"] = instruction
        if offset is not UNSET:
            field_dict["offset"] = offset
        if length is not UNSET:
            field_dict["length"] = length
        if current_road is not UNSET:
            field_dict["currentRoad"] = current_road
        if next_road is not UNSET:
            field_dict["nextRoad"] = next_road
        if exit_sign is not UNSET:
            field_dict["exitSign"] = exit_sign
        if signpost is not UNSET:
            field_dict["signpost"] = signpost
        if intersection_name is not UNSET:
            field_dict["intersectionName"] = intersection_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.exit_info import ExitInfo
        from ..models.localized_string import LocalizedString
        from ..models.road_info import RoadInfo
        from ..models.signpost_info import SignpostInfo

        d = dict(src_dict)
        action = ContinueActionAction(d.pop("action"))

        duration = d.pop("duration")

        instruction = d.pop("instruction", UNSET)

        offset = d.pop("offset", UNSET)

        length = d.pop("length", UNSET)

        _current_road = d.pop("currentRoad", UNSET)
        current_road: RoadInfo | Unset
        if isinstance(_current_road, Unset):
            current_road = UNSET
        else:
            current_road = RoadInfo.from_dict(_current_road)

        _next_road = d.pop("nextRoad", UNSET)
        next_road: RoadInfo | Unset
        if isinstance(_next_road, Unset):
            next_road = UNSET
        else:
            next_road = RoadInfo.from_dict(_next_road)

        _exit_sign = d.pop("exitSign", UNSET)
        exit_sign: ExitInfo | Unset
        if isinstance(_exit_sign, Unset):
            exit_sign = UNSET
        else:
            exit_sign = ExitInfo.from_dict(_exit_sign)

        _signpost = d.pop("signpost", UNSET)
        signpost: SignpostInfo | Unset
        if isinstance(_signpost, Unset):
            signpost = UNSET
        else:
            signpost = SignpostInfo.from_dict(_signpost)

        _intersection_name = d.pop("intersectionName", UNSET)
        intersection_name: list[LocalizedString] | Unset = UNSET
        if _intersection_name is not UNSET:
            intersection_name = []
            for intersection_name_item_data in _intersection_name:
                intersection_name_item = LocalizedString.from_dict(
                    intersection_name_item_data
                )

                intersection_name.append(intersection_name_item)

        continue_action = cls(
            action=action,
            duration=duration,
            instruction=instruction,
            offset=offset,
            length=length,
            current_road=current_road,
            next_road=next_road,
            exit_sign=exit_sign,
            signpost=signpost,
            intersection_name=intersection_name,
        )

        continue_action.additional_properties = d
        return continue_action

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
