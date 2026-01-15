from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.route_response_notice import RouteResponseNotice
    from ..models.router_route import RouterRoute


T = TypeVar("T", bound="RouterRouteResponse")


@_attrs_define
class RouterRouteResponse:
    """Returns a list of routes.

    Attributes:
        routes (list[RouterRoute]): List of possible routes
        notices (list[RouteResponseNotice] | Unset): Contains a list of issues related to this route calculation.
            Please refer to the `code` attribute for possible values.
    """

    routes: list[RouterRoute]
    notices: list[RouteResponseNotice] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        routes = []
        for routes_item_data in self.routes:
            routes_item = routes_item_data.to_dict()
            routes.append(routes_item)

        notices: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.notices, Unset):
            notices = []
            for notices_item_data in self.notices:
                notices_item = notices_item_data.to_dict()
                notices.append(notices_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "routes": routes,
        })
        if notices is not UNSET:
            field_dict["notices"] = notices

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.route_response_notice import RouteResponseNotice
        from ..models.router_route import RouterRoute

        d = dict(src_dict)
        routes = []
        _routes = d.pop("routes")
        for routes_item_data in _routes:
            routes_item = RouterRoute.from_dict(routes_item_data)

            routes.append(routes_item)

        _notices = d.pop("notices", UNSET)
        notices: list[RouteResponseNotice] | Unset = UNSET
        if _notices is not UNSET:
            notices = []
            for notices_item_data in _notices:
                notices_item = RouteResponseNotice.from_dict(notices_item_data)

                notices.append(notices_item)

        router_route_response = cls(
            routes=routes,
            notices=notices,
        )

        router_route_response.additional_properties = d
        return router_route_response

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
