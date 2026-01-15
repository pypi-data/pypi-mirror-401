from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.localized_route_number_direction import LocalizedRouteNumberDirection
from ..types import UNSET, Unset

T = TypeVar("T", bound="LocalizedRouteNumber")


@_attrs_define
class LocalizedRouteNumber:
    """Represents a route number in specific language with optional cardinal direction and route level.

    Example:
        {'value': 'US-101', 'language': 'en', 'direction': 'south', 'routeType': 1}

    Attributes:
        value (str): String written in the language specified in the language property.
        language (str | Unset): Language in BCP47 format
        direction (LocalizedRouteNumberDirection | Unset): This property indicates the official directional identifier
            assigned to highways. Use direction on sign in conjunction with official name or route number.
            For example, for route guidance, use "US-101 S" and not just "US-101" when appropriate.

            Note that the official direction is not necessarily the travel direction. For example, US-101 through the city
            of Sunnyvale is physically located East to West.
            However, the official direction on sign is North/South.
        route_type (int | Unset): Specifies route type for different route element. These values must be used in
            conjunction with a separate HERE data product: Country Profile Road Signs.
            One of the usage example for this property is it affects how the road shield will be rendered, i.e.
            this route type might change the shape, color and the font of the road shield.
            Related examples for different countries can be found [here](https://en.wikipedia.org/wiki/Highway_shield).
            Possible values are from 1 to 6. But if some countries add extra route type in the future, this range could
            change as well.
    """

    value: str
    language: str | Unset = UNSET
    direction: LocalizedRouteNumberDirection | Unset = UNSET
    route_type: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        language = self.language

        direction: str | Unset = UNSET
        if not isinstance(self.direction, Unset):
            direction = self.direction.value

        route_type = self.route_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "value": value,
        })
        if language is not UNSET:
            field_dict["language"] = language
        if direction is not UNSET:
            field_dict["direction"] = direction
        if route_type is not UNSET:
            field_dict["routeType"] = route_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        language = d.pop("language", UNSET)

        _direction = d.pop("direction", UNSET)
        direction: LocalizedRouteNumberDirection | Unset
        if isinstance(_direction, Unset):
            direction = UNSET
        else:
            direction = LocalizedRouteNumberDirection(_direction)

        route_type = d.pop("routeType", UNSET)

        localized_route_number = cls(
            value=value,
            language=language,
            direction=direction,
            route_type=route_type,
        )

        localized_route_number.additional_properties = d
        return localized_route_number

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
