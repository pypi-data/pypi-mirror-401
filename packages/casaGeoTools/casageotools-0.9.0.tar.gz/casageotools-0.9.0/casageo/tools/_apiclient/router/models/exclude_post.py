from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.bounding_box_area_with_exceptions import BoundingBoxAreaWithExceptions
    from ..models.corridor_area_with_exceptions import CorridorAreaWithExceptions
    from ..models.encoded_corridor_area_with_exceptions import (
        EncodedCorridorAreaWithExceptions,
    )
    from ..models.encoded_polygon_area_with_exceptions import (
        EncodedPolygonAreaWithExceptions,
    )
    from ..models.polygon_area_with_exceptions import PolygonAreaWithExceptions


T = TypeVar("T", bound="ExcludePost")


@_attrs_define
class ExcludePost:
    """User-specified properties that need to be strictly excluded during route calculation.

    For the general description of the functionality please refer to the `exclude` parameter of the
    query string.

    Passing parameters in the POST body is suggested when the length of the parameters exceeds the
    limitation of the GET request.

        Attributes:
            areas (list[BoundingBoxAreaWithExceptions | CorridorAreaWithExceptions | EncodedCorridorAreaWithExceptions |
                EncodedPolygonAreaWithExceptions | PolygonAreaWithExceptions] | Unset): List of user-defined areas that routes
                should avoid/exclude going through.

                Notes:
                * Maximum count of avoided and excluded polygons and corridors is 20.
                * Maximum total count of avoided and excluded bounding boxes, polygons, corridors, including exceptions, is 250.
                 Example: {'areas': [{'type': 'polygon', 'outer': [{'lat': 52.514414, 'lng': 13.384685}, {'lat': 52.514414,
                'lng': 13.393568}, {'lat': 52.512403, 'lng': 13.393568}, {'lat': 52.512403, 'lng': 13.384685}]}, {'type':
                'encodedPolygon', 'outer': 'BG8mnlkD6-9wZAmrR19DAAlrR'}, {'type': 'boundingBox', 'west': 1.1, 'south': 2.2,
                'east': 3.3, 'north': 4.4, 'exceptions': [{'type': 'polygon', 'outer': [{'lat': 52.514414, 'lng': 13.384685},
                {'lat': 52.514414, 'lng': 13.393568}, {'lat': 52.512403, 'lng': 13.393568}, {'lat': 52.512403, 'lng':
                13.384685}]}, {'type': 'encodedPolygon', 'outer': 'BG8mnlkD6-9wZAmrR19DAAlrR'}]}]}.
    """

    areas: (
        list[
            BoundingBoxAreaWithExceptions
            | CorridorAreaWithExceptions
            | EncodedCorridorAreaWithExceptions
            | EncodedPolygonAreaWithExceptions
            | PolygonAreaWithExceptions
        ]
        | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.bounding_box_area_with_exceptions import (
            BoundingBoxAreaWithExceptions,
        )
        from ..models.corridor_area_with_exceptions import CorridorAreaWithExceptions
        from ..models.encoded_polygon_area_with_exceptions import (
            EncodedPolygonAreaWithExceptions,
        )
        from ..models.polygon_area_with_exceptions import PolygonAreaWithExceptions

        areas: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.areas, Unset):
            areas = []
            for componentsschemas_areas_post_item_data in self.areas:
                componentsschemas_areas_post_item: dict[str, Any]
                if isinstance(
                    componentsschemas_areas_post_item_data,
                    BoundingBoxAreaWithExceptions,
                ):
                    componentsschemas_areas_post_item = (
                        componentsschemas_areas_post_item_data.to_dict()
                    )
                elif isinstance(
                    componentsschemas_areas_post_item_data, PolygonAreaWithExceptions
                ):
                    componentsschemas_areas_post_item = (
                        componentsschemas_areas_post_item_data.to_dict()
                    )
                elif isinstance(
                    componentsschemas_areas_post_item_data,
                    EncodedPolygonAreaWithExceptions,
                ):
                    componentsschemas_areas_post_item = (
                        componentsschemas_areas_post_item_data.to_dict()
                    )
                elif isinstance(
                    componentsschemas_areas_post_item_data, CorridorAreaWithExceptions
                ):
                    componentsschemas_areas_post_item = (
                        componentsschemas_areas_post_item_data.to_dict()
                    )
                else:
                    componentsschemas_areas_post_item = (
                        componentsschemas_areas_post_item_data.to_dict()
                    )

                areas.append(componentsschemas_areas_post_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if areas is not UNSET:
            field_dict["areas"] = areas

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bounding_box_area_with_exceptions import (
            BoundingBoxAreaWithExceptions,
        )
        from ..models.corridor_area_with_exceptions import CorridorAreaWithExceptions
        from ..models.encoded_corridor_area_with_exceptions import (
            EncodedCorridorAreaWithExceptions,
        )
        from ..models.encoded_polygon_area_with_exceptions import (
            EncodedPolygonAreaWithExceptions,
        )
        from ..models.polygon_area_with_exceptions import PolygonAreaWithExceptions

        d = dict(src_dict)
        _areas = d.pop("areas", UNSET)
        areas: (
            list[
                BoundingBoxAreaWithExceptions
                | CorridorAreaWithExceptions
                | EncodedCorridorAreaWithExceptions
                | EncodedPolygonAreaWithExceptions
                | PolygonAreaWithExceptions
            ]
            | Unset
        ) = UNSET
        if _areas is not UNSET:
            areas = []
            for componentsschemas_areas_post_item_data in _areas:

                def _parse_componentsschemas_areas_post_item(
                    data: object,
                ) -> (
                    BoundingBoxAreaWithExceptions
                    | CorridorAreaWithExceptions
                    | EncodedCorridorAreaWithExceptions
                    | EncodedPolygonAreaWithExceptions
                    | PolygonAreaWithExceptions
                ):
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_area_post_type_0 = (
                            BoundingBoxAreaWithExceptions.from_dict(data)
                        )

                        return componentsschemas_area_post_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_area_post_type_1 = (
                            PolygonAreaWithExceptions.from_dict(data)
                        )

                        return componentsschemas_area_post_type_1
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_area_post_type_2 = (
                            EncodedPolygonAreaWithExceptions.from_dict(data)
                        )

                        return componentsschemas_area_post_type_2
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_area_post_type_3 = (
                            CorridorAreaWithExceptions.from_dict(data)
                        )

                        return componentsschemas_area_post_type_3
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_area_post_type_4 = (
                        EncodedCorridorAreaWithExceptions.from_dict(data)
                    )

                    return componentsschemas_area_post_type_4

                componentsschemas_areas_post_item = (
                    _parse_componentsschemas_areas_post_item(
                        componentsschemas_areas_post_item_data
                    )
                )

                areas.append(componentsschemas_areas_post_item)

        exclude_post = cls(
            areas=areas,
        )

        exclude_post.additional_properties = d
        return exclude_post

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
