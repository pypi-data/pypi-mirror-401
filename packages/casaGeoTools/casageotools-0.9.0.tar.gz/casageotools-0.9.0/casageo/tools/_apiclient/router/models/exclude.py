from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Exclude")


@_attrs_define
class Exclude:
    """Options to exclude strictly during the route calculation.

    Attributes:
        countries (str | Unset): A comma separated list of three-letter country codes (ISO-3166-1 alpha-3 code) that
            routes will exclude.
            - Format: `{country1}[,country2][,country...]`
              + `{country}` - Country code according to (ISO-3166-1 alpha-3)
            - Example: `CZE,SVK` - exclude Czechia and Slovakia from routing.

            Note - Exclude countries guarantees exclusion, but doesn't guarantee finding a route.
        states (str | Unset): A pipe separated list of country-aggregated state codes.

            - Format: `{country1}:{state1.1}[,state1.2][,state1.3]...[|{country2}:{state2.1}[,state2.2]]...`
              + `{country}` - Country code according to (ISO-3166-1 alpha-3)
              + `{state}`   - State code part according to (ISO 3166-2)
            - Examples:
              + `USA:NY,PA`       - exclude USA's New York and Pennsylvania states
              + `USA:NY,PA|CAN:QC`- exclude USA's New York, Pennsylvania states and Canada's Quebec province
            - Notes:
              + Exclude states guarantees exclusion, but doesn't guarantee finding a route.
              + Some countries don't have the state code data available for them, so the states in those countries won't be
            excluded.
        areas (str | Unset): A pipe separated list of user-defined areas that routes should avoid/exclude going through.

            Notes:
            * Maximum count of avoided and excluded polygons and corridors is 20.
            * Maximum total count of avoided and excluded bounding boxes, polygons, corridors, including exceptions, is 250.

            Format: `{area1}[!exception1.1[!exception1.2...]]|{area2}[!exception2.1[!exception2.2...]]|{area3}[!exception3.1
            [!exception3.2...]]...`

            Supported areas:
            * Bounding box - A rectangular area on earth defined by a comma separated list of two latitude and two longitude
            values.
              - Format: `bbox:{west},{south},{east},{north}`
                + `{west}`  - Longitude value of the westernmost point of the area.
                + `{south}` - Latitude value of the southernmost point of the area.
                + `{east}`  - Longitude value of the easternmost point of the area.
                + `{north}` - Latitude value of the northernmost point of the area.
              - Example: `bbox:13.082,52.416,13.628,52.626` - Bounding box of Berlin
            * Polygon - A polygon on earth which defines area.
              Possible formats:
              1) As list of geopoints.
                - Format: `polygon:{lat},{lon};{lat},{lon};{lat},{lon}...`
                  + `{lat}` - Latitude
                  + `{lon}` - Longitude
                - Example: `polygon:52.416,13.082;52.626,13.628;52.916,13.482` - Polygon in Berlin
              2) As [Flexible Polyline](https://github.com/heremaps/flexible-polyline) Encoding.
                - Support only 2D polyline (without `elevation` specified).
                - Format: `polygon:{encoded_polyline}`
                  + `{encoded_polyline}` - encoded [Flexible Polyline](https://github.com/heremaps/flexible-polyline)
                - Example: `polygon:BF05xgKuy2xCx9B7vUl0OhnR54EqSzpEl-HxjD3pBiGnyGi2CvwFsgD3nD4vB6e`
            * Corridor - A polyline with a specified radius (integer, in meters) that defines width of corridor area.
              Possible formats:
              1) As a list of geopoints that defines a polyline and a radius that defines an area around the polyline.
                - Format: `corridor:{lat},{lon};{lat},{lon};{lat},{lon}...;r={radius}`
                - Example: `corridor:52.416,13.082;52.626,13.628;52.916,13.482;r=1000`
              2) As [Flexible Polyline](https://github.com/heremaps/flexible-polyline) encoding and a radius that defines an
            area around the polyline.
                - Supports only 2D polyline (without `elevation` specified).
                - Format: `corridor:{encoded_polyline};r={radius}`
                  + `{encoded_polyline}` - encoded [Flexible Polyline](https://github.com/heremaps/flexible-polyline)
                - Example: `corridor:BF05xgKuy2xCx9B7vUl0OhnR54EqSzpEl-HxjD3pBiGnyGi2CvwFsgD3nD4vB6e;r=1000`

            * Exception - area to exclude from avoidance. Any area type can be specified. Any area type can be used as an
            exception. Multiple exceptions can be specified for each area.
              - Format: `{area to avoid/exclude}!exception={area}`
              - Example: `bbox:13.082,52.416,13.628,52.626!exception=polygon:BF05xgKuy2xCx9B7vUl0OhnR54EqSzpEl-
            HxjD3pBiGnyGi2CvwFsgD3nD4vB6e!exception=bbox:13.082,52.416,13.628,52.626`

              Notes:
              * Maximum count of avoided and excluded polygons and corridors is 20.
              * Maximum total count of avoided and excluded bounding boxes, polygons, corridors, including exceptions, is
            250.
              * Minimum count of coordinates in one polygon is 3
              * Minimum count of coordinates in any single corridor is 2.
              * Maximum count of coordinates in one polygon or in one corridor is 100
              * The polygon is closed automatically, there is no need to duplicate the first point as the last one.
              * Self-intersecting polygons are not supported.
    """

    countries: str | Unset = UNSET
    states: str | Unset = UNSET
    areas: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        countries = self.countries

        states = self.states

        areas = self.areas

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if countries is not UNSET:
            field_dict["countries"] = countries
        if states is not UNSET:
            field_dict["states"] = states
        if areas is not UNSET:
            field_dict["areas"] = areas

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        countries = d.pop("countries", UNSET)

        states = d.pop("states", UNSET)

        areas = d.pop("areas", UNSET)

        exclude = cls(
            countries=countries,
            states=states,
            areas=areas,
        )

        exclude.additional_properties = d
        return exclude

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
