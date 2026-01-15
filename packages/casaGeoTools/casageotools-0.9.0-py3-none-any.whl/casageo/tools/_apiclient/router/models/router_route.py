from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.notice import Notice
    from ..models.pedestrian_section import PedestrianSection
    from ..models.route_label import RouteLabel
    from ..models.transit_section import TransitSection
    from ..models.vehicle_section import VehicleSection


T = TypeVar("T", bound="RouterRoute")


@_attrs_define
class RouterRoute:
    """A basic route. Includes personal vehicles as car, truck, etc... For all modes, cf. `transportMode`.

    Attributes:
        id (str): Unique identifier of the route
        sections (list[PedestrianSection | TransitSection | VehicleSection]): An ordered list of vehicle, transit, and
            pedestrian sections making up the route.
        notices (list[Notice] | Unset): Contains a list of issues encountered during the processing of this response.
        route_labels (list[RouteLabel] | Unset): Contains a list of the most important names and route numbers on this
            route that differentiate it from other alternatives.
            These names are used to make labels for the main and alternative routes, like "route1 via A4,D10", "route2 via
            D11,5"
            The generated list is expected to be unique for each route in response (but it's not guaranteed)
        route_handle (str | Unset): Opaque handle of the calculated route.

            A handle encodes the calculated route. The route can be decoded from a handle at a
            later point in time as long as the service uses the same map data which was used
            during encoding.

            To request a handle set the `routeHandle` flag in `return` parameter. If a handle is
            requested, but fails to be calculated for any reason, then the `routeHandle` property is
            not available in the response. The rest of the route is intact.
    """

    id: str
    sections: list[PedestrianSection | TransitSection | VehicleSection]
    notices: list[Notice] | Unset = UNSET
    route_labels: list[RouteLabel] | Unset = UNSET
    route_handle: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.pedestrian_section import PedestrianSection
        from ..models.vehicle_section import VehicleSection

        id = self.id

        sections = []
        for sections_item_data in self.sections:
            sections_item: dict[str, Any]
            if isinstance(sections_item_data, VehicleSection):
                sections_item = sections_item_data.to_dict()
            elif isinstance(sections_item_data, PedestrianSection):
                sections_item = sections_item_data.to_dict()
            else:
                sections_item = sections_item_data.to_dict()

            sections.append(sections_item)

        notices: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.notices, Unset):
            notices = []
            for notices_item_data in self.notices:
                notices_item = notices_item_data.to_dict()
                notices.append(notices_item)

        route_labels: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.route_labels, Unset):
            route_labels = []
            for route_labels_item_data in self.route_labels:
                route_labels_item = route_labels_item_data.to_dict()
                route_labels.append(route_labels_item)

        route_handle = self.route_handle

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "sections": sections,
        })
        if notices is not UNSET:
            field_dict["notices"] = notices
        if route_labels is not UNSET:
            field_dict["routeLabels"] = route_labels
        if route_handle is not UNSET:
            field_dict["routeHandle"] = route_handle

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.notice import Notice
        from ..models.pedestrian_section import PedestrianSection
        from ..models.route_label import RouteLabel
        from ..models.transit_section import TransitSection
        from ..models.vehicle_section import VehicleSection

        d = dict(src_dict)
        id = d.pop("id")

        sections = []
        _sections = d.pop("sections")
        for sections_item_data in _sections:

            def _parse_sections_item(
                data: object,
            ) -> PedestrianSection | TransitSection | VehicleSection:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_router_section_type_0 = VehicleSection.from_dict(
                        data
                    )

                    return componentsschemas_router_section_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_router_section_type_1 = (
                        PedestrianSection.from_dict(data)
                    )

                    return componentsschemas_router_section_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_router_section_type_2 = TransitSection.from_dict(data)

                return componentsschemas_router_section_type_2

            sections_item = _parse_sections_item(sections_item_data)

            sections.append(sections_item)

        _notices = d.pop("notices", UNSET)
        notices: list[Notice] | Unset = UNSET
        if _notices is not UNSET:
            notices = []
            for notices_item_data in _notices:
                notices_item = Notice.from_dict(notices_item_data)

                notices.append(notices_item)

        _route_labels = d.pop("routeLabels", UNSET)
        route_labels: list[RouteLabel] | Unset = UNSET
        if _route_labels is not UNSET:
            route_labels = []
            for route_labels_item_data in _route_labels:
                route_labels_item = RouteLabel.from_dict(route_labels_item_data)

                route_labels.append(route_labels_item)

        route_handle = d.pop("routeHandle", UNSET)

        router_route = cls(
            id=id,
            sections=sections,
            notices=notices,
            route_labels=route_labels,
            route_handle=route_handle,
        )

        router_route.additional_properties = d
        return router_route

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
