from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Connection")


@_attrs_define
class Connection:
    """Connection represents the geometry of special links that were reached but not included in the components.
    These links are connections like ferries.

        Attributes:
            from_polygon_index (int): Index of start component of the connection
            to_polygon_index (int): Index of end component of the connection
            polyline (str): Line string in [Flexible Polyline](https://github.com/heremaps/flexible-polyline) format.
                Coordinates are in the WGS84 coordinate system, including `Elevation` (if present). Example:
                A05xgKuy2xCx9B7vUl0OhnR54EqSzpEl-HxjD3pBiGnyGi2CvwFsgD3nD4vB6e.
    """

    from_polygon_index: int
    to_polygon_index: int
    polyline: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_polygon_index = self.from_polygon_index

        to_polygon_index = self.to_polygon_index

        polyline = self.polyline

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "fromPolygonIndex": from_polygon_index,
            "toPolygonIndex": to_polygon_index,
            "polyline": polyline,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        from_polygon_index = d.pop("fromPolygonIndex")

        to_polygon_index = d.pop("toPolygonIndex")

        polyline = d.pop("polyline")

        connection = cls(
            from_polygon_index=from_polygon_index,
            to_polygon_index=to_polygon_index,
            polyline=polyline,
        )

        connection.additional_properties = d
        return connection

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
