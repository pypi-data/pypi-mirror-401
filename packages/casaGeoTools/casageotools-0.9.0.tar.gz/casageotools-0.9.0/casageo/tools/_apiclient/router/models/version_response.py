from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_version import DataVersion


T = TypeVar("T", bound="VersionResponse")


@_attrs_define
class VersionResponse:
    """Returns the versions of the service components.

    Attributes:
        api_version (str): The current version of the API. Example: 8.18.0.
        service_version (str | Unset): The current version of the service. Example: 2022-12-15-b706cc8c-9057409.
        data_versions (list[DataVersion] | Unset): Returns the versions of data sets used by the service.
    """

    api_version: str
    service_version: str | Unset = UNSET
    data_versions: list[DataVersion] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api_version = self.api_version

        service_version = self.service_version

        data_versions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data_versions, Unset):
            data_versions = []
            for data_versions_item_data in self.data_versions:
                data_versions_item = data_versions_item_data.to_dict()
                data_versions.append(data_versions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "apiVersion": api_version,
        })
        if service_version is not UNSET:
            field_dict["serviceVersion"] = service_version
        if data_versions is not UNSET:
            field_dict["dataVersions"] = data_versions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data_version import DataVersion

        d = dict(src_dict)
        api_version = d.pop("apiVersion")

        service_version = d.pop("serviceVersion", UNSET)

        _data_versions = d.pop("dataVersions", UNSET)
        data_versions: list[DataVersion] | Unset = UNSET
        if _data_versions is not UNSET:
            data_versions = []
            for data_versions_item_data in _data_versions:
                data_versions_item = DataVersion.from_dict(data_versions_item_data)

                data_versions.append(data_versions_item)

        version_response = cls(
            api_version=api_version,
            service_version=service_version,
            data_versions=data_versions,
        )

        version_response.additional_properties = d
        return version_response

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
