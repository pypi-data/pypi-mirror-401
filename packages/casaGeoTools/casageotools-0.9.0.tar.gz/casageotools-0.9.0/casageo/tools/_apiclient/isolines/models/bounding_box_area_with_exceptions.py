from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.bounding_box_area import BoundingBoxArea
    from ..models.corridor_area import CorridorArea
    from ..models.encoded_corridor_area import EncodedCorridorArea
    from ..models.encoded_polygon_area import EncodedPolygonArea
    from ..models.polygon_area import PolygonArea


T = TypeVar("T", bound="BoundingBoxAreaWithExceptions")


@_attrs_define
class BoundingBoxAreaWithExceptions:
    """A bounding box defined by two longitudes and two latitudes.
    Can be expanded to include excepted areas that are excluded from the current bounding box area.

        Attributes:
            type_ (str):  Example: boundingBox.
            north (float): Latitude in WGS-84 degrees of the northern boundary of the box. Example: 30.0.
            south (float): Latitude in WGS-84 degrees of the southern boundary of the box. Example: 30.0.
            east (float): Longitude in WGS-84 degrees of the eastern boundary of the box Example: 30.0.
            west (float): Longitude in WGS-84 degrees of the western boundary of the box. Example: 30.0.
            exceptions (list[BoundingBoxArea | CorridorArea | EncodedCorridorArea | EncodedPolygonArea | PolygonArea] |
                Unset): Optional list of areas to exclude from avoidance.
    """

    type_: str
    north: float
    south: float
    east: float
    west: float
    exceptions: (
        list[
            BoundingBoxArea
            | CorridorArea
            | EncodedCorridorArea
            | EncodedPolygonArea
            | PolygonArea
        ]
        | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.bounding_box_area import BoundingBoxArea
        from ..models.corridor_area import CorridorArea
        from ..models.encoded_polygon_area import EncodedPolygonArea
        from ..models.polygon_area import PolygonArea

        type_ = self.type_

        north = self.north

        south = self.south

        east = self.east

        west = self.west

        exceptions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.exceptions, Unset):
            exceptions = []
            for exceptions_item_data in self.exceptions:
                exceptions_item: dict[str, Any]
                if isinstance(exceptions_item_data, BoundingBoxArea):
                    exceptions_item = exceptions_item_data.to_dict()
                elif isinstance(exceptions_item_data, PolygonArea):
                    exceptions_item = exceptions_item_data.to_dict()
                elif isinstance(exceptions_item_data, EncodedPolygonArea):
                    exceptions_item = exceptions_item_data.to_dict()
                elif isinstance(exceptions_item_data, CorridorArea):
                    exceptions_item = exceptions_item_data.to_dict()
                else:
                    exceptions_item = exceptions_item_data.to_dict()

                exceptions.append(exceptions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "north": north,
            "south": south,
            "east": east,
            "west": west,
        })
        if exceptions is not UNSET:
            field_dict["exceptions"] = exceptions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bounding_box_area import BoundingBoxArea
        from ..models.corridor_area import CorridorArea
        from ..models.encoded_corridor_area import EncodedCorridorArea
        from ..models.encoded_polygon_area import EncodedPolygonArea
        from ..models.polygon_area import PolygonArea

        d = dict(src_dict)
        type_ = d.pop("type")

        north = d.pop("north")

        south = d.pop("south")

        east = d.pop("east")

        west = d.pop("west")

        _exceptions = d.pop("exceptions", UNSET)
        exceptions: (
            list[
                BoundingBoxArea
                | CorridorArea
                | EncodedCorridorArea
                | EncodedPolygonArea
                | PolygonArea
            ]
            | Unset
        ) = UNSET
        if _exceptions is not UNSET:
            exceptions = []
            for exceptions_item_data in _exceptions:

                def _parse_exceptions_item(
                    data: object,
                ) -> (
                    BoundingBoxArea
                    | CorridorArea
                    | EncodedCorridorArea
                    | EncodedPolygonArea
                    | PolygonArea
                ):
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_area_type_0 = BoundingBoxArea.from_dict(data)

                        return componentsschemas_area_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_area_type_1 = PolygonArea.from_dict(data)

                        return componentsschemas_area_type_1
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_area_type_2 = EncodedPolygonArea.from_dict(
                            data
                        )

                        return componentsschemas_area_type_2
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_area_type_3 = CorridorArea.from_dict(data)

                        return componentsschemas_area_type_3
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_area_type_4 = EncodedCorridorArea.from_dict(data)

                    return componentsschemas_area_type_4

                exceptions_item = _parse_exceptions_item(exceptions_item_data)

                exceptions.append(exceptions_item)

        bounding_box_area_with_exceptions = cls(
            type_=type_,
            north=north,
            south=south,
            east=east,
            west=west,
            exceptions=exceptions,
        )

        bounding_box_area_with_exceptions.additional_properties = d
        return bounding_box_area_with_exceptions

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
