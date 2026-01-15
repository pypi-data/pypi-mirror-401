from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.access_point_place import AccessPointPlace
    from ..models.charging_station_place import ChargingStationPlace
    from ..models.docking_station_place import DockingStationPlace
    from ..models.parking_lot_place import ParkingLotPlace
    from ..models.place import Place
    from ..models.station_place import StationPlace


T = TypeVar("T", bound="PedestrianDeparture")


@_attrs_define
class PedestrianDeparture:
    """Departure of pedestrian

    Attributes:
        place (AccessPointPlace | ChargingStationPlace | DockingStationPlace | ParkingLotPlace | Place | StationPlace):
            Place used in pedestrian routing
        time (datetime.datetime | Unset): **RFC 3339**, section 5.6 as defined by either `date-time` or `date-only` 'T'
            `partial-time` (ie no time-offset).
    """

    place: (
        AccessPointPlace
        | ChargingStationPlace
        | DockingStationPlace
        | ParkingLotPlace
        | Place
        | StationPlace
    )
    time: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.access_point_place import AccessPointPlace
        from ..models.charging_station_place import ChargingStationPlace
        from ..models.parking_lot_place import ParkingLotPlace
        from ..models.place import Place
        from ..models.station_place import StationPlace

        place: dict[str, Any]
        if isinstance(self.place, Place):
            place = self.place.to_dict()
        elif isinstance(self.place, StationPlace):
            place = self.place.to_dict()
        elif isinstance(self.place, AccessPointPlace):
            place = self.place.to_dict()
        elif isinstance(self.place, ParkingLotPlace):
            place = self.place.to_dict()
        elif isinstance(self.place, ChargingStationPlace):
            place = self.place.to_dict()
        else:
            place = self.place.to_dict()

        time: str | Unset = UNSET
        if not isinstance(self.time, Unset):
            time = self.time.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "place": place,
        })
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.access_point_place import AccessPointPlace
        from ..models.charging_station_place import ChargingStationPlace
        from ..models.docking_station_place import DockingStationPlace
        from ..models.parking_lot_place import ParkingLotPlace
        from ..models.place import Place
        from ..models.station_place import StationPlace

        d = dict(src_dict)

        def _parse_place(
            data: object,
        ) -> (
            AccessPointPlace
            | ChargingStationPlace
            | DockingStationPlace
            | ParkingLotPlace
            | Place
            | StationPlace
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_pedestrian_place_type_0 = Place.from_dict(data)

                return componentsschemas_pedestrian_place_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_pedestrian_place_type_1 = StationPlace.from_dict(data)

                return componentsschemas_pedestrian_place_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_pedestrian_place_type_2 = AccessPointPlace.from_dict(
                    data
                )

                return componentsschemas_pedestrian_place_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_pedestrian_place_type_3 = ParkingLotPlace.from_dict(
                    data
                )

                return componentsschemas_pedestrian_place_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_pedestrian_place_type_4 = (
                    ChargingStationPlace.from_dict(data)
                )

                return componentsschemas_pedestrian_place_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_pedestrian_place_type_5 = DockingStationPlace.from_dict(
                data
            )

            return componentsschemas_pedestrian_place_type_5

        place = _parse_place(d.pop("place"))

        _time = d.pop("time", UNSET)
        time: datetime.datetime | Unset
        if isinstance(_time, Unset):
            time = UNSET
        else:
            time = isoparse(_time)

        pedestrian_departure = cls(
            place=place,
            time=time,
        )

        pedestrian_departure.additional_properties = d
        return pedestrian_departure

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
