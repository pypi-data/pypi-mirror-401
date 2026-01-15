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


T = TypeVar("T", bound="EncodedPolygonAreaWithExceptions")


@_attrs_define
class EncodedPolygonAreaWithExceptions:
    """A polygon defined as a [Flexible Polyline](https://github.com/heremaps/flexible-polyline) encoded string.
    Can be expanded to include excepted areas that are excluded from the current polygon area.

        Attributes:
            type_ (str):  Example: encodedPolygon.
            outer (str): [Flexible Polyline](https://github.com/heremaps/flexible-polyline) that defines the outline of the
                polygon.
                Notes:
                * Support only 2D polyline (without `elevation` specified).
                * Minimum count of vertices in polygon is 3.
                * Maximum count of vertices in polygon is 16.
                 Example: BFoz5xJ67i1B1B7PzIhaxL7Y.
            exceptions (list[BoundingBoxArea | CorridorArea | EncodedCorridorArea | EncodedPolygonArea | PolygonArea] |
                Unset): Optional list of areas to exclude from avoidance.
    """

    type_: str
    outer: str
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

        outer = self.outer

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
            "outer": outer,
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

        outer = d.pop("outer")

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

        encoded_polygon_area_with_exceptions = cls(
            type_=type_,
            outer=outer,
            exceptions=exceptions,
        )

        encoded_polygon_area_with_exceptions.additional_properties = d
        return encoded_polygon_area_with_exceptions

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
