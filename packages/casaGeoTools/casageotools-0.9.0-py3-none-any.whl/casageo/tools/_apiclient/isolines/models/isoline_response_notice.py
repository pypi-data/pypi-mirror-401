from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.notice_severity import NoticeSeverity
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_notice_detail import BaseNoticeDetail


T = TypeVar("T", bound="IsolineResponseNotice")


@_attrs_define
class IsolineResponseNotice:
    """A notice contains important notifications.

    Attributes:
        code (str): Extensible enum: `avoidSegmentsInvalidId` `avoidSegmentsInvalidPrefix` `avoidZonesInvalidId`
            `avoidTruckRoadTypesInvalidId` `cancelled` `couldNotMatchOrigin` `couldNotMatchDestination`
            `isolineCalculationFailed` `isolineCalculationBlocked` `unknownParameter` `...`
            Currently known codes (non-exhaustive: this list will be extended for new error situations):

            | Code      | Description  | Severity |
            | --------- | ------- | ------- |
            | avoidSegmentsInvalidId | Avoid segments: The provided segment ID was not found | info |
            | avoidSegmentsInvalidPrefix | Avoid segments: The provided domain prefix was not found | info |
            | avoidZonesInvalidId | Avoid zones: The provided zone ID was not found | info |
            | avoidTruckRoadTypesInvalidId | The provided truck road type id was not found | info |
            | cancelled | Calculation took too long and was cancelled | critical |
            | couldNotMatchOrigin | Origin waypoint could not be matched | critical |
            | couldNotMatchDestination | Destination waypoint could not be matched | critical |
            | isolineCalculationFailed | Isolines could not be calculated. | critical |
            | isolineCalculationBlocked | Isolines calculation was blocked by restrictions or traffic at the requested
            origin or destination | critical |
            | unknownParameter | The provided parameter is unknown | info |
             Example: noRouteFound.
        title (str | Unset): Human-readable notice description. Example: No route found.
        severity (NoticeSeverity | Unset): Describes the impact a notice has on the resource to which the notice is
            attached.
            * critical - The notice must not be ignored, even if the type of notice is not known to the user. Any associated
            resource (e.g., route section) must not be used without further evaluation.
            * info - The notice is for informative purposes, but does not affect usability of the route.
        details (list[BaseNoticeDetail] | Unset): Additional details about the notice
    """

    code: str
    title: str | Unset = UNSET
    severity: NoticeSeverity | Unset = UNSET
    details: list[BaseNoticeDetail] | Unset = UNSET
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
        from ..models.base_notice_detail import BaseNoticeDetail

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
        details: list[BaseNoticeDetail] | Unset = UNSET
        if _details is not UNSET:
            details = []
            for details_item_data in _details:
                details_item = BaseNoticeDetail.from_dict(details_item_data)

                details.append(details_item)

        isoline_response_notice = cls(
            code=code,
            title=title,
            severity=severity,
            details=details,
        )

        isoline_response_notice.additional_properties = d
        return isoline_response_notice

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
