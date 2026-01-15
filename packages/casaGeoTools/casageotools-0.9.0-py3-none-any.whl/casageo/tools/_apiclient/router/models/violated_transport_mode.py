from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.violated_transport_mode_type import ViolatedTransportModeType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ViolatedTransportMode")


@_attrs_define
class ViolatedTransportMode:
    """Contains details about the violated transport mode on this road, such as trucks being generally forbidden.

    Attributes:
        type_ (ViolatedTransportModeType): Detail type. Each type of detail might contain extra attributes.

            **NOTE:** The list of possible detail types may be extended in the future.
            The client application is expected to handle such a case gracefully.
        title (str | Unset): Detail title
        cause (str | Unset): Cause of the notice
    """

    type_: ViolatedTransportModeType
    title: str | Unset = UNSET
    cause: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        title = self.title

        cause = self.cause

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
        })
        if title is not UNSET:
            field_dict["title"] = title
        if cause is not UNSET:
            field_dict["cause"] = cause

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = ViolatedTransportModeType(d.pop("type"))

        title = d.pop("title", UNSET)

        cause = d.pop("cause", UNSET)

        violated_transport_mode = cls(
            type_=type_,
            title=title,
            cause=cause,
        )

        violated_transport_mode.additional_properties = d
        return violated_transport_mode

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
