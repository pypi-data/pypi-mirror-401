from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="NotAllowed")


@_attrs_define
class NotAllowed:
    """Not Allowed, actions not permitted by server.

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
            | `E605101` | Credentials not allowed for calculating routes in Japan. |
             Example: E600101.
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

        not_allowed = cls(
            title=title,
            status=status,
            code=code,
            cause=cause,
            action=action,
            correlation_id=correlation_id,
        )

        not_allowed.additional_properties = d
        return not_allowed

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
