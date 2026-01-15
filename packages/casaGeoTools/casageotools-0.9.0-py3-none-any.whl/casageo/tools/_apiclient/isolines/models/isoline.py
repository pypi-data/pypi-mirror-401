from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.connection import Connection
    from ..models.polygon import Polygon
    from ..models.response_range import ResponseRange


T = TypeVar("T", bound="Isoline")


@_attrs_define
class Isoline:
    """An isoline for the specified range parameter.

    Attributes:
        range_ (ResponseRange): Range specified in terms of distance, travel time or energy consumption.
        polygons (list[Polygon]): A set of multiple polygons.
        connections (list[Connection] | Unset): Connections represent the geometry of special links that were reached
            but not included in the components.
            These links are connections like ferries.
    """

    range_: ResponseRange
    polygons: list[Polygon]
    connections: list[Connection] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        range_ = self.range_.to_dict()

        polygons = []
        for componentsschemas_multi_polygon_item_data in self.polygons:
            componentsschemas_multi_polygon_item = (
                componentsschemas_multi_polygon_item_data.to_dict()
            )
            polygons.append(componentsschemas_multi_polygon_item)

        connections: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.connections, Unset):
            connections = []
            for connections_item_data in self.connections:
                connections_item = connections_item_data.to_dict()
                connections.append(connections_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "range": range_,
            "polygons": polygons,
        })
        if connections is not UNSET:
            field_dict["connections"] = connections

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.connection import Connection
        from ..models.polygon import Polygon
        from ..models.response_range import ResponseRange

        d = dict(src_dict)
        range_ = ResponseRange.from_dict(d.pop("range"))

        polygons = []
        _polygons = d.pop("polygons")
        for componentsschemas_multi_polygon_item_data in _polygons:
            componentsschemas_multi_polygon_item = Polygon.from_dict(
                componentsschemas_multi_polygon_item_data
            )

            polygons.append(componentsschemas_multi_polygon_item)

        _connections = d.pop("connections", UNSET)
        connections: list[Connection] | Unset = UNSET
        if _connections is not UNSET:
            connections = []
            for connections_item_data in _connections:
                connections_item = Connection.from_dict(connections_item_data)

                connections.append(connections_item)

        isoline = cls(
            range_=range_,
            polygons=polygons,
            connections=connections,
        )

        isoline.additional_properties = d
        return isoline

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
