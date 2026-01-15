from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="IsolineErrorResponse")


@_attrs_define
class IsolineErrorResponse:
    """Response in case of error

    Attributes:
        title (str): Human-readable error description Example: Input data failed validation.
        status (int): HTTP status code Example: 400.
        code (str): Machine-readable service error code.

            All error codes of this service start with "`E605`". The last three digits describe a specific error. Provide
            this error code when contacting support.

            **NOTE:** The list of possible error codes could be extended in the future. The client application is expected
            to handle such a case gracefully.

            | Code      | Reason  |
            | --------- | ------- |
            | `E605010` | Invalid combination of truck and transport mode. Check `truck` for valid truck transport modes. |
            | `E605011` | Invalid combination of avoid feature `difficultTurns` or `uTurns` and transport mode. Check
            `avoid` for details. |
            | `E605012` | Invalid combination of transport mode and routing mode. Check `routingMode` for a list of
            supported combinations. |
            | `E605019` | `truck[weightPerAxle]` and `truck[weightPerAxleGroup]` are incompatible |
            | `E605020` | Invalid combination of `radius` and `snapRadius`  |
            | `E605030` | Invalid EV options. Check `ev` for details. |
            | `E605038` | Range based on consumption requires either ev or fuel parameters. Provide one as both parameters
            are missing. |
            | `E605040` | Invalid combination of EV and transport mode. Check `ev` for details. |
            | `E605041` | Invalid combination of EV and routing mode. Check `ev` for details. |
            | `E605048` | Invalid combination of avoid feature `difficultTurns` and truck category `lightTruck`. |
            | `E605070` | Invalid Range Type. |
            | `E605071` | Invalid Range for Range Type - Distance. |
            | `E605072` | Invalid Range for Range Type - Time. |
            | `E605073` | Invalid Shape Max Points. |
            | `E605074` | Invalid Range for Range Type - Consumption.  |
             Example: E605001.
        cause (str): Human-readable explanation for the error Example: The input data in question does not comply with
            validation rules.
        action (str): Human-readable description of the action that can be taken to correct the error Example: Request a
            valid id.
        correlation_id (str): Auto-generated id that univocally identifies the request Example:
            4199533b-6290-41db-8d79-edf4f4019a74.
    """

    title: str
    status: int
    code: str
    cause: str
    action: str
    correlation_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        status = self.status

        code = self.code

        cause = self.cause

        action = self.action

        correlation_id = self.correlation_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "title": title,
            "status": status,
            "code": code,
            "cause": cause,
            "action": action,
            "correlationId": correlation_id,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        status = d.pop("status")

        code = d.pop("code")

        cause = d.pop("cause")

        action = d.pop("action")

        correlation_id = d.pop("correlationId")

        isoline_error_response = cls(
            title=title,
            status=status,
            code=code,
            cause=cause,
            action=action,
            correlation_id=correlation_id,
        )

        isoline_error_response.additional_properties = d
        return isoline_error_response

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
