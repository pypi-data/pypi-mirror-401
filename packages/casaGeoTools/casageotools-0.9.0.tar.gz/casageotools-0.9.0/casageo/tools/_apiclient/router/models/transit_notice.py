from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.notice_severity import NoticeSeverity
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vehicle_restriction import VehicleRestriction
    from ..models.violated_transport_mode import ViolatedTransportMode


T = TypeVar("T", bound="TransitNotice")


@_attrs_define
class TransitNotice:
    """A notice contains important notifications.

    Attributes:
        code (str): Extensible enum: `noSchedule` `noIntermediate` `unwantedMode` `scheduledTimes` `simplePolyline`
            `violatedAvoidFerry` `violatedAvoidRailFerry` `seasonalClosure` `currentWeightNegative`
            `travelTimeExceedsDriverWorkHours` `vehicleRestriction` `...`
            Currently known codes (non-exhaustive: this list could be extended for new situations):

            | Code      | Description  | Severity |
            | --------- | ------- | ------- |
            | noSchedule | A timetable schedule is not available for the transit line in this section, and only the run
            frequency is available. As a result, departure/arrival times are approximated | info |
            | noIntermediate | Information about intermediate stops is not available for this transit line | info |
            | unwantedMode | This section contains a transport mode that was explicitly disabled. Mode filtering is not
            available in this area | info |
            | scheduledTimes | The times returned on this section are the scheduled times even though delay information are
            available | info |
            | simplePolyline | An accurate polyline is not available for this section. The returned polyline has been
            generated from departure and arrival places | info |
            | violatedAvoidFerry | Route did not manage to avoid user preference | critical |
            | violatedAvoidRailFerry | Route did not manage to avoid user preference | critical |
            | seasonalClosure | Route goes through seasonal closure | info |
            | currentWeightNegative | `vehicle[currentWeight]` is negative after applying `currentWeightChange` at a via
            waypoint. | critical |
            | travelTimeExceedsDriverWorkHours | The route travelTime exceeds drive time sequence provided in
            `driver[schedule]` parameter | critical |


            The codes listed below can appear as info notices when the request contains
            `return=potentialTimeDependentViolations`.
            The resulting info notices are not violations on the current route but could be violations if the arrival time
            at these restrictions differs from the calculated time.
            For example, an info notice for a `vehicleRestriction` could indicate that your vehicle is not currently
            violating any restriction but,
            If the journey is delayed by an hour, the vehicle would not be allowed on part of the route because there is a
            time-dependent restriction active at that time.

            Codes for potential time-dependent restriction violations are (non-exhaustive: can be extended for new
            situations):

            | Code      | Description  | Severity |
            | --------- | ------- | ------- |
            | vehicleRestriction | Route potentially uses a road that is forbidden for the given vehicle profile | info |
             Example: noSchedule.
        title (str | Unset): Human-readable notice description. Example: No schedule.
        severity (NoticeSeverity | Unset): Describes the impact a notice has on the resource to which the notice is
            attached.
            * critical - The notice must not be ignored, even if the type of notice is not known to the user. Any associated
            resource (e.g., route section) must not be used without further evaluation.
            * info - The notice is for informative purposes, but does not affect usability of the route.
        details (list[VehicleRestriction | ViolatedTransportMode] | Unset): Additional details about the notice
    """

    code: str
    title: str | Unset = UNSET
    severity: NoticeSeverity | Unset = UNSET
    details: list[VehicleRestriction | ViolatedTransportMode] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.vehicle_restriction import VehicleRestriction

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
        from ..models.violated_transport_mode import ViolatedTransportMode

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
        details: list[VehicleRestriction | ViolatedTransportMode] | Unset = UNSET
        if _details is not UNSET:
            details = []
            for details_item_data in _details:

                def _parse_details_item(
                    data: object,
                ) -> VehicleRestriction | ViolatedTransportMode:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_transit_notice_detail_type_0 = (
                            VehicleRestriction.from_dict(data)
                        )

                        return componentsschemas_transit_notice_detail_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_transit_notice_detail_type_1 = (
                        ViolatedTransportMode.from_dict(data)
                    )

                    return componentsschemas_transit_notice_detail_type_1

                details_item = _parse_details_item(details_item_data)

                details.append(details_item)

        transit_notice = cls(
            code=code,
            title=title,
            severity=severity,
            details=details,
        )

        transit_notice.additional_properties = d
        return transit_notice

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
