from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Avoid")


@_attrs_define
class Avoid:
    """
    Attributes:
        features (str | Unset): A comma-separated list of features that routes should avoid.

            * `seasonalClosure`
            * `tollRoad`: This option avoids roads that have an applicable toll.
            * `controlledAccessHighway`
            * `ferry`
            * `carShuttleTrain`
            * `tunnel`
            * `dirtRoad`
            * `difficultTurns`: This option avoids difficult turns, sharp turns and U-turns on multi-digitized roads,
            intersections and stopover-type waypoints. It is only supported for the `truck` transport mode.
              **Disclaimer: This parameter is currently in beta release. Depending on your location and vehicle type, the
            outcome might not be according to the expectations. Please test the behavior of this feature for your use case
            before enabling it.**
            * `uTurns`: This option avoids U-turns on multi-digitized roads, intersections, stopover-type waypoints. U-turns
            on mini roundabouts (roundabouts with a small turn radius, which are difficult for long vehicles to navigate)
            are avoided when `transportMode = truck`. This option is not supported for pedestrian, bicycle and scooter
            transport modes.

            **Notes**
              - It may not always be possible to find a route which avoids the requested feature. A route may not be
            returned, or one may be returned with a critical notice.
              - Using `avoid[features]=tollRoad` does not optimize the route to reduce the overall toll costs.
              - Using `avoid[features]=tollRoad` is not recommended for large vehicles, e.g., trucks or buses. Even if a
            route is suggested, it may use smaller roads, where driving such vehicles is not convenient or safe.
              - Using `avoid[features]=difficultTurns` together with `avoid[features]=controlledAccessHighway` or
            `avoid[features]=tollRoads` is not recommended, as it may lead to routes which could include difficult turns.
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
        segments (str | Unset): A comma separated list of segment identifiers that routes should avoid going through.

            Each entry has the following structure:
            `{segmentId}(#{direction})?`

            The individual parts are:
            * segmentId: The identifier of the referenced topology segment inside the catalog, example:
            `here:cm:segment:207551710`
            * direction (optional): Either '*' for bidirectional (default), '+' for positive direction, or '-' for negative
            direction

            Example of a parameter value excluding two segments:
            `here:cm:segment:207551710#+,here:cm:segment:76771992#*`

            **Note**: Maximum number of penalized segments in one request should not be greater than 1000.
                      "Penalized segments" refers to segments that either have a restriction on maximum baseSpeed with
            `maxSpeedOnSegment`
                      or avoided with `avoid[segments]`
        zone_categories (str | Unset): Specifies a list of categories of zones which routes should avoid going through.

            Format: `Categories[ZoneCategoryOptions]`

            * Categories: `{cat1},{cat2}...`
              A comma separated list of zone categories.
            * ZoneCategoriesOptions (optional): `;option1=value1;options2=value2...`
              A list of options for zone categories in `KEY=VALUE` form.

            Supported zone category options:
              * exceptZoneIds: A comma-separated list of zone identifiers, which should not be taken into account for
            evaluation of zone categories to avoid.

            Supported zone categories:
              * `vignette`
              * `congestionPricing`
              * `environmental`

            **Note**: Zones that don't apply to the current vehicle aren't avoided.
            Time-dependent zones are avoided only during the validity period.

            Example of zone categories avoidance:
            `avoid[zoneCategories]=environmental,vignette`

            Example of zone categories avoidance with exceptions:
            `avoid[zoneCategories]=environmental,vignette;exceptZoneIds=here:cm:envzone:3`
        zone_identifiers (str | Unset): A comma separated list containing identifiers of zones that routes should avoid
            going through.

            **Note**: Zones specified by id in this manner are avoided even if their conditions don't apply to the current
            vehicle.
            Time-dependent zones are avoided by id even outside of the validity period.

            Example of an identifier referencing an environmental zone:
            `here:cm:envzone:2`
        truck_road_types (str | Unset): A comma-separated list of truck road type identifiers to be avoided.

            A truck road type is an identifier associated with roads that have additional regulations applied by local
            administration for traversal by heavy vehicles like trucks.
            For example, the BK Bearing Class regulations in Sweden, and ET categories in Mexico.
            Identifiers for supported truck road types are specified in HERE Map Content
            [TruckRoadType](https://www.here.com/docs/bundle/map-content-schema-data-
            specification/page/topics_schema/truckroadtypeattribute.html).

            Example: `avoid[truckRoadTypes]=BK1,BK2,BK3,BK4`
             Example: BK1,BK2,BK3,BK4.
        toll_transponders (str | Unset): Specifies that routes should avoid roads where the specified toll transponders
            are the only payment method.

            The value of the parameter is a comma-separated list of transponder systems that the user has. Alternatively,
            the user can also specify `all` as a list element to state they have all required transponders along any
            potential route.

            **Note**: Currently, the only valid value is `all`.
            Example: `avoid[tollTransponders]=all`
    """

    features: str | Unset = UNSET
    areas: str | Unset = UNSET
    segments: str | Unset = UNSET
    zone_categories: str | Unset = UNSET
    zone_identifiers: str | Unset = UNSET
    truck_road_types: str | Unset = UNSET
    toll_transponders: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        features = self.features

        areas = self.areas

        segments = self.segments

        zone_categories = self.zone_categories

        zone_identifiers = self.zone_identifiers

        truck_road_types = self.truck_road_types

        toll_transponders = self.toll_transponders

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if features is not UNSET:
            field_dict["features"] = features
        if areas is not UNSET:
            field_dict["areas"] = areas
        if segments is not UNSET:
            field_dict["segments"] = segments
        if zone_categories is not UNSET:
            field_dict["zoneCategories"] = zone_categories
        if zone_identifiers is not UNSET:
            field_dict["zoneIdentifiers"] = zone_identifiers
        if truck_road_types is not UNSET:
            field_dict["truckRoadTypes"] = truck_road_types
        if toll_transponders is not UNSET:
            field_dict["tollTransponders"] = toll_transponders

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        features = d.pop("features", UNSET)

        areas = d.pop("areas", UNSET)

        segments = d.pop("segments", UNSET)

        zone_categories = d.pop("zoneCategories", UNSET)

        zone_identifiers = d.pop("zoneIdentifiers", UNSET)

        truck_road_types = d.pop("truckRoadTypes", UNSET)

        toll_transponders = d.pop("tollTransponders", UNSET)

        avoid = cls(
            features=features,
            areas=areas,
            segments=segments,
            zone_categories=zone_categories,
            zone_identifiers=zone_identifiers,
            truck_road_types=truck_road_types,
            toll_transponders=toll_transponders,
        )

        avoid.additional_properties = d
        return avoid

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
