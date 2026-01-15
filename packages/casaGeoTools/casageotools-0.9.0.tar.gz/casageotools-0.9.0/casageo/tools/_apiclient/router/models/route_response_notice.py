from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.notice_severity import NoticeSeverity
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.via_notice_detail import ViaNoticeDetail


T = TypeVar("T", bound="RouteResponseNotice")


@_attrs_define
class RouteResponseNotice:
    """A notice contains important notifications.

    Example:
        {'$ref': '#/components/examples/routeResponseNoticeExample'}

    Attributes:
        code (str): Extensible enum: `noRouteFound` `failedRouteHandleCreation` `cancelled` `routeCalculationFailed`
            `couldNotMatchOrigin` `couldNotMatchDestination` `noReachableChargingStationsFound`
            `violatedTransportModeInRouteHandleDecoding` `unknownError` `routeLengthLimitExceeded` `avoidSegmentsInvalidId`
            `avoidZonesInvalidId` `avoidTruckRoadTypesInvalidId` `returnToRoute` `importFailed` `importSplitRoute`
            `brandDoesNotExist` `unknownParameter` `mainLanguageNotFound` `avoidOptionsWithMakeReachableLimitation`
            `currentWeightChangeNoCurrentWeight` `currentWeightChangeNoGrossWeight` `...`
            Currently known codes (non-exhaustive: this list could be extended for new error situations):

            | Code      | Description  | Severity |
            | --------- | ------- | ------- |
            | noRouteFound | No Route was found | critical |
            | failedRouteHandleCreation | No RouteHandle was created | critical |
            | cancelled | Calculation took too long and was cancelled | critical |
            | routeCalculationFailed | Calculation did not succeed | critical |
            | couldNotMatchOrigin | Origin waypoint could not be matched | critical |
            | couldNotMatchDestination | Destination waypoint could not be matched | critical |
            | noReachableChargingStationsFound | Initial charge is not enough to reach any known charging stations |
            critical |
            | violatedTransportModeInRouteHandleDecoding | Route handle decoding failed due to forbidden segments for the
            specified transport mode | critical |
            | unknownError | No detailed error cause has been determined | critical |
            | routeLengthLimitExceeded | Distance between waypoints is too large for current options | critical |
            | avoidSegmentsInvalidId | The provided segment ID was not found | info |
            | avoidZonesInvalidId | The provided zone ID was not found | info |
            | avoidTruckRoadTypesInvalidId | The provided truck road type id was not found | info |
            | returnToRoute | Applicable only to requests with route handle provided. Current route position was not on the
            original route. New route was calculated from the current position to the destination. Old route may have been
            reused. | info |
            | importFailed | No route section was found for imported waypoints | critical |
            | importSplitRoute | Not all trace points were matched | info |
            | brandDoesNotExist | Preferred charging station brand does not exist | info |
            | unknownParameter | The provided parameter is unknown | info |
            | mainLanguageNotFound | The first language in the list of preferred languages is not supported. | info |
            | avoidOptionsWithMakeReachableLimitation | Avoiding toll or controlledAccessHighway with makeReachable is
            supported only for trucks up to 7.5 tons. | critical |
            | currentWeightChangeNoCurrentWeight | Route handle contains `currentWeightChange` but missing
            vehicle[currentWeight]. `currentWeight` will not be evaluated. | info |
            | currentWeightChangeNoGrossWeight | Route handle contains `currentWeightChange` but missing
            vehicle[grossWeight]. Vehicle restrictions based on gross weight will not be evaluated. | info |
             Example: noRouteFound.
        title (str | Unset): Human-readable notice description. Example: No route found.
        severity (NoticeSeverity | Unset): Describes the impact a notice has on the resource to which the notice is
            attached.
            * critical - The notice must not be ignored, even if the type of notice is not known to the user. Any associated
            resource (e.g., route section) must not be used without further evaluation.
            * info - The notice is for informative purposes, but does not affect usability of the route.
        details (list[ViaNoticeDetail] | Unset): Additional details about the notice
    """

    code: str
    title: str | Unset = UNSET
    severity: NoticeSeverity | Unset = UNSET
    details: list[ViaNoticeDetail] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        title = self.title

        severity: str | Unset = UNSET
        if not isinstance(self.severity, Unset):
            severity = self.severity.value

        details: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.details, Unset):
            details = []
            for details_item_data in self.details:
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
        from ..models.via_notice_detail import ViaNoticeDetail

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
        details: list[ViaNoticeDetail] | Unset = UNSET
        if _details is not UNSET:
            details = []
            for details_item_data in _details:
                details_item = ViaNoticeDetail.from_dict(details_item_data)

                details.append(details_item)

        route_response_notice = cls(
            code=code,
            title=title,
            severity=severity,
            details=details,
        )

        route_response_notice.additional_properties = d
        return route_response_notice

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
