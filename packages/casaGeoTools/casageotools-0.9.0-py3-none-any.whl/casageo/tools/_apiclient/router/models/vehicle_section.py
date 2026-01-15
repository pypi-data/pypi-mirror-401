from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vehicle_section_type import VehicleSectionType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.arrive_action import ArriveAction
    from ..models.base_action import BaseAction
    from ..models.charging_action import ChargingAction
    from ..models.charging_setup_action import ChargingSetupAction
    from ..models.continue_action import ContinueAction
    from ..models.deboard_action import DeboardAction
    from ..models.depart_action import DepartAction
    from ..models.exit_action import ExitAction
    from ..models.passthrough import Passthrough
    from ..models.ref_replacements import RefReplacements
    from ..models.routing_zone import RoutingZone
    from ..models.toll_cost import TollCost
    from ..models.toll_system import TollSystem
    from ..models.traffic_incident import TrafficIncident
    from ..models.turn_action import TurnAction
    from ..models.vehicle_departure import VehicleDeparture
    from ..models.vehicle_notice import VehicleNotice
    from ..models.vehicle_restriction import VehicleRestriction
    from ..models.vehicle_span import VehicleSpan
    from ..models.vehicle_summary import VehicleSummary
    from ..models.vehicle_transport import VehicleTransport
    from ..models.vehicle_travel_summary import VehicleTravelSummary
    from ..models.wait_action import WaitAction


T = TypeVar("T", bound="VehicleSection")


