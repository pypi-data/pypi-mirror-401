from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transit_departure import TransitDeparture
    from ..models.transit_transport import TransitTransport


T = TypeVar("T", bound="TransitStop")


@_attrs_define
class TransitStop:
    """A transit stop of the route

    Attributes:
        departure (TransitDeparture): Transit departure
        duration (int | Unset): Stop duration. If not set the vehicle departs as soon as people are on board. Default:
            0. Example: 198.
        transport (TransitTransport | Unset): Transit transport information.
        offset (int | Unset): The position of the stop on the polyline.
        attributes (list[str] | Unset): **NOTE:** As it is possible that new attributes are supported in the future,
            unknown attributes should be ignored.
    """

    departure: TransitDeparture
    duration: int | Unset = 0
    transport: TransitTransport | Unset = UNSET
    offset: int | Unset = UNSET
    attributes: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        departure = self.departure.to_dict()

        duration = self.duration

        transport: dict[str, Any] | Unset = UNSET
        if not isinstance(self.transport, Unset):
            transport = self.transport.to_dict()

        offset = self.offset

        attributes: list[str] | Unset = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "departure": departure,
        })
        if duration is not UNSET:
            field_dict["duration"] = duration
        if transport is not UNSET:
            field_dict["transport"] = transport
        if offset is not UNSET:
            field_dict["offset"] = offset
        if attributes is not UNSET:
            field_dict["attributes"] = attributes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transit_departure import TransitDeparture
        from ..models.transit_transport import TransitTransport

        d = dict(src_dict)
        departure = TransitDeparture.from_dict(d.pop("departure"))

        duration = d.pop("duration", UNSET)

        _transport = d.pop("transport", UNSET)
        transport: TransitTransport | Unset
        if isinstance(_transport, Unset):
            transport = UNSET
        else:
            transport = TransitTransport.from_dict(_transport)

        offset = d.pop("offset", UNSET)

        attributes = cast(list[str], d.pop("attributes", UNSET))

        transit_stop = cls(
            departure=departure,
            duration=duration,
            transport=transport,
            offset=offset,
            attributes=attributes,
        )

        transit_stop.additional_properties = d
        return transit_stop

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
