from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.notice_severity import NoticeSeverity
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vehicle_restriction import VehicleRestriction
    from ..models.violated_charging_station_opening_hours import (
        ViolatedChargingStationOpeningHours,
    )
    from ..models.violated_transport_mode import ViolatedTransportMode
    from ..models.violated_truck_road_type import ViolatedTruckRoadType
    from ..models.violated_zone_reference import ViolatedZoneReference


T = TypeVar("T", bound="VehicleNotice")


@_attrs_define
class VehicleNotice:
    """A notice contains important notifications.

    Example:
        {'$ref': '#/components/examples/noticeWithRestrictionsExample'}

    Attributes:
        code (str): Extensible enum: `violatedAvoidControlledAccessHighway` `violatedAvoidTollRoad`
            `violatedAvoidTunnel` `violatedAvoidDirtRoad` `violatedBlockedRoad` `violatedStartDirection` `violatedCarpool`
            `violatedTurnRestriction` `violatedVehicleRestriction` `violatedZoneRestriction` `violatedAvoidDifficultTurns`
            `violatedAvoidUTurns` `violatedEmergencyGate` `violatedAvoidSeasonalClosure` `violatedAvoidTollTransponder`
            `violatedAvoidTruckRoadType` `seasonalClosure` `tollTransponder` `mlDurationUnavailable` `simplePolyline`
            `tollsDataUnavailable` `tollsDataTemporarilyUnavailable` `chargingStopNotNeeded`
            `violatedChargingStationOpeningHours` `violatedMinChargeAtDestination` `violatedMinChargeAtFirstChargingStation`
            `violatedMinChargeAtChargingStation` `outOfCharge` `currentWeightNegative` `currentWeightExceedsLimit`
            `travelTimeExceedsDriverWorkHours` `carpool` `turnRestriction` `vehicleRestriction` `zoneRestriction`
            `avoidTollRoad` `targetChargeNotAchievable` `violatedChargingStationTransportMode`
            `violatedChargingStationVehicleRestrictions` `...`
            Currently known codes (non-exhaustive: this list could be extended for new situations):

            | Code      | Description  | Severity |
            | --------- | ------- | ------- |
            | violatedAvoidControlledAccessHighway | Route did not manage to avoid user preference. | critical |
            | violatedAvoidTollRoad | Route did not manage to avoid user preference. | critical |
            | violatedAvoidTunnel | Route did not manage to avoid user preference. | critical |
            | violatedAvoidDirtRoad | Route did not manage to avoid user preference. | critical |
            | violatedBlockedRoad | Route uses roads that are blocked, due to traffic incidents, `avoid[areas]`, or
            `avoid[segments]`. | critical |
            | violatedStartDirection | The starting direction of the route differs from the value set in the `course`
            parameter of the waypoint. | critical |
            | violatedCarpool | Route did not manage to avoid user preference. | critical |
            | violatedTurnRestriction | Route requires performing a time-restricted maneuver at a time when it's prohibited.
            | critical |
            | violatedVehicleRestriction | Route uses a road which is forbidden for the given vehicle profile. | critical |
            | violatedZoneRestriction | Route uses a road in a user-specified avoidance zone, such as the London Low
            Emission Zone. | critical |
            | violatedAvoidDifficultTurns | Route did not manage to avoid user preference.| critical |
            | violatedAvoidUTurns | Route did not manage to avoid user preference. | critical |
            | violatedEmergencyGate | Route goes through an emergency gate. | critical |
            | violatedAvoidSeasonalClosure | Route did not manage to avoid a seasonal closure.| critical |
            | violatedAvoidTollTransponder | Route did not manage to avoid a toll booth that requires a transponder. |
            critical |
            | violatedAvoidTruckRoadType | Route did not manage to avoid truck road type. | critical |
            | seasonalClosure | Route goes through a seasonal closure. | info |
            | tollTransponder | Route goes through a toll booth that requires a transponder. | info |
            | mlDurationUnavailable | Machine learning duration was requested but is not available for this section. | info
            |
            | simplePolyline | An accurate polyline is not available for this section. The returned polyline has been
            generated from departure and arrival places. | info |
            | tollsDataUnavailable | Tolls data was requested but could not be calculated for this section. | info |
            | tollsDataTemporarilyUnavailable | Tolls data was requested but is temporarily unavailable. | info |
            | chargingStopNotNeeded | A charging stop was planned at the destination of this section, but it is no longer
            needed (getRoutesByHandle requests only). | info |
            | violatedChargingStationOpeningHours | A charging stop was planned at the destination of this section, but the
            `postActions` would not be completed within the opening hours. | critical |
            | violatedMinChargeAtDestination | The `arrival.charge` at the destination is lower than the
            `minChargeAtDestination`. | info |
            | violatedMinChargeAtFirstChargingStation | The `arrival.charge` on the first charging stop is lower than the
            `minChargeAtFirstChargingStation`. | info |
            | violatedMinChargeAtChargingStation | The `arrival.charge` on a charging station stop is lower than the
            `minChargeAtChargingStation`. This can be on the first charging stop if `minChargeAtFirstChargingStation` is not
            specified. | info |
            | outOfCharge | The charge of the EV drops below 0 along the section. | info |
            | currentWeightNegative | `vehicle[currentWeight]` is negative after applying `currentWeightChange` at a via
            waypoint. | critical |
            | currentWeightExceedsLimit | `vehicle[currentWeight]` exceeds limit for given `transportMode`. | critical |
            | travelTimeExceedsDriverWorkHours | The route travelTime exceeds drive time sequence provided in
            `driver[schedule]` parameter. | critical |
            | targetChargeNotAchievable | `ev[MaxChargingDuration]` too short to achieve required charging level. | info |
            | violatedChargingStationTransportMode | Provided `transportMode` is not permitted at the charging station |
            critical |
            | violatedChargingStationVehicleRestrictions | One or more vehicle attributes exceed the permitted vehicle
            limits of the charging station | critical |


            The codes listed below can appear as info notices when the request contains
            `return=potentialTimeDependentViolations`.
            The resulting info notices are not violations on the current route but could be violations if the arrival time
            at these restrictions differs from the calculated time.
            For example, an info notice for a `vehicleRestriction` could indicate that while your vehicle is not currently
            violating any restriction.
            However, if the journey is delayed by an hour the vehicle would not be allowed on part of the route because
            there is a time-dependent restriction active at that time.

            Codes for potential time dependent restriction violations are (non-exhaustive: can be extended for new
            situations):

            | Code      | Description  | Severity |
            | --------- | ------- | ------- |
            | carpool | Route potentially uses a carpool only road when not allowed. | info |
            | turnRestriction | Route potentially uses a time-restricted turn when not allowed. | info |
            | vehicleRestriction | Route potentially uses a road that is forbidden for the given vehicle profile. | info |
            | zoneRestriction | Route uses a road that is potentially part of restricted routing zones. | info |
            | avoidTollRoad | Route uses a road that potentially is a toll road. **Note:** This is not currently supported
            and will not be returned, but the enum value is retained for backwards-compatibility purposes. | info |
             Example: violatedAvoidTollRoad.
        title (str | Unset): Human-readable notice description. Example: Violated avoid toll road.
        severity (NoticeSeverity | Unset): Describes the impact a notice has on the resource to which the notice is
            attached.
            * critical - The notice must not be ignored, even if the type of notice is not known to the user. Any associated
            resource (e.g., route section) must not be used without further evaluation.
            * info - The notice is for informative purposes, but does not affect usability of the route.
        details (list[VehicleRestriction | ViolatedChargingStationOpeningHours | ViolatedTransportMode |
            ViolatedTruckRoadType | ViolatedZoneReference] | Unset): Additional details about the notice
    """

    code: str
    title: str | Unset = UNSET
    severity: NoticeSeverity | Unset = UNSET
    details: (
        list[
            VehicleRestriction
            | ViolatedChargingStationOpeningHours
            | ViolatedTransportMode
            | ViolatedTruckRoadType
            | ViolatedZoneReference
        ]
        | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.vehicle_restriction import VehicleRestriction
        from ..models.violated_transport_mode import ViolatedTransportMode
        from ..models.violated_truck_road_type import ViolatedTruckRoadType
        from ..models.violated_zone_reference import ViolatedZoneReference

        code = self.code

        title = self.title

        severity: str | Unset = UNSET
        if not isinstance(self.severity, Unset):
            severity = self.severity.value

        details: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.details, Unset):
            details = []
            for details_item_data in self.details:
                details_item: dict[str, Any]
                if isinstance(details_item_data, VehicleRestriction):
                    details_item = details_item_data.to_dict()
                elif isinstance(details_item_data, ViolatedTransportMode):
                    details_item = details_item_data.to_dict()
                elif isinstance(details_item_data, ViolatedTruckRoadType):
                    details_item = details_item_data.to_dict()
                elif isinstance(details_item_data, ViolatedZoneReference):
                    details_item = details_item_data.to_dict()
                else:
                    details_item = details_item_data.to_dict()

                details.append(details_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "code": code,
        })
        if title is not UNSET:
            field_dict["title"] = title
        if severity is not UNSET:
            field_dict["severity"] = severity
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vehicle_restriction import VehicleRestriction
        from ..models.violated_charging_station_opening_hours import (
            ViolatedChargingStationOpeningHours,
        )
        from ..models.violated_transport_mode import ViolatedTransportMode
        from ..models.violated_truck_road_type import ViolatedTruckRoadType
        from ..models.violated_zone_reference import ViolatedZoneReference

        d = dict(src_dict)
        code = d.pop("code")

        title = d.pop("title", UNSET)

        _severity = d.pop("severity", UNSET)
        severity: NoticeSeverity | Unset
        if isinstance(_severity, Unset):
            severity = UNSET
        else:
            severity = NoticeSeverity(_severity)

        _details = d.pop("details", UNSET)
        details: (
            list[
                VehicleRestriction
                | ViolatedChargingStationOpeningHours
                | ViolatedTransportMode
                | ViolatedTruckRoadType
                | ViolatedZoneReference
            ]
            | Unset
        ) = UNSET
        if _details is not UNSET:
            details = []
            for details_item_data in _details:

                def _parse_details_item(
                    data: object,
                ) -> (
                    VehicleRestriction
                    | ViolatedChargingStationOpeningHours
                    | ViolatedTransportMode
                    | ViolatedTruckRoadType
                    | ViolatedZoneReference
                ):
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_vehicle_notice_detail_type_0 = (
                            VehicleRestriction.from_dict(data)
                        )

                        return componentsschemas_vehicle_notice_detail_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_vehicle_notice_detail_type_1 = (
                            ViolatedTransportMode.from_dict(data)
                        )

                        return componentsschemas_vehicle_notice_detail_type_1
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_vehicle_notice_detail_type_2 = (
                            ViolatedTruckRoadType.from_dict(data)
                        )

                        return componentsschemas_vehicle_notice_detail_type_2
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_vehicle_notice_detail_type_3 = (
                            ViolatedZoneReference.from_dict(data)
                        )

                        return componentsschemas_vehicle_notice_detail_type_3
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_vehicle_notice_detail_type_4 = (
                        ViolatedChargingStationOpeningHours.from_dict(data)
                    )

                    return componentsschemas_vehicle_notice_detail_type_4

                details_item = _parse_details_item(details_item_data)

                details.append(details_item)

        vehicle_notice = cls(
            code=code,
            title=title,
            severity=severity,
            details=details,
        )

        vehicle_notice.additional_properties = d
        return vehicle_notice

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
