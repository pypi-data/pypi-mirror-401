from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PedestrianTransport")


@_attrs_define
class PedestrianTransport:
    """Information about a transport

    Attributes:
        mode (str): Extensible enum: `pedestrian` `...`
            Pedestrian mode of transport.

            Since the supported pedestrian modes may be extended in the future, the pedestrian mode should be hidden when an
            unknown mode is encountered.
        name (str | Unset): Name of the transport, e.g., the name of a ferry or train.
    """

    mode: str
    name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "mode": mode,
        })
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = d.pop("mode")

        name = d.pop("name", UNSET)

        pedestrian_transport = cls(
            mode=mode,
            name=name,
        )

        pedestrian_transport.additional_properties = d
        return pedestrian_transport

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
