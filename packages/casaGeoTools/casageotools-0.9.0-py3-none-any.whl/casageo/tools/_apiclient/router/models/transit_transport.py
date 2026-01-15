from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TransitTransport")


@_attrs_define
class TransitTransport:
    """Transit transport information.

    Attributes:
        mode (str): Extensible enum: `highSpeedTrain` `intercityTrain` `interRegionalTrain` `regionalTrain` `cityTrain`
            `bus` `ferry` `subway` `lightRail` `privateBus` `inclined` `aerial` `busRapid` `monorail` `carShuttleTrain`
            `flight` `spaceship` `...`
            Transit mode of transport in the route response
        name (str | Unset): Transit line name Example: U2.
        headsign (str | Unset): Transit line headsign
        category (str | Unset): Human readable transport category (such as Bus, Gondola, Tram, Train, ...) Example:
            Train.
        color (str | Unset):  Example: #FF0000.
        text_color (str | Unset):  Example: #FF0000.
        short_name (str | Unset): Short name of a transit line. Example: U2.
        long_name (str | Unset): Long name of a transit line. Example: Pankow - Ruhleben.
    """

    mode: str
    name: str | Unset = UNSET
    headsign: str | Unset = UNSET
    category: str | Unset = UNSET
    color: str | Unset = UNSET
    text_color: str | Unset = UNSET
    short_name: str | Unset = UNSET
    long_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode

        name = self.name

        headsign = self.headsign

        category = self.category

        color = self.color

        text_color = self.text_color

        short_name = self.short_name

        long_name = self.long_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "mode": mode,
        })
        if name is not UNSET:
            field_dict["name"] = name
        if headsign is not UNSET:
            field_dict["headsign"] = headsign
        if category is not UNSET:
            field_dict["category"] = category
        if color is not UNSET:
            field_dict["color"] = color
        if text_color is not UNSET:
            field_dict["textColor"] = text_color
        if short_name is not UNSET:
            field_dict["shortName"] = short_name
        if long_name is not UNSET:
            field_dict["longName"] = long_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = d.pop("mode")

        name = d.pop("name", UNSET)

        headsign = d.pop("headsign", UNSET)

        category = d.pop("category", UNSET)

        color = d.pop("color", UNSET)

        text_color = d.pop("textColor", UNSET)

        short_name = d.pop("shortName", UNSET)

        long_name = d.pop("longName", UNSET)

        transit_transport = cls(
            mode=mode,
            name=name,
            headsign=headsign,
            category=category,
            color=color,
            text_color=text_color,
            short_name=short_name,
            long_name=long_name,
        )

        transit_transport.additional_properties = d
        return transit_transport

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
