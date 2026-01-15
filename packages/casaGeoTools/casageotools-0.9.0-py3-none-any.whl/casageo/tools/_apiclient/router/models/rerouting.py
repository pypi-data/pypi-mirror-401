from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.rerouting_mode import ReroutingMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="Rerouting")


@_attrs_define
class Rerouting:
    """Rerouting parameters allow to request a new route calculation based on the route handle.

    All attributes are optional.

        Example:
            {'$ref': '#/components/examples/ReroutingExample'}

        Attributes:
            mode (ReroutingMode | Unset): Defines what kind of additional route calculation should be done.

                * `none` - Cuts off route before the current position. Updates dynamic attributes of the
                route after the current position. If the current position, i.e., the new `origin`, is defined and is
                outside of the original route then the request will fail. If both `origin` and
                `lastTraveledSectionIndex` or `traveledDistanceOnLastSection` are provided then
                `lastTraveledSectionIndex` and `traveledDistanceOnLastSection` will be applied first, and
                then `origin` will be matched to the part of the route that's left. This is the default behavior.
                * `returnToRoute` - Same as `none` if current position is on the route. If the current
                position is not on the original route then a new route to the destination will be
                calculated, starting from the current position. The new route will try to preserve the shape
                of the original route, if possible. If a new optimal route is found before a route back to
                the original route then the new route will be returned.
            last_traveled_section_index (int | Unset): Can be used to indicate the index of the last traveled route section
                on multi-section
                routes. The traveled part of the route won't be reused.

                If the last traveled section is specified and the current position, i.e., the new
                `origin`, is provided, it is expected to be on the last traveled section. If it is
                not on the last traveled section, it is treated as not on the route, triggering
                return to route, if enabled, to the waypoint at the end of the last traveled section.

                If the last traveled section index is not specified, the current position can be
                matched to any section of the route. In this case the route will continue to the
                next waypoint after the current position, i.e., the new `origin`. If the current
                position is not on the route, return to route, if enabled, will by default return
                to the waypoint at the end of the first section.
            traveled_distance_on_last_section (int | Unset): Offset in meter to the last visited position on the route
                section defined by the `lastTraveledSectionIndex`.
                 Default: 0.
    """

    mode: ReroutingMode | Unset = UNSET
    last_traveled_section_index: int | Unset = UNSET
    traveled_distance_on_last_section: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        last_traveled_section_index = self.last_traveled_section_index

        traveled_distance_on_last_section = self.traveled_distance_on_last_section

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mode is not UNSET:
            field_dict["mode"] = mode
        if last_traveled_section_index is not UNSET:
            field_dict["lastTraveledSectionIndex"] = last_traveled_section_index
        if traveled_distance_on_last_section is not UNSET:
            field_dict["traveledDistanceOnLastSection"] = (
                traveled_distance_on_last_section
            )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _mode = d.pop("mode", UNSET)
        mode: ReroutingMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = ReroutingMode(_mode)

        last_traveled_section_index = d.pop("lastTraveledSectionIndex", UNSET)

        traveled_distance_on_last_section = d.pop(
            "traveledDistanceOnLastSection", UNSET
        )

        rerouting = cls(
            mode=mode,
            last_traveled_section_index=last_traveled_section_index,
            traveled_distance_on_last_section=traveled_distance_on_last_section,
        )

        rerouting.additional_properties = d
        return rerouting

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
