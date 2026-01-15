from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.localized_route_number import LocalizedRouteNumber


T = TypeVar("T", bound="SignpostLabelRouteNumber")


@_attrs_define
class SignpostLabelRouteNumber:
    """Route number on a signpost label. The `routeType` property of the LocalizedRouteNumber is always null at the moment
    for SignpostLabel, because the data is currently not available.

        Attributes:
            route_number (LocalizedRouteNumber | Unset): Represents a route number in specific language with optional
                cardinal direction and route level. Example: {'value': 'US-101', 'language': 'en', 'direction': 'south',
                'routeType': 1}.
    """

    route_number: LocalizedRouteNumber | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        route_number: dict[str, Any] | Unset = UNSET
        if not isinstance(self.route_number, Unset):
            route_number = self.route_number.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if route_number is not UNSET:
            field_dict["routeNumber"] = route_number

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.localized_route_number import LocalizedRouteNumber

        d = dict(src_dict)
        _route_number = d.pop("routeNumber", UNSET)
        route_number: LocalizedRouteNumber | Unset
        if isinstance(_route_number, Unset):
            route_number = UNSET
        else:
            route_number = LocalizedRouteNumber.from_dict(_route_number)

        signpost_label_route_number = cls(
            route_number=route_number,
        )

        signpost_label_route_number.additional_properties = d
        return signpost_label_route_number

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
