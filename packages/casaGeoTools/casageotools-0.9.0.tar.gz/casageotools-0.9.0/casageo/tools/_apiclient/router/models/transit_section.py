from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.transit_section_type import TransitSectionType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agency import Agency
    from ..models.arrive_action import ArriveAction
    from ..models.attribution import Attribution
    from ..models.base_summary import BaseSummary
    from ..models.board_action import BoardAction
    from ..models.continue_action import ContinueAction
    from ..models.deboard_action import DeboardAction
    from ..models.depart_action import DepartAction
    from ..models.fare import Fare
    from ..models.passthrough import Passthrough
    from ..models.ref_replacements import RefReplacements
    from ..models.transit_departure import TransitDeparture
    from ..models.transit_incident import TransitIncident
    from ..models.transit_notice import TransitNotice
    from ..models.transit_span import TransitSpan
    from ..models.transit_stop import TransitStop
    from ..models.transit_transport import TransitTransport
    from ..models.web_link import WebLink
    from ..models.web_link_with_device_type import WebLinkWithDeviceType


T = TypeVar("T", bound="TransitSection")


@_attrs_define
class TransitSection:
    """A section of the route. It contains departure, arrival, and route information.

    Attributes:
        id (str): Unique identifier of the section
        type_ (TransitSectionType): Section type used by the client to identify what extension to the BaseSection are
            available.
        departure (TransitDeparture): Transit departure
        arrival (TransitDeparture): Transit departure
        pre_actions (list[BoardAction] | Unset): Actions that must be done prior to `departure`.
        actions (list[ArriveAction | ContinueAction | DepartAction] | Unset): Actions that must be done during the
            travel portion of the section.

            Action offsets represent the coordinate index in the polyline.

            *NOTE:* currentRoad and nextRoad are not populated for actions.
        language (str | Unset): Language of the localized strings in the section, if any, in BCP47 format.
        post_actions (list[DeboardAction] | Unset): Actions that must be done after `arrival`.
        turn_by_turn_actions (list[DepartAction] | Unset): Actions for turn by turn guidance during the travel portion
            of the section, i.e., between `departure` and `arrival`.
        passthrough (list[Passthrough] | Unset): List of via waypoints this section is passing through.

            Each via waypoint of the request that is a `passThrough=true` waypoint, appears as a
            `Passthrough` in the response. It appears in the section that starts with the closest
            non-passthrough via specified before it or origin.

            The passthrough vias appear in this list in the order they are traversed. They are
            traversed in the order they are specified in the request.
        summary (BaseSummary | Unset): Total value of key attributes for a route section.
        travel_summary (BaseSummary | Unset): Total value of key attributes for a route section.
        polyline (str | Unset): Line string in [Flexible Polyline](https://github.com/heremaps/flexible-polyline)
            format. Coordinates are in the WGS84 coordinate system, including `Elevation` (if present). Example:
            A05xgKuy2xCx9B7vUl0OhnR54EqSzpEl-HxjD3pBiGnyGi2CvwFsgD3nD4vB6e.
        notices (list[TransitNotice] | Unset): Contains a list of issues related to this section of the route.
        booking_links (list[WebLinkWithDeviceType] | Unset): Links to external ticket booking services
        transport (TransitTransport | Unset): Transit transport information.
        intermediate_stops (list[TransitStop] | Unset): Intermediate stops between departure and destination of the
            transit line. It can be missing if this information is not available or not requested.
        agency (Agency | Unset): Contains information about a particular agency.
        attributions (list[Attribution] | Unset): List of required attributions to display.
        fares (list[Fare] | Unset): "List of tickets to pay for this section of the route"

            **NOTE**: Fares information support will be available soon.
        booking (WebLink | Unset): The URL address to an external resource. Example: {'id': '88-7568-21.07.2023',
            'text': 'Information for public transit provided by ThePublicTransit GmbH'}.
        spans (list[TransitSpan] | Unset): Span attached to a `Section` describing transit content.
        ref_replacements (RefReplacements | Unset): Dictionary of placeholders to replacement strings for the compact
            representation of map entity references.
        incidents (list[TransitIncident] | Unset): A list of all incidents that apply to the section.
    """

    id: str
    type_: TransitSectionType
    departure: TransitDeparture
    arrival: TransitDeparture
    pre_actions: list[BoardAction] | Unset = UNSET
    actions: list[ArriveAction | ContinueAction | DepartAction] | Unset = UNSET
    language: str | Unset = UNSET
    post_actions: list[DeboardAction] | Unset = UNSET
    turn_by_turn_actions: list[DepartAction] | Unset = UNSET
    passthrough: list[Passthrough] | Unset = UNSET
    summary: BaseSummary | Unset = UNSET
    travel_summary: BaseSummary | Unset = UNSET
    polyline: str | Unset = UNSET
    notices: list[TransitNotice] | Unset = UNSET
    booking_links: list[WebLinkWithDeviceType] | Unset = UNSET
    transport: TransitTransport | Unset = UNSET
    intermediate_stops: list[TransitStop] | Unset = UNSET
    agency: Agency | Unset = UNSET
    attributions: list[Attribution] | Unset = UNSET
    fares: list[Fare] | Unset = UNSET
    booking: WebLink | Unset = UNSET
    spans: list[TransitSpan] | Unset = UNSET
    ref_replacements: RefReplacements | Unset = UNSET
    incidents: list[TransitIncident] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.arrive_action import ArriveAction
        from ..models.depart_action import DepartAction

        id = self.id

        type_ = self.type_.value

        departure = self.departure.to_dict()

        arrival = self.arrival.to_dict()

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
                else:
                    actions_item = actions_item_data.to_dict()

                actions.append(actions_item)

        language = self.language

        post_actions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.post_actions, Unset):
            post_actions = []
            for post_actions_item_data in self.post_actions:
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

        booking_links: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.booking_links, Unset):
            booking_links = []
            for booking_links_item_data in self.booking_links:
                booking_links_item = booking_links_item_data.to_dict()
                booking_links.append(booking_links_item)

        transport: dict[str, Any] | Unset = UNSET
        if not isinstance(self.transport, Unset):
            transport = self.transport.to_dict()

        intermediate_stops: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.intermediate_stops, Unset):
            intermediate_stops = []
            for intermediate_stops_item_data in self.intermediate_stops:
                intermediate_stops_item = intermediate_stops_item_data.to_dict()
                intermediate_stops.append(intermediate_stops_item)

        agency: dict[str, Any] | Unset = UNSET
        if not isinstance(self.agency, Unset):
            agency = self.agency.to_dict()

        attributions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.attributions, Unset):
            attributions = []
            for attributions_item_data in self.attributions:
                attributions_item = attributions_item_data.to_dict()
                attributions.append(attributions_item)

        fares: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.fares, Unset):
            fares = []
            for fares_item_data in self.fares:
                fares_item = fares_item_data.to_dict()
                fares.append(fares_item)

        booking: dict[str, Any] | Unset = UNSET
        if not isinstance(self.booking, Unset):
            booking = self.booking.to_dict()

        spans: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.spans, Unset):
            spans = []
            for spans_item_data in self.spans:
                spans_item = spans_item_data.to_dict()
                spans.append(spans_item)

        ref_replacements: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ref_replacements, Unset):
            ref_replacements = self.ref_replacements.to_dict()

        incidents: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.incidents, Unset):
            incidents = []
            for incidents_item_data in self.incidents:
                incidents_item = incidents_item_data.to_dict()
                incidents.append(incidents_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "type": type_,
            "departure": departure,
            "arrival": arrival,
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
        if booking_links is not UNSET:
            field_dict["bookingLinks"] = booking_links
        if transport is not UNSET:
            field_dict["transport"] = transport
        if intermediate_stops is not UNSET:
            field_dict["intermediateStops"] = intermediate_stops
        if agency is not UNSET:
            field_dict["agency"] = agency
        if attributions is not UNSET:
            field_dict["attributions"] = attributions
        if fares is not UNSET:
            field_dict["fares"] = fares
        if booking is not UNSET:
            field_dict["booking"] = booking
        if spans is not UNSET:
            field_dict["spans"] = spans
        if ref_replacements is not UNSET:
            field_dict["refReplacements"] = ref_replacements
        if incidents is not UNSET:
            field_dict["incidents"] = incidents

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agency import Agency
        from ..models.arrive_action import ArriveAction
        from ..models.attribution import Attribution
        from ..models.base_summary import BaseSummary
        from ..models.board_action import BoardAction
        from ..models.continue_action import ContinueAction
        from ..models.deboard_action import DeboardAction
        from ..models.depart_action import DepartAction
        from ..models.fare import Fare
        from ..models.passthrough import Passthrough
        from ..models.ref_replacements import RefReplacements
        from ..models.transit_departure import TransitDeparture
        from ..models.transit_incident import TransitIncident
        from ..models.transit_notice import TransitNotice
        from ..models.transit_span import TransitSpan
        from ..models.transit_stop import TransitStop
        from ..models.transit_transport import TransitTransport
        from ..models.web_link import WebLink
        from ..models.web_link_with_device_type import WebLinkWithDeviceType

        d = dict(src_dict)
        id = d.pop("id")

        type_ = TransitSectionType(d.pop("type"))

        departure = TransitDeparture.from_dict(d.pop("departure"))

        arrival = TransitDeparture.from_dict(d.pop("arrival"))

        _pre_actions = d.pop("preActions", UNSET)
        pre_actions: list[BoardAction] | Unset = UNSET
        if _pre_actions is not UNSET:
            pre_actions = []
            for pre_actions_item_data in _pre_actions:
                pre_actions_item = BoardAction.from_dict(pre_actions_item_data)

                pre_actions.append(pre_actions_item)

        _actions = d.pop("actions", UNSET)
        actions: list[ArriveAction | ContinueAction | DepartAction] | Unset = UNSET
        if _actions is not UNSET:
            actions = []
            for actions_item_data in _actions:

                def _parse_actions_item(
                    data: object,
                ) -> ArriveAction | ContinueAction | DepartAction:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_transit_action_type_0 = (
                            DepartAction.from_dict(data)
                        )

                        return componentsschemas_transit_action_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_transit_action_type_1 = (
                            ArriveAction.from_dict(data)
                        )

                        return componentsschemas_transit_action_type_1
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_transit_action_type_2 = ContinueAction.from_dict(
                        data
                    )

                    return componentsschemas_transit_action_type_2

                actions_item = _parse_actions_item(actions_item_data)

                actions.append(actions_item)

        language = d.pop("language", UNSET)

        _post_actions = d.pop("postActions", UNSET)
        post_actions: list[DeboardAction] | Unset = UNSET
        if _post_actions is not UNSET:
            post_actions = []
            for post_actions_item_data in _post_actions:
                post_actions_item = DeboardAction.from_dict(post_actions_item_data)

                post_actions.append(post_actions_item)

        _turn_by_turn_actions = d.pop("turnByTurnActions", UNSET)
        turn_by_turn_actions: list[DepartAction] | Unset = UNSET
        if _turn_by_turn_actions is not UNSET:
            turn_by_turn_actions = []
            for turn_by_turn_actions_item_data in _turn_by_turn_actions:
                turn_by_turn_actions_item = DepartAction.from_dict(
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
        summary: BaseSummary | Unset
        if isinstance(_summary, Unset):
            summary = UNSET
        else:
            summary = BaseSummary.from_dict(_summary)

        _travel_summary = d.pop("travelSummary", UNSET)
        travel_summary: BaseSummary | Unset
        if isinstance(_travel_summary, Unset):
            travel_summary = UNSET
        else:
            travel_summary = BaseSummary.from_dict(_travel_summary)

        polyline = d.pop("polyline", UNSET)

        _notices = d.pop("notices", UNSET)
        notices: list[TransitNotice] | Unset = UNSET
        if _notices is not UNSET:
            notices = []
            for notices_item_data in _notices:
                notices_item = TransitNotice.from_dict(notices_item_data)

                notices.append(notices_item)

        _booking_links = d.pop("bookingLinks", UNSET)
        booking_links: list[WebLinkWithDeviceType] | Unset = UNSET
        if _booking_links is not UNSET:
            booking_links = []
            for booking_links_item_data in _booking_links:
                booking_links_item = WebLinkWithDeviceType.from_dict(
                    booking_links_item_data
                )

                booking_links.append(booking_links_item)

        _transport = d.pop("transport", UNSET)
        transport: TransitTransport | Unset
        if isinstance(_transport, Unset):
            transport = UNSET
        else:
            transport = TransitTransport.from_dict(_transport)

        _intermediate_stops = d.pop("intermediateStops", UNSET)
        intermediate_stops: list[TransitStop] | Unset = UNSET
        if _intermediate_stops is not UNSET:
            intermediate_stops = []
            for intermediate_stops_item_data in _intermediate_stops:
                intermediate_stops_item = TransitStop.from_dict(
                    intermediate_stops_item_data
                )

                intermediate_stops.append(intermediate_stops_item)

        _agency = d.pop("agency", UNSET)
        agency: Agency | Unset
        if isinstance(_agency, Unset):
            agency = UNSET
        else:
            agency = Agency.from_dict(_agency)

        _attributions = d.pop("attributions", UNSET)
        attributions: list[Attribution] | Unset = UNSET
        if _attributions is not UNSET:
            attributions = []
            for attributions_item_data in _attributions:
                attributions_item = Attribution.from_dict(attributions_item_data)

                attributions.append(attributions_item)

        _fares = d.pop("fares", UNSET)
        fares: list[Fare] | Unset = UNSET
        if _fares is not UNSET:
            fares = []
            for fares_item_data in _fares:
                fares_item = Fare.from_dict(fares_item_data)

                fares.append(fares_item)

        _booking = d.pop("booking", UNSET)
        booking: WebLink | Unset
        if isinstance(_booking, Unset):
            booking = UNSET
        else:
            booking = WebLink.from_dict(_booking)

        _spans = d.pop("spans", UNSET)
        spans: list[TransitSpan] | Unset = UNSET
        if _spans is not UNSET:
            spans = []
            for spans_item_data in _spans:
                spans_item = TransitSpan.from_dict(spans_item_data)

                spans.append(spans_item)

        _ref_replacements = d.pop("refReplacements", UNSET)
        ref_replacements: RefReplacements | Unset
        if isinstance(_ref_replacements, Unset):
            ref_replacements = UNSET
        else:
            ref_replacements = RefReplacements.from_dict(_ref_replacements)

        _incidents = d.pop("incidents", UNSET)
        incidents: list[TransitIncident] | Unset = UNSET
        if _incidents is not UNSET:
            incidents = []
            for incidents_item_data in _incidents:
                incidents_item = TransitIncident.from_dict(incidents_item_data)

                incidents.append(incidents_item)

        transit_section = cls(
            id=id,
            type_=type_,
            departure=departure,
            arrival=arrival,
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
            booking_links=booking_links,
            transport=transport,
            intermediate_stops=intermediate_stops,
            agency=agency,
            attributions=attributions,
            fares=fares,
            booking=booking,
            spans=spans,
            ref_replacements=ref_replacements,
            incidents=incidents,
        )

        transit_section.additional_properties = d
        return transit_section

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
