from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.health_response_ok_schema_status import HealthResponseOKSchemaStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="HealthResponseOKSchema")


@_attrs_define
class HealthResponseOKSchema:
    """Returns the health of the service

    Attributes:
        status (HealthResponseOKSchemaStatus | Unset): Health status of the service:

            * `ok` - the service is operating normally
            * `fail` - the service is currently encountering a failure
    """

    status: HealthResponseOKSchemaStatus | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _status = d.pop("status", UNSET)
        status: HealthResponseOKSchemaStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = HealthResponseOKSchemaStatus(_status)

        health_response_ok_schema = cls(
            status=status,
        )

        health_response_ok_schema.additional_properties = d
        return health_response_ok_schema

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
