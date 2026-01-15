from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BrowseBody")


@_attrs_define
class BrowseBody:
    r"""
    Attributes:
        route (str | Unset): **BETA**

            Select within a geographic corridor. This is a hard filter. Results will be returned if they are located within
            the specified area.

            A `route` is defined by a [Flexible Polyline Encoding](https://github.com/heremaps/flexible-polyline),
             followed by an optional width, represented by a sub-parameter "w".

            Format: `{route};w={width}`

            In regular expression syntax, the values of `route` are formatted as follows:

            `[a-zA-Z0-9_-]+(;w=\d+)?`

            "[a-zA-Z0-9._-]+" is the encoded flexible polyline.

            "w=\d+" is the optional width. The width is specified in meters from the center of the path. If no width is
            provided, the default is 1000 meters.

            Type: `{Flexible Polyline Encoding};w={integer}`

            The following constraints apply:
             * A `route` MUST contain at least two points (one segment).
             * A `route` MUST NOT contain more than 2,000 points.
             * A `route` MUST NOT have a width of more than 50,000 meters.

            Examples:
             * `BFoz5xJ67i1B1B7PzIhaxL7Y`
             * `BFoz5xJ67i1B1B7PzIhaxL7Y;w=5000`
             * `BlD05xgKuy2xCCx9B7vUCl0OhnRC54EqSCzpEl-HCxjD3pBCiGnyGCi2CvwFCsgD3nDC4vB6eC;w=2000`

            Note: The last example above can be decoded (using the Python class [here](https://github.com/heremaps/flexible-
            polyline/tree/master/python) as follows:

            ```
            >>> import flexpolyline
            >>> polyline = 'BlD05xgKuy2xCCx9B7vUCl0OhnRC54EqSCzpEl-HCxjD3pBCiGnyGCi2CvwFCsgD3nDC4vB6eC'
            >>> flexpolyline.decode(polyline)
            [(52.51994, 13.38663, 1.0), (52.51009, 13.28169, 2.0), (52.43518, 13.19352, 3.0), (52.41073, 13.19645, 4.0),
             (52.38871, 13.15578, 5.0), (52.37278, 13.1491, 6.0), (52.37375, 13.11546, 7.0), (52.38752, 13.08722, 8.0),
             (52.40294, 13.07062, 9.0), (52.41058, 13.07555, 10.0)]
            ```
    """

    route: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        route = self.route

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if route is not UNSET:
            field_dict["route"] = route

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        route = d.pop("route", UNSET)

        browse_body = cls(
            route=route,
        )

        browse_body.additional_properties = d
        return browse_body

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
