from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.pedestrian_section_type import PedestrianSectionType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.arrive_action import ArriveAction
    from ..models.base_action import BaseAction
    from ..models.base_summary import BaseSummary
    from ..models.continue_action import ContinueAction
    from ..models.deboard_action import DeboardAction
    from ..models.depart_action import DepartAction
    from ..models.exit_action import ExitAction
    from ..models.offset_action import OffsetAction
    from ..models.passthrough import Passthrough
    from ..models.pedestrian_departure import PedestrianDeparture
    from ..models.pedestrian_notice import PedestrianNotice
    from ..models.pedestrian_span import PedestrianSpan
    from ..models.pedestrian_summary import PedestrianSummary
    from ..models.pedestrian_transport import PedestrianTransport
    from ..models.ref_replacements import RefReplacements
    from ..models.simple_turn_action import SimpleTurnAction
    from ..models.wait_action import WaitAction


T = TypeVar("T", bound="PedestrianSection")


@_attrs_define
class PedestrianSection:
    """Represent a section of a route

    Attributes:
        id (str): Unique identifier of the section
        type_ (PedestrianSectionType): Section type used by the client to identify what extension to the BaseSection are
            available.
        departure (PedestrianDeparture): Departure of pedestrian
        arrival (PedestrianDeparture): Departure of pedestrian
        transport (PedestrianTransport): Information about a transport
        pre_actions (list[BaseAction] | Unset): Actions that must be done prior to `departure`.
        actions (list[ArriveAction | ContinueAction | DepartAction | ExitAction | SimpleTurnAction] | Unset): Actions to
            be performed at or during a specific portion of a section.

            Action offsets are the coordinate index in the polyline.

            *NOTE:* currentRoad and nextRoad are not populated for actions.
        language (str | Unset): Language of the localized strings in the section, if any, in BCP47 format.
        post_actions (list[DeboardAction | WaitAction] | Unset): Actions that must be done after `arrival`.
        turn_by_turn_actions (list[OffsetAction] | Unset): Actions for turn by turn guidance during the travel portion
            of the section, i.e., between `departure` and `arrival`.
        passthrough (list[Passthrough] | Unset): List of via waypoints this section is passing through.

            Each via waypoint of the request that is a `passThrough=true` waypoint, appears as a
            `Passthrough` in the response. It appears in the section that starts with the closest
            non-passthrough via specified before it or origin.

            The passthrough vias appear in this list in the order they are traversed. They are
            traversed in the order they are specified in the request.
        summary (PedestrianSummary | Unset): Total value of key attributes for a route section.
        travel_summary (BaseSummary | Unset): Total value of key attributes for a route section.
        polyline (str | Unset): Line string in [Flexible Polyline](https://github.com/heremaps/flexible-polyline)
            format. Coordinates are in the WGS84 coordinate system, including `Elevation` (if present). Example:
            A05xgKuy2xCx9B7vUl0OhnR54EqSzpEl-HxjD3pBiGnyGi2CvwFsgD3nD4vB6e.
        notices (list[PedestrianNotice] | Unset): Contains a list of issues related to this section of the route.
        spans (list[PedestrianSpan] | Unset): Spans attached to a `Section` describing pedestrian content.
        ref_replacements (RefReplacements | Unset): Dictionary of placeholders to replacement strings for the compact
            representation of map entity references.
    """

    id: str
    type_: PedestrianSectionType
    departure: PedestrianDeparture
    arrival: PedestrianDeparture
    transport: PedestrianTransport
    pre_actions: list[BaseAction] | Unset = UNSET
    actions: (
        list[
            ArriveAction | ContinueAction | DepartAction | ExitAction | SimpleTurnAction
        ]
        | Unset
    ) = UNSET
    language: str | Unset = UNSET
    post_actions: list[DeboardAction | WaitAction] | Unset = UNSET
    turn_by_turn_actions: list[OffsetAction] | Unset = UNSET
    passthrough: list[Passthrough] | Unset = UNSET
    summary: PedestrianSummary | Unset = UNSET
    travel_summary: BaseSummary | Unset = UNSET
    polyline: str | Unset = UNSET
    notices: list[PedestrianNotice] | Unset = UNSET
    spans: list[PedestrianSpan] | Unset = UNSET
    ref_replacements: RefReplacements | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.arrive_action import ArriveAction
        from ..models.continue_action import ContinueAction
        from ..models.depart_action import DepartAction
        from ..models.exit_action import ExitAction
        from ..models.wait_action import WaitAction

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
                if isinstance(post_actions_item_data, WaitAction):
                    post_actions_item = post_actions_item_data.to_dict()
                else:
                    post_actions_item = post_actions_item_data.to_dict()

                post_actions.append(post_actions_item)

        turn_by_turn_actions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.turn_by_turn_actions, Unset):
            turn_by_turn_actions = []
            for turn_by_turn_actions_item_data in self.turn_by_turn_actions:
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

        ref_replacements: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ref_replacements, Unset):
            ref_replacements = self.ref_replacements.to_dict()

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
        if ref_replacements is not UNSET:
            field_dict["refReplacements"] = ref_replacements

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.arrive_action import ArriveAction
        from ..models.base_action import BaseAction
        from ..models.base_summary import BaseSummary
        from ..models.continue_action import ContinueAction
        from ..models.deboard_action import DeboardAction
        from ..models.depart_action import DepartAction
        from ..models.exit_action import ExitAction
        from ..models.offset_action import OffsetAction
        from ..models.passthrough import Passthrough
        from ..models.pedestrian_departure import PedestrianDeparture
        from ..models.pedestrian_notice import PedestrianNotice
        from ..models.pedestrian_span import PedestrianSpan
        from ..models.pedestrian_summary import PedestrianSummary
        from ..models.pedestrian_transport import PedestrianTransport
        from ..models.ref_replacements import RefReplacements
        from ..models.simple_turn_action import SimpleTurnAction
        from ..models.wait_action import WaitAction

        d = dict(src_dict)
        id = d.pop("id")

        type_ = PedestrianSectionType(d.pop("type"))

        departure = PedestrianDeparture.from_dict(d.pop("departure"))

        arrival = PedestrianDeparture.from_dict(d.pop("arrival"))

        transport = PedestrianTransport.from_dict(d.pop("transport"))

        _pre_actions = d.pop("preActions", UNSET)
        pre_actions: list[BaseAction] | Unset = UNSET
        if _pre_actions is not UNSET:
            pre_actions = []
            for pre_actions_item_data in _pre_actions:
                pre_actions_item = BaseAction.from_dict(pre_actions_item_data)

                pre_actions.append(pre_actions_item)

        _actions = d.pop("actions", UNSET)
        actions: (
            list[
                ArriveAction
                | ContinueAction
                | DepartAction
                | ExitAction
                | SimpleTurnAction
            ]
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
                    | SimpleTurnAction
                ):
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_pedestrian_action_type_0 = (
                            DepartAction.from_dict(data)
                        )

                        return componentsschemas_pedestrian_action_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_pedestrian_action_type_1 = (
                            ArriveAction.from_dict(data)
                        )

                        return componentsschemas_pedestrian_action_type_1
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_pedestrian_action_type_2 = (
                            ContinueAction.from_dict(data)
                        )

                        return componentsschemas_pedestrian_action_type_2
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_pedestrian_action_type_3 = (
                            ExitAction.from_dict(data)
                        )

                        return componentsschemas_pedestrian_action_type_3
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_pedestrian_action_type_4 = (
                        SimpleTurnAction.from_dict(data)
                    )

                    return componentsschemas_pedestrian_action_type_4

                actions_item = _parse_actions_item(actions_item_data)

                actions.append(actions_item)

        language = d.pop("language", UNSET)

        _post_actions = d.pop("postActions", UNSET)
        post_actions: list[DeboardAction | WaitAction] | Unset = UNSET
        if _post_actions is not UNSET:
            post_actions = []
            for post_actions_item_data in _post_actions:

                def _parse_post_actions_item(
                    data: object,
                ) -> DeboardAction | WaitAction:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_pedestrian_post_action_type_0 = (
                            WaitAction.from_dict(data)
                        )

                        return componentsschemas_pedestrian_post_action_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_pedestrian_post_action_type_1 = (
                        DeboardAction.from_dict(data)
                    )

                    return componentsschemas_pedestrian_post_action_type_1

                post_actions_item = _parse_post_actions_item(post_actions_item_data)

                post_actions.append(post_actions_item)

        _turn_by_turn_actions = d.pop("turnByTurnActions", UNSET)
        turn_by_turn_actions: list[OffsetAction] | Unset = UNSET
        if _turn_by_turn_actions is not UNSET:
            turn_by_turn_actions = []
            for turn_by_turn_actions_item_data in _turn_by_turn_actions:
                turn_by_turn_actions_item = OffsetAction.from_dict(
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
        summary: PedestrianSummary | Unset
        if isinstance(_summary, Unset):
            summary = UNSET
        else:
            summary = PedestrianSummary.from_dict(_summary)

        _travel_summary = d.pop("travelSummary", UNSET)
        travel_summary: BaseSummary | Unset
        if isinstance(_travel_summary, Unset):
            travel_summary = UNSET
        else:
            travel_summary = BaseSummary.from_dict(_travel_summary)

        polyline = d.pop("polyline", UNSET)

        _notices = d.pop("notices", UNSET)
        notices: list[PedestrianNotice] | Unset = UNSET
        if _notices is not UNSET:
            notices = []
            for notices_item_data in _notices:
                notices_item = PedestrianNotice.from_dict(notices_item_data)

                notices.append(notices_item)

        _spans = d.pop("spans", UNSET)
        spans: list[PedestrianSpan] | Unset = UNSET
        if _spans is not UNSET:
            spans = []
            for spans_item_data in _spans:
                spans_item = PedestrianSpan.from_dict(spans_item_data)

                spans.append(spans_item)

        _ref_replacements = d.pop("refReplacements", UNSET)
        ref_replacements: RefReplacements | Unset
        if isinstance(_ref_replacements, Unset):
            ref_replacements = UNSET
        else:
            ref_replacements = RefReplacements.from_dict(_ref_replacements)

        pedestrian_section = cls(
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
            ref_replacements=ref_replacements,
        )

        pedestrian_section.additional_properties = d
        return pedestrian_section

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