@_attrs_define
class VehicleSection:
    """Represent a section of a route

    Attributes:
        id (str): Unique identifier of the section
        type_ (VehicleSectionType): Section type used by the client to identify what extension to the BaseSection are
            available.
        departure (VehicleDeparture): Describe a departure or arrival location and time.
        arrival (VehicleDeparture): Describe a departure or arrival location and time.
        transport (VehicleTransport): Information about a transport
        pre_actions (list[BaseAction] | Unset): Actions that must be done prior to `departure`.
        actions (list[ArriveAction | ContinueAction | DepartAction | ExitAction | TurnAction] | Unset): Actions to be
            performed at or during a specific portion of a section.

            Action offsets represent the coordinate index in the polyline.

            *NOTE:* The following attributes are valid for turnByTurnActions only and are not populated for actions
              * currentRoad
              * nextRoad
              * exitSign
              * signPost
              * intersectionName
              * turnAngle
        language (str | Unset): Language of the localized strings in the section, if any, in BCP47 format.
        post_actions (list[ChargingAction | ChargingSetupAction | DeboardAction | WaitAction] | Unset): Actions that
            must be done after `arrival`.
        turn_by_turn_actions (list[ArriveAction | ContinueAction | DepartAction | ExitAction | TurnAction] | Unset):
            Turn-by-turn guidance actions.

            Action offsets represent the coordinate index in the polyline.
        passthrough (list[Passthrough] | Unset): List of via waypoints this section is passing through.

            Each via waypoint of the request that is a `passThrough=true` waypoint, appears as a
            `Passthrough` in the response. It appears in the section that starts with the closest
            non-passthrough via specified before it or origin.

            The passthrough vias appear in this list in the order they are traversed. They are
            traversed in the order they are specified in the request.
        summary (VehicleSummary | Unset): Total value of key attributes for a route section.
        travel_summary (VehicleTravelSummary | Unset): Total value of key attributes for a route section.
        polyline (str | Unset): Line string in [Flexible Polyline](https://github.com/heremaps/flexible-polyline)
            format. Coordinates are in the WGS84 coordinate system, including `Elevation` (if present). Example:
            A05xgKuy2xCx9B7vUl0OhnR54EqSzpEl-HxjD3pBiGnyGi2CvwFsgD3nD4vB6e.
        notices (list[VehicleNotice] | Unset): Contains a list of issues related to this section of the route.

            Notices must be carefully evaluated and, if deemed necessary, the route section should be discarded accordingly.
            In particular, the user should be aware that new notice codes may be added at any time. If an unrecognized
            notice code appears with a `critical` severity level, the route section must be discarded.
            Please refer to the `code` attribute for possible values.
        spans (list[VehicleSpan] | Unset): Spans attached to a `Section` describing vehicle content.
        routing_zones (list[RoutingZone] | Unset): A list of routing zones that are applicable to the section.

            Elements of this list will be referenced by indexes within the `span` attribute of the section.
        truck_road_types (list[str] | Unset): A list of truck road types that are applicable to the section.

            Elements of this list will be referenced by indexes within the `span` attribute of the section.

            A truck road type is an identifier associated with roads that have additional regulations applied by local
            administration for
            traversal by heavy vehicles like trucks. For example, the BK Bearing Class regulations in Sweden, and ET
            categories in Mexico.
            The identifiers of supported truck road types are specified at HERE Map Content
            [TruckRoadType](https://www.here.com/docs/bundle/map-content-schema-data-
            specification/page/topics_schema/truckroadtypeattribute.html).

            These names should be provided when avoiding a certain truck road type.
        incidents (list[TrafficIncident] | Unset): A list of all incidents that apply to the section.
        ref_replacements (RefReplacements | Unset): Dictionary of placeholders to replacement strings for the compact
            representation of map entity references.
        toll_systems (list[TollSystem] | Unset): An array of toll authorities that collect payments for the use of (part
            of) the specified section of the route.
        tolls (list[TollCost] | Unset): Detail of tolls to be paid for traversing the specified section.
        consumption_type (str | Unset): Extensible enum: `electric` `diesel` `petrol` `lpg` `cng` `lng` `ethanol`
            `propane` `hydrogen` `...`
            Vehicle consumption type. The energy or fuel consumption type (electric, diesel, petrol, lpg, cng, etc.)
            of a vehicle which provides the relevant information required to parse (unit, etc.) the energy or fuel
            `consumption` value of a vehicle.
        no_through_restrictions (list[VehicleRestriction] | Unset): A list of all rules that restrict movement through
            the area without there being an
            origin, destination, or `via` waypoint inside of it. Only restrictions applicable
            to the vehicle for which the route was requested are returned.
    """

    id: str
    type_: VehicleSectionType
    departure: VehicleDeparture
    arrival: VehicleDeparture
    transport: VehicleTransport
    pre_actions: list[BaseAction] | Unset = UNSET
    actions: (
        list[ArriveAction | ContinueAction | DepartAction | ExitAction | TurnAction]
        | Unset
    ) = UNSET
    language: str | Unset = UNSET
    post_actions: (
        list[ChargingAction | ChargingSetupAction | DeboardAction | WaitAction] | Unset
    ) = UNSET
    turn_by_turn_actions: (
        list[ArriveAction | ContinueAction | DepartAction | ExitAction | TurnAction]
        | Unset
    ) = UNSET
    passthrough: list[Passthrough] | Unset = UNSET
    summary: VehicleSummary | Unset = UNSET
    travel_summary: VehicleTravelSummary | Unset = UNSET
    polyline: str | Unset = UNSET
    notices: list[VehicleNotice] | Unset = UNSET
    spans: list[VehicleSpan] | Unset = UNSET
    routing_zones: list[RoutingZone] | Unset = UNSET
    truck_road_types: list[str] | Unset = UNSET
    incidents: list[TrafficIncident] | Unset = UNSET
    ref_replacements: RefReplacements | Unset = UNSET
    toll_systems: list[TollSystem] | Unset = UNSET
    tolls: list[TollCost] | Unset = UNSET
    consumption_type: str | Unset = UNSET
    no_through_restrictions: list[VehicleRestriction] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.arrive_action import ArriveAction
        from ..models.charging_action import ChargingAction
        from ..models.charging_setup_action import ChargingSetupAction
        from ..models.continue_action import ContinueAction
        from ..models.deboard_action import DeboardAction
        from ..models.depart_action import DepartAction
        from ..models.exit_action import ExitAction

        id = self.id

        type_ = self.type_.value

        departure = self.departure.to_dict()

        arrival = self.arrival.to_dict()

        transport = self.transport.to_dict()

        pre_actions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.pre_actions, Unset):
            pre_actions = []
            for pre_actions_item_data in self.pre_actions:
                pre_actions_item = pre_actions_item_data.to_dict()
                pre_actions.append(pre_actions_item)

        actions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.actions, Unset):
            actions = []
            for actions_item_data in self.actions:
                actions_item: dict[str, Any]
                if isinstance(actions_item_data, DepartAction):
                    actions_item = actions_item_data.to_dict()
                elif isinstance(actions_item_data, ArriveAction):
                    actions_item = actions_item_data.to_dict()
                elif isinstance(actions_item_data, ContinueAction):
                    actions_item = actions_item_data.to_dict()
                elif isinstance(actions_item_data, ExitAction):
                    actions_item = actions_item_data.to_dict()
                else:
                    actions_item = actions_item_data.to_dict()

                actions.append(actions_item)

        language = self.language

        post_actions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.post_actions, Unset):
            post_actions = []
            for post_actions_item_data in self.post_actions:
                post_actions_item: dict[str, Any]
                if isinstance(post_actions_item_data, ChargingSetupAction):
                    post_actions_item = post_actions_item_data.to_dict()
                elif isinstance(post_actions_item_data, ChargingAction):
                    post_actions_item = post_actions_item_data.to_dict()
                elif isinstance(post_actions_item_data, DeboardAction):
                    post_actions_item = post_actions_item_data.to_dict()
                else:
                    post_actions_item = post_actions_item_data.to_dict()

                post_actions.append(post_actions_item)

        turn_by_turn_actions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.turn_by_turn_actions, Unset):
            turn_by_turn_actions = []
            for turn_by_turn_actions_item_data in self.turn_by_turn_actions:
                turn_by_turn_actions_item: dict[str, Any]
                if isinstance(turn_by_turn_actions_item_data, DepartAction):
                    turn_by_turn_actions_item = turn_by_turn_actions_item_data.to_dict()
                elif isinstance(turn_by_turn_actions_item_data, ArriveAction):
                    turn_by_turn_actions_item = turn_by_turn_actions_item_data.to_dict()
                elif isinstance(turn_by_turn_actions_item_data, ContinueAction):
                    turn_by_turn_actions_item = turn_by_turn_actions_item_data.to_dict()
                elif isinstance(turn_by_turn_actions_item_data, ExitAction):
                    turn_by_turn_actions_item = turn_by_turn_actions_item_data.to_dict()
                else:
                    turn_by_turn_actions_item = turn_by_turn_actions_item_data.to_dict()

                turn_by_turn_actions.append(turn_by_turn_actions_item)

        passthrough: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.passthrough, Unset):
            passthrough = []
            for passthrough_item_data in self.passthrough:
                passthrough_item = passthrough_item_data.to_dict()
                passthrough.append(passthrough_item)

        summary: dict[str, Any] | Unset = UNSET
        if not isinstance(self.summary, Unset):
            summary = self.summary.to_dict()

        travel_summary: dict[str, Any] | Unset = UNSET
        if not isinstance(self.travel_summary, Unset):
            travel_summary = self.travel_summary.to_dict()

        polyline = self.polyline

        notices: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.notices, Unset):
            notices = []
            for notices_item_data in self.notices:
                notices_item = notices_item_data.to_dict()
                notices.append(notices_item)

        spans: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.spans, Unset):
            spans = []
            for spans_item_data in self.spans:
                spans_item = spans_item_data.to_dict()
                spans.append(spans_item)

        routing_zones: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.routing_zones, Unset):
            routing_zones = []
            for routing_zones_item_data in self.routing_zones:
                routing_zones_item = routing_zones_item_data.to_dict()
                routing_zones.append(routing_zones_item)

        truck_road_types: list[str] | Unset = UNSET
        if not isinstance(self.truck_road_types, Unset):
            truck_road_types = self.truck_road_types

        incidents: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.incidents, Unset):
            incidents = []
            for incidents_item_data in self.incidents:
                incidents_item = incidents_item_data.to_dict()
                incidents.append(incidents_item)

        ref_replacements: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ref_replacements, Unset):
            ref_replacements = self.ref_replacements.to_dict()

        toll_systems: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.toll_systems, Unset):
            toll_systems = []
            for toll_systems_item_data in self.toll_systems:
                toll_systems_item = toll_systems_item_data.to_dict()
                toll_systems.append(toll_systems_item)

        tolls: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tolls, Unset):
            tolls = []
            for tolls_item_data in self.tolls:
                tolls_item = tolls_item_data.to_dict()
                tolls.append(tolls_item)

        consumption_type = self.consumption_type

        no_through_restrictions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.no_through_restrictions, Unset):
            no_through_restrictions = []
            for no_through_restrictions_item_data in self.no_through_restrictions:
                no_through_restrictions_item = (
                    no_through_restrictions_item_data.to_dict()
                )
                no_through_restrictions.append(no_through_restrictions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "type": type_,
            "departure": departure,
            "arrival": arrival,
            "transport": transport,
        })
        if pre_actions is not UNSET:
            field_dict["preActions"] = pre_actions
        if actions is not UNSET:
            field_dict["actions"] = actions
        if language is not UNSET:
            field_dict["language"] = language
        if post_actions is not UNSET:
            field_dict["postActions"] = post_actions
        if turn_by_turn_actions is not UNSET:
            field_dict["turnByTurnActions"] = turn_by_turn_actions
        if passthrough is not UNSET:
            field_dict["passthrough"] = passthrough
        if summary is not UNSET:
            field_dict["summary"] = summary
        if travel_summary is not UNSET:
            field_dict["travelSummary"] = travel_summary
        if polyline is not UNSET:
            field_dict["polyline"] = polyline
        if notices is not UNSET:
            field_dict["notices"] = notices
        if spans is not UNSET:
            field_dict["spans"] = spans
        if routing_zones is not UNSET:
            field_dict["routingZones"] = routing_zones
        if truck_road_types is not UNSET:
            field_dict["truckRoadTypes"] = truck_road_types
        if incidents is not UNSET:
            field_dict["incidents"] = incidents
        if ref_replacements is not UNSET:
            field_dict["refReplacements"] = ref_replacements
        if toll_systems is not UNSET:
            field_dict["tollSystems"] = toll_systems
        if tolls is not UNSET:
            field_dict["tolls"] = tolls
        if consumption_type is not UNSET:
            field_dict["consumptionType"] = consumption_type
        if no_through_restrictions is not UNSET:
            field_dict["noThroughRestrictions"] = no_through_restrictions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.arrive_action import ArriveAction
        from ..models.base_action import BaseAction
        from ..models.charging_action import ChargingAction
        from ..models.charging_setup_action import ChargingSetupAction
        from ..models.continue_action import ContinueAction
        from ..models.deboard_action import DeboardAction
        from ..models.depart_action import DepartAction
        from ..models.exit_action import ExitAction
        from ..models.passthrough import Passthrough
        from ..models.ref_replacements import RefReplacements
        from ..models.routing_zone import RoutingZone
        from ..models.toll_cost import TollCost
        from ..models.toll_system import TollSystem
        from ..models.traffic_incident import TrafficIncident
        from ..models.turn_action import TurnAction
        from ..models.vehicle_departure import VehicleDeparture
        from ..models.vehicle_notice import VehicleNotice
        from ..models.vehicle_restriction import VehicleRestriction
        from ..models.vehicle_span import VehicleSpan
        from ..models.vehicle_summary import VehicleSummary
        from ..models.vehicle_transport import VehicleTransport
        from ..models.vehicle_travel_summary import VehicleTravelSummary
        from ..models.wait_action import WaitAction

        d = dict(src_dict)
        id = d.pop("id")

        type_ = VehicleSectionType(d.pop("type"))

        departure = VehicleDeparture.from_dict(d.pop("departure"))

        arrival = VehicleDeparture.from_dict(d.pop("arrival"))

        transport = VehicleTransport.from_dict(d.pop("transport"))

        _pre_actions = d.pop("preActions", UNSET)
        pre_actions: list[BaseAction] | Unset = UNSET
        if _pre_actions is not UNSET:
            pre_actions = []
            for pre_actions_item_data in _pre_actions:
                pre_actions_item = BaseAction.from_dict(pre_actions_item_data)

                pre_actions.append(pre_actions_item)

        _actions = d.pop("actions", UNSET)
        actions: (
            list[ArriveAction | ContinueAction | DepartAction | ExitAction | TurnAction]
            | Unset
        ) = UNSET
        if _actions is not UNSET:
            actions = []
            for actions_item_data in _actions:

                def _parse_actions_item(
                    data: object,
                ) -> (
                    ArriveAction
                    | ContinueAction
                    | DepartAction
                    | ExitAction
                    | TurnAction
                ):
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_vehicle_action_type_0 = (
                            DepartAction.from_dict(data)
                        )

                        return componentsschemas_vehicle_action_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_vehicle_action_type_1 = (
                            ArriveAction.from_dict(data)
                        )

                        return componentsschemas_vehicle_action_type_1
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_vehicle_action_type_2 = (
                            ContinueAction.from_dict(data)
                        )

                        return componentsschemas_vehicle_action_type_2
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_vehicle_action_type_3 = ExitAction.from_dict(
                            data
                        )

                        return componentsschemas_vehicle_action_type_3
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_vehicle_action_type_4 = TurnAction.from_dict(data)

                    return componentsschemas_vehicle_action_type_4

                actions_item = _parse_actions_item(actions_item_data)

                actions.append(actions_item)

        language = d.pop("language", UNSET)

        _post_actions = d.pop("postActions", UNSET)
        post_actions: (
            list[ChargingAction | ChargingSetupAction | DeboardAction | WaitAction]
            | Unset
        ) = UNSET
        if _post_actions is not UNSET:
            post_actions = []
            for post_actions_item_data in _post_actions:

                def _parse_post_actions_item(
                    data: object,
                ) -> ChargingAction | ChargingSetupAction | DeboardAction | WaitAction:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_vehicle_post_action_type_0 = (
                            ChargingSetupAction.from_dict(data)
                        )

                        return componentsschemas_vehicle_post_action_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_vehicle_post_action_type_1 = (
                            ChargingAction.from_dict(data)
                        )

                        return componentsschemas_vehicle_post_action_type_1
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_vehicle_post_action_type_2 = (
                            DeboardAction.from_dict(data)
                        )

                        return componentsschemas_vehicle_post_action_type_2
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_vehicle_post_action_type_3 = WaitAction.from_dict(
                        data
                    )

                    return componentsschemas_vehicle_post_action_type_3

                post_actions_item = _parse_post_actions_item(post_actions_item_data)

                post_actions.append(post_actions_item)

        _turn_by_turn_actions = d.pop("turnByTurnActions", UNSET)
        turn_by_turn_actions: (
            list[ArriveAction | ContinueAction | DepartAction | ExitAction | TurnAction]
            | Unset
        ) = UNSET
        if _turn_by_turn_actions is not UNSET:
            turn_by_turn_actions = []
            for turn_by_turn_actions_item_data in _turn_by_turn_actions:

                def _parse_turn_by_turn_actions_item(
                    data: object,
                ) -> (
                    ArriveAction
                    | ContinueAction
                    | DepartAction
                    | ExitAction
                    | TurnAction
                ):
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_vehicle_action_type_0 = (
                            DepartAction.from_dict(data)
                        )

                        return componentsschemas_vehicle_action_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_vehicle_action_type_1 = (
                            ArriveAction.from_dict(data)
                        )

                        return componentsschemas_vehicle_action_type_1
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_vehicle_action_type_2 = (
                            ContinueAction.from_dict(data)
                        )

                        return componentsschemas_vehicle_action_type_2
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_vehicle_action_type_3 = ExitAction.from_dict(
                            data
                        )

                        return componentsschemas_vehicle_action_type_3
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_vehicle_action_type_4 = TurnAction.from_dict(data)

                    return componentsschemas_vehicle_action_type_4

                turn_by_turn_actions_item = _parse_turn_by_turn_actions_item(
                    turn_by_turn_actions_item_data
                )

                turn_by_turn_actions.append(turn_by_turn_actions_item)

        _passthrough = d.pop("passthrough", UNSET)
        passthrough: list[Passthrough] | Unset = UNSET
        if _passthrough is not UNSET:
            passthrough = []
            for passthrough_item_data in _passthrough:
                passthrough_item = Passthrough.from_dict(passthrough_item_data)

                passthrough.append(passthrough_item)

        _summary = d.pop("summary", UNSET)
        summary: VehicleSummary | Unset
        if isinstance(_summary, Unset):
            summary = UNSET
        else:
            summary = VehicleSummary.from_dict(_summary)

        _travel_summary = d.pop("travelSummary", UNSET)
        travel_summary: VehicleTravelSummary | Unset
        if isinstance(_travel_summary, Unset):
            travel_summary = UNSET
        else:
            travel_summary = VehicleTravelSummary.from_dict(_travel_summary)

        polyline = d.pop("polyline", UNSET)

        _notices = d.pop("notices", UNSET)
        notices: list[VehicleNotice] | Unset = UNSET
        if _notices is not UNSET:
            notices = []
            for notices_item_data in _notices:
                notices_item = VehicleNotice.from_dict(notices_item_data)

                notices.append(notices_item)

        _spans = d.pop("spans", UNSET)
        spans: list[VehicleSpan] | Unset = UNSET
        if _spans is not UNSET:
            spans = []
            for spans_item_data in _spans:
                spans_item = VehicleSpan.from_dict(spans_item_data)

                spans.append(spans_item)

        _routing_zones = d.pop("routingZones", UNSET)
        routing_zones: list[RoutingZone] | Unset = UNSET
        if _routing_zones is not UNSET:
            routing_zones = []
            for routing_zones_item_data in _routing_zones:
                routing_zones_item = RoutingZone.from_dict(routing_zones_item_data)

                routing_zones.append(routing_zones_item)

        truck_road_types = cast(list[str], d.pop("truckRoadTypes", UNSET))

        _incidents = d.pop("incidents", UNSET)
        incidents: list[TrafficIncident] | Unset = UNSET
        if _incidents is not UNSET:
            incidents = []
            for incidents_item_data in _incidents:
                incidents_item = TrafficIncident.from_dict(incidents_item_data)

                incidents.append(incidents_item)

        _ref_replacements = d.pop("refReplacements", UNSET)
        ref_replacements: RefReplacements | Unset
        if isinstance(_ref_replacements, Unset):
            ref_replacements = UNSET
        else:
            ref_replacements = RefReplacements.from_dict(_ref_replacements)

        _toll_systems = d.pop("tollSystems", UNSET)
        toll_systems: list[TollSystem] | Unset = UNSET
        if _toll_systems is not UNSET:
            toll_systems = []
            for toll_systems_item_data in _toll_systems:
                toll_systems_item = TollSystem.from_dict(toll_systems_item_data)

                toll_systems.append(toll_systems_item)

        _tolls = d.pop("tolls", UNSET)
        tolls: list[TollCost] | Unset = UNSET
        if _tolls is not UNSET:
            tolls = []
            for tolls_item_data in _tolls:
                tolls_item = TollCost.from_dict(tolls_item_data)

                tolls.append(tolls_item)

        consumption_type = d.pop("consumptionType", UNSET)

        _no_through_restrictions = d.pop("noThroughRestrictions", UNSET)
        no_through_restrictions: list[VehicleRestriction] | Unset = UNSET
        if _no_through_restrictions is not UNSET:
            no_through_restrictions = []
            for no_through_restrictions_item_data in _no_through_restrictions:
                no_through_restrictions_item = VehicleRestriction.from_dict(
                    no_through_restrictions_item_data
                )

                no_through_restrictions.append(no_through_restrictions_item)

        vehicle_section = cls(
            id=id,
            type_=type_,
            departure=departure,
            arrival=arrival,
            transport=transport,
            pre_actions=pre_actions,
            actions=actions,
            language=language,
            post_actions=post_actions,
            turn_by_turn_actions=turn_by_turn_actions,
            passthrough=passthrough,
            summary=summary,
            travel_summary=travel_summary,
            polyline=polyline,
            notices=notices,
            spans=spans,
            routing_zones=routing_zones,
            truck_road_types=truck_road_types,
            incidents=incidents,
            ref_replacements=ref_replacements,
            toll_systems=toll_systems,
            tolls=tolls,
            consumption_type=consumption_type,
            no_through_restrictions=no_through_restrictions,
        )

        vehicle_section.additional_properties = d
        return vehicle_section

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
