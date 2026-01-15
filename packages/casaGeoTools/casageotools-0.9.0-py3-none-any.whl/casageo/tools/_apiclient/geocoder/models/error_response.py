from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ErrorResponse")


@_attrs_define
class ErrorResponse:
    """
    Attributes:
        status (int): The HTTP status code
        title (str): Human-readable error description
        correlation_id (str): Auto-generated ID univocally identifying this request
        request_id (str): Request identifier provided by the user
        code (str | Unset): Error code
        cause (str | Unset): Human-readable explanation for the error
        action (str | Unset): Human-readable action for the user
    """

    status: int
    title: str
    correlation_id: str
    request_id: str
    code: str | Unset = UNSET
    cause: str | Unset = UNSET
    action: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        title = self.title

        correlation_id = self.correlation_id

        request_id = self.request_id

        code = self.code

        cause = self.cause

        action = self.action

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "status": status,
            "title": title,
            "correlationId": correlation_id,
            "requestId": request_id,
        })
        if code is not UNSET:
            field_dict["code"] = code
        if cause is not UNSET:
            field_dict["cause"] = cause
        if action is not UNSET:
            field_dict["action"] = action

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = d.pop("status")

        title = d.pop("title")

        correlation_id = d.pop("correlationId")

        request_id = d.pop("requestId")

        code = d.pop("code", UNSET)

        cause = d.pop("cause", UNSET)

        action = d.pop("action", UNSET)

        error_response = cls(
            status=status,
            title=title,
            correlation_id=correlation_id,
            request_id=request_id,
            code=code,
            cause=cause,
            action=action,
        )

        error_response.additional_properties = d
        return error_response

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
