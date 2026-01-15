from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.place import Place
    from ..models.station_place import StationPlace


T = TypeVar("T", bound="TransitDeparture")


@_attrs_define
class TransitDeparture:
    """Transit departure

    Attributes:
        place (Place | StationPlace): Departure/arrival location
        time (datetime.datetime | Unset): **RFC 3339**, section 5.6 as defined by either `date-time` or `date-only` 'T'
            `partial-time` (ie no time-offset).
        charge (float | Unset): Vehicle battery charge, specified in kilowatt-hours (kWh).
            **NOTE:** This is only returned in ferry sections when a vehicle route requests battery consumption.
    """

    place: Place | StationPlace
    time: datetime.datetime | Unset = UNSET
    charge: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.place import Place

        place: dict[str, Any]
        if isinstance(self.place, Place):
            place = self.place.to_dict()
        else:
            place = self.place.to_dict()

        time: str | Unset = UNSET
        if not isinstance(self.time, Unset):
            time = self.time.isoformat()

        charge = self.charge

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "place": place,
        })
        if time is not UNSET:
            field_dict["time"] = time
        if charge is not UNSET:
            field_dict["charge"] = charge

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.place import Place
        from ..models.station_place import StationPlace

        d = dict(src_dict)

        def _parse_place(data: object) -> Place | StationPlace:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_transit_departure_place_type_0 = Place.from_dict(data)

                return componentsschemas_transit_departure_place_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_transit_departure_place_type_1 = StationPlace.from_dict(
                data
            )

            return componentsschemas_transit_departure_place_type_1

        place = _parse_place(d.pop("place"))

        _time = d.pop("time", UNSET)
        time: datetime.datetime | Unset
        if isinstance(_time, Unset):
            time = UNSET
        else:
            time = isoparse(_time)

        charge = d.pop("charge", UNSET)

        transit_departure = cls(
            place=place,
            time=time,
            charge=charge,
        )

        transit_departure.additional_properties = d
        return transit_departure

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
