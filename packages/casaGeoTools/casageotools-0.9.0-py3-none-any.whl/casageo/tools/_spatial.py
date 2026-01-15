from collections.abc import Sequence
from dataclasses import KW_ONLY, dataclass
from datetime import datetime
from typing import Any

from geopandas import GeoDataFrame
from shapely import (
    MultiLineString,
    MultiPolygon,
    Point,
)

from . import _consts, _util
from ._client import CasaGeoClient
from ._types import CasaGeoResult


def _position_point(data: dict | None) -> Point | None:
    if data is None:
        return None
    try:
        if (elv := data.get("elv")) is not None:
            return Point(data["lng"], data["lat"], elv)
        return Point(data["lng"], data["lat"])
    except KeyError:
        # FIXME: Raise warning here.
        return None


def _fromisoformat(date: str | None) -> datetime | None:
    if date is None:
        return None
    try:
        return datetime.fromisoformat(date)
    except ValueError:
        # FIXME: Raise warning here.
        return None


class IsolinesResult(CasaGeoResult):
    """
    Represents the result of a CasaGeoSpatial.isolines() query.
    """

    @staticmethod
    def _geometry(isoline: dict) -> MultiPolygon | None:
        try:
            polygons = isoline["polygons"]
        except KeyError:
            return None

        return MultiPolygon([
            (
                _util.flexpolyline_points(outer),
                [
                    _util.flexpolyline_points(inner)
                    for inner in polygon.get("inner", ())
                ],
            )
            for polygon in polygons
            if (outer := polygon.get("outer")) is not None
        ])

    @staticmethod
    def _range_type(isoline: dict) -> str | None:
        try:
            return isoline["range"]["type"]
        except KeyError:
            return None

    @staticmethod
    def _range_value(isoline: dict) -> float | None:
        try:
            value = float(isoline["range"]["value"])
        except KeyError:
            return None

        # We interpret range_values as minutes, while HERE interprets them as seconds.
        if IsolinesResult._range_type(isoline) == "time":
            value /= 60

        return value

    def dataframe(
        self,
        id_: Any | None = None,
        *,
        departure_info: bool = False,
        arrival_info: bool = False,
    ) -> GeoDataFrame:
        """
        Return the result as a GeoDataFrame.

        The dataframe will contain the following columns:

        - *id* (str | Any): Fixed identifier added to each row. Can be
          overridden using the ``id_`` parameter.
        - *subid* (int): Numeric index of the result value starting from zero.
        - *geometry* (MultiPolygon): A MultiPolygon representing the isoline’s geometry.
        - *rangetype* (str): String representing the type of the distance value.
        - *rangevalue* (float): The distance value represented by this range.
        - *timestamp* (datetime): Timestamp of when this result was created.

        When ``departure_info`` is ``True``, the dataframe also contains the
        columns below. If the direction of the query was not ``"outgoing"``, all
        these values will be null.

        - *departure_time* (datetime): Timestamp representing the expected
          departure time.
        - *departure_placename* (str): Name of the departure location.
        - *departure_position* (Point): Resolved position of the departure
          location used for route calculation.
        - *departure_displayposition* (Point): Position of a map marker
          referring to the departure location.
        - *departure_queryposition* (Point): The original position provided
          in the request.

        When ``arrival_info`` is ``True``, the dataframe also contains the
        columns below. If the direction of the query was not ``"incoming"``, all
        these values will be null.

        - *arrival_time* (datetime): Timestamp representing the expected
          arrival time.
        - *arrival_placename* (str): Name of the arrival location.
        - *arrival_position* (Point): Resolved position of the arrival
          location used for route calculation.
        - *arrival_displayposition* (Point): Position of a map marker
          referring to the arrival location.
        - *arrival_queryposition* (Point): The original position provided
          in the request.

        Args:
            id_: Fixed identifier to be added to each row.
            departure_info: Include additional info about the departure
                time and location.
            arrival_info: Include additional info about the arrival
                time and location.

        Returns:
            GeoDataFrame: The list of computed isolines as a GeoDataFrame.
        """
        # - *names*: String descriptor of an isoline, generated from 'range_type' and 'range_value'.

        if id_ is None:
            id_ = str(self._uuid)

        data: list[dict] = []
        for index, isoline in enumerate(self._data.get("isolines", [])):
            data.append(row := {})

            if True:
                # fmt: off
                row["id"]               = id_
                row["subid"]            = index
                row["geometry"]         = self._geometry(isoline)
                row["rangetype"]        = self._range_type(isoline)
                row["rangevalue"]       = self._range_value(isoline)
                row["timestamp"]        = self._timestamp
                # fmt: on

        if not data:
            return GeoDataFrame()

        # TODO: When elevation is returned, the CRS should be different (EPSG:4979 ?).
        df = GeoDataFrame(data, geometry="geometry", crs="EPSG:4326")

        if departure_info:
            departure = self.departure_info() or {}
            # fmt: off
            df["departure_time"]            = departure.get("time")
            df["departure_placename"]       = departure.get("placename")
            df["departure_position"]        = departure.get("position")
            df["departure_displayposition"] = departure.get("displayposition")
            df["departure_queryposition"]   = departure.get("queryposition")
            # fmt: on

        if arrival_info:
            arrival = self.arrival_info() or {}
            # fmt: off
            df["arrival_time"]              = arrival.get("time")
            df["arrival_placename"]         = arrival.get("placename")
            df["arrival_position"]          = arrival.get("position")
            df["arrival_displayposition"]   = arrival.get("displayposition")
            df["arrival_queryposition"]     = arrival.get("queryposition")
            # fmt: on

        return df

    def has_departure_info(self) -> bool:
        """Return ``True`` if the API response includes departure information."""
        return "departure" in self._data

    def departure_info(self) -> dict | None:
        """
        Return departure information, if available.

        Departure information includes the following values, all of which can be
        ``None``:

        - *time* (datetime): Timestamp representing the expected departure time.
        - *placename* (str): Name of the departure location.
        - *position* (Point): Resolved position of the departure location used
          for route calculation.
        - *displayposition* (Point): Position of a map marker referring to the
          departure location.
        - *queryposition* (Point): The original departure position specified in
          the request.

        Returns:
            dict | None: Departure information as a ``dict``, or ``None`` if no
            departure information is available.
        """
        try:
            departure = self._data["departure"]
            place = departure["place"]
        except KeyError:
            return None
        return {
            "time": _fromisoformat(departure.get("time")),
            "placename": place.get("name"),
            "position": _position_point(place.get("location")),
            "displayposition": _position_point(place.get("displayLocation")),
            "queryposition": _position_point(place.get("originalLocation")),
        }

    def has_arrival_info(self) -> bool:
        """Return ``True`` if the API response includes arrival information."""
        return "arrival" in self._data

    def arrival_info(self) -> dict | None:
        """
        Return arrival information, if available.

        Arrival information includes the following values, all of which can be
        ``None``:

        - *time* (datetime): Timestamp representing the expected arrival time.
        - *placename* (str): Name of the arrival location.
        - *position* (Point): Resolved position of the arrival location used
          for route calculation.
        - *displayposition* (Point): Position of a map marker referring to the
          arrival location.
        - *queryposition* (Point): The original arrival position specified in
          the request.

        Returns:
            dict | None: Arrival information as a ``dict``, or ``None`` if no
            arrival information is available.
        """
        try:
            arrival = self._data["arrival"]
            place = arrival["place"]
        except KeyError:
            return None
        return {
            "time": _fromisoformat(arrival.get("time")),
            "placename": place.get("name"),
            "position": _position_point(place.get("location")),
            "displayposition": _position_point(place.get("displayLocation")),
            "queryposition": _position_point(place.get("originalLocation")),
        }


class RoutesResult(CasaGeoResult):
    """
    Represents the result of a CasaGeoSpatial.routes() query.
    """

    @staticmethod
    def _geometry(route: dict) -> MultiLineString | None:
        try:
            return MultiLineString([
                _util.flexpolyline_points(section["polyline"])
                for section in route["sections"]
            ])
        except KeyError:
            return None

    def dataframe(
        self,
        id_: Any | None = None,
        *,
        departure_info: bool = False,
        arrival_info: bool = False,
    ) -> GeoDataFrame:
        """
        Return the result as a GeoDataFrame.

        The dataframe will contain the following columns:

        - *id* (str | Any): Fixed identifier added to each row. Can be
          overridden using the ``id_`` parameter.
        - *subid* (int): Numeric index of the result value starting from zero.
        - *routeid* (str): Unique identifier of the route.
        - *geometry* (MultiLineString): Geometry of the route by sections.
        - *timestamp* (datetime): Timestamp of when this result was created.

        When ``departure_info`` is ``True``, the dataframe also contains the
        following columns:

        - *departure_time* (datetime): Timestamp representing the expected
          departure time.
        - *departure_placename* (str): Name of the departure location.
        - *departure_position* (Point): Resolved position of the departure
          location used for route calculation.
        - *departure_displayposition* (Point): Position of a map marker
          referring to the departure location.
        - *departure_queryposition* (Point): The original departure position
          specified in the request.

        When ``arrival_info`` is ``True``, the dataframe also contains the
        following columns:

        - *arrival_time* (datetime): Timestamp representing the expected arrival
          time.
        - *arrival_placename* (str): Name of the arrival location.
        - *arrival_position* (Point): Resolved position of the arrival location
          used for route calculation.
        - *arrival_displayposition* (Point): Position of a map marker referring
          to the arrival location.
        - *arrival_queryposition* (Point): The original arrival position
          specified in the request.

        Args:
            id_: Fixed identifier to be added to each row.
            departure_info: Include additional info about the departure
                time and location of each route.
            arrival_info: Include additional info about the arrival
                time and location of each route.

        Returns:
            GeoDataFrame: The list of computed routes as a GeoDataFrame.
        """

        if id_ is None:
            id_ = str(self._uuid)

        data: list[dict] = []
        for index, route in enumerate(self._data.get("routes", [])):
            data.append(row := {})

            if True:
                # fmt: off
                row["id"]                           = id_
                row["subid"]                        = index
                row["routeid"]                      = route.get("id")
                row["geometry"]                     = self._geometry(route)
                row["timestamp"]                    = self._timestamp
                # fmt: on

            if departure_info:
                departure = self.departure_info(index) or {}
                # fmt: off
                row["departure_time"]               = departure.get("time")
                row["departure_placename"]          = departure.get("placename")
                row["departure_position"]           = departure.get("position")
                row["departure_displayposition"]    = departure.get("displayposition")
                row["departure_queryposition"]      = departure.get("queryposition")
                # fmt: on

            if arrival_info:
                arrival = self.arrival_info(index) or {}
                # fmt: off
                row["arrival_time"]                 = arrival.get("time")
                row["arrival_placename"]            = arrival.get("placename")
                row["arrival_position"]             = arrival.get("position")
                row["arrival_displayposition"]      = arrival.get("displayposition")
                row["arrival_queryposition"]        = arrival.get("queryposition")
                # fmt: on

        if not data:
            return GeoDataFrame()

        # TODO: When elevation is returned, the CRS should be different (EPSG:4979 ?).
        return GeoDataFrame(data, geometry="geometry", crs="EPSG:4326")

    def departure_info(self, route: int, section: int = 0) -> dict | None:
        """
        Returns departure information for a specific route or section.

        Departure information includes the following values, all of which can be
        ``None``:

        - *time* (datetime): Timestamp representing the expected departure time.
        - *placename* (str): Name of the departure location.
        - *position* (Point): Resolved position of the departure location used
          for route calculation.
        - *displayposition* (Point): Position of a map marker referring to the
          departure location.
        - *queryposition* (Point): The original departure position specified in
          the request.

        Args:
            route: Index of the route in the result list.
            section: Index of the section within the route, defaults to the
                first section.

        Returns:
            dict | None: Departure information as a ``dict``, or ``None`` if no
            such information exists for the specified route and section.
        """
        try:
            departure = self._data["routes"][route]["sections"][section]["departure"]
            place = departure["place"]
        except (KeyError, IndexError):
            return None
        return {
            "time": _fromisoformat(departure.get("time")),
            "placename": place.get("name"),
            "position": _position_point(place.get("location")),
            "displayposition": _position_point(place.get("displayLocation")),
            "queryposition": _position_point(place.get("originalLocation")),
        }

    def arrival_info(self, route: int, section: int = -1) -> dict | None:
        """
        Returns arrival information for a specific route or section.

        Arrival information includes the following values, all of which can be
        ``None``:

        - *time* (datetime): Timestamp representing the expected arrival time.
        - *placename* (str): Name of the arrival location.
        - *position* (Point): Resolved position of the arrival location used
          for route calculation.
        - *displayposition* (Point): Position of a map marker referring to the
          arrival location.
        - *queryposition* (Point): The original arrival position specified in
          the request.

        Args:
            route: Index of the route in the result list.
            section: Index of the section within the route, defaults to the
                last section.

        Returns:
            dict | None: Arrival information as a ``dict``, or ``None`` if no
            such information exists for the specified route and section.
        """
        try:
            arrival = self._data["routes"][route]["sections"][section]["arrival"]
            place = arrival["place"]
        except (KeyError, IndexError):
            return None
        return {
            "time": _fromisoformat(arrival.get("time")),
            "placename": place.get("name"),
            "position": _position_point(place.get("location")),
            "displayposition": _position_point(place.get("displayLocation")),
            "queryposition": _position_point(place.get("originalLocation")),
        }


@dataclass
class CasaGeoSpatial:
    """
    Provides spatial calculations such as routing and isolines.

    Attributes:
        client:
            The client object authorizing these queries.

        language:
            The preferred language for the response.

            This must be a valid IETF BCP47 language tag, such as "en-US", or a
            comma-separated list of such tags in order of preference.

        unit_system:
            The system of units to use for localized quantities, either
            ``"metric"`` or ``"imperial"``.

        transport_mode:
            The mode of transport to use for routing, e.g. ``"car"``.

            The following modes are available:

            - ``"car"``
            - ``"pedestrian"``
            - ``"bicycle"``

        routing_mode:
            Whether to prefer ``"fast"`` or ``"short"`` routes.

        direction:
            The direction of travel for isolines, either ``"outgoing"`` or
            ``"incoming"``.

        departure_time:
            The date and time of departure for time-dependent routing. This
            value is only used when ``direction`` is ``"outgoing"``.

        arrival_time:
            The date and time of arrival for time-dependent routing. This
            value is only used when ``direction`` is ``"incoming"``.

        consider_traffic:
            Whether to consider traffic data during routing.

            When using this feature, you should also specify either
            ``departure_time`` or ``arrival_time``, depending on ``direction``,
            to get meaningful and reproducible results.

        avoid_features:
            Route features to avoid during routing, e.g. ``("ferry", "tollRoad")``.

            The following features are currently supported:

            - ``"carShuttleTrain"``
            - ``"controlledAccessHighway"``
            - ``"dirtRoad"``
            - ``"ferry"``
            - ``"seasonalClosure"``
            - ``"tollRoad"``
            - ``"tunnel"``

        exclude_countries:
            Countries to exclude from routing, e.g. ``("USA", "DEU")``.

            Countries must be specified by their ISO 3166-1 alpha-3 country
            codes.
    """

    client: CasaGeoClient
    _: KW_ONLY
    language: str | None = None
    unit_system: str | None = None
    transport_mode: str = "car"
    routing_mode: str = "fast"
    direction: str = "outgoing"
    departure_time: datetime | None = None
    arrival_time: datetime | None = None
    consider_traffic: bool = False
    avoid_features: Sequence[str] = ()
    exclude_countries: Sequence[str] = ()

    def __post_init__(self) -> None:
        # Check that self.client is not a string, because the beta version of
        # this class took the license key as the first parameter.
        if not isinstance(self.client, CasaGeoClient):
            raise TypeError("client must be a CasaGeoClient instance")
        if self.language is None:
            self.language = self.client.preferred_language
        if self.unit_system is None:
            self.unit_system = self.client.preferred_unit_system

    def _validate(self) -> None:
        if self.language is not None:
            if not self.language:
                raise ValueError("language must not be empty")
            for tag in self.language.split(","):
                _util.validate_ietf_bcp47_language_tag(tag)

        if self.unit_system is not None:
            if self.unit_system not in _consts.UNIT_SYSTEMS:
                raise ValueError(
                    f"unit_system must be one of {_consts.UNIT_SYSTEMS}, got {self.unit_system!r}"
                )

        if self.transport_mode not in _consts.TRANSPORT_MODES:
            raise ValueError(
                f"transport_mode must be one of {_consts.TRANSPORT_MODES}, got {self.transport_mode!r}"
            )

        if self.routing_mode not in _consts.ROUTING_MODES:
            raise ValueError(
                f"routing_mode must be one of {_consts.ROUTING_MODES}, got {self.routing_mode!r}"
            )

        if self.direction not in _consts.DIRECTION_TYPES:
            raise ValueError(
                f"direction must be one of {_consts.DIRECTION_TYPES}, got {self.direction!r}"
            )

        for feature in self.avoid_features:
            if feature not in _consts.AVOIDABLE_FEATURES:
                raise ValueError(
                    f"avoid_features may only contain {_consts.AVOIDABLE_FEATURES}, got {feature!r}"
                )

        for country in self.exclude_countries:
            _util.validate_iso3166_alpha3_country_code(country)

    def _departure(self) -> str | None:
        if self.direction != "outgoing":
            return None
        if self.departure_time is None:
            return "any"
        return self.departure_time.isoformat()

    def _arrival(self) -> str | None:
        if self.direction != "incoming":
            return None
        if self.arrival_time is None:
            return "any"
        return self.arrival_time.isoformat()

    # https://www.here.com/docs/bundle/isoline-routing-api-developer-guide-v8/page/README.html
    # https://www.here.com/docs/bundle/isoline-routing-api-v8-api-reference/page/index.html
    @IsolinesResult.wrap_errors()
    def isolines(
        self,
        position: Point,
        ranges: Sequence[float],
        *,
        range_type: str = "time",
    ) -> IsolinesResult:
        """
        Calculate isolines around ``position``.

        Args:
            position:
                The center point of the isolines.
            ranges:
                The distances (in meters) or durations (in minutes) for which to
                calculate isolines.
            range_type:
                The type of range to calculate. Must be one of ``"time"`` or
                ``"distance"``.

        Returns:
            IsolinesResult: The result of the isoline calculation.
        """
        from ._apiclient.isolines.api.isoline import calculate_isolines
        from ._apiclient.isolines.models import (
            Avoid,
            Exclude,
            Range,
            RouterMode,
            RoutingMode,
            Traffic,
            TrafficMode,
        )
        from ._apiclient.isolines.types import UNSET

        self._validate()

        if not position.is_valid:
            raise ValueError("position must be a valid 2D point")

        if range_type not in _consts.RANGE_TYPES:
            raise ValueError(
                f"range_type must be one of {_consts.RANGE_TYPES}, got {range_type!r}"
            )

        # We interpret time values as minutes, while HERE interprets them as seconds.
        if range_type == "time":
            ranges = [x * 60 for x in ranges]

        point_str = _util.point_to_latlng(position)
        departure = self.departure_time or UNSET
        arrival = self.arrival_time or UNSET

        response = calculate_isolines.sync_detailed(
            client=self.client._isolines_client,
            range_=Range(
                type_=range_type,
                values=",".join(str(int(x)) for x in ranges),
            ),
            origin=(point_str if self.direction == "outgoing" else UNSET),
            destination=(point_str if self.direction == "incoming" else UNSET),
            departure_time=(departure if self.direction == "outgoing" else UNSET),
            arrival_time=(arrival if self.direction == "incoming" else UNSET),
            transport_mode=RouterMode(self.transport_mode),
            routing_mode=RoutingMode(self.routing_mode),
            avoid=Avoid(
                features=",".join(self.avoid_features)
                if self.avoid_features
                else UNSET,
            ),
            exclude=Exclude(
                countries=",".join(self.exclude_countries)
                if self.exclude_countries
                else UNSET
            ),
            traffic=Traffic(
                mode=TrafficMode.DEFAULT
                if self.consider_traffic
                else TrafficMode.DISABLED
            ),
        )

        return IsolinesResult.from_response(response)

    # https://www.here.com/docs/bundle/routing-api-developer-guide-v8/page/README.html
    # https://www.here.com/docs/bundle/routing-api-v8-api-reference/page/index.html
    @RoutesResult.wrap_errors()
    def routes(
        self,
        origin: Point,
        destination: Point,
        *,
        alternatives: int = 0,
    ) -> RoutesResult:
        """
        Calculate routes from ``origin`` to ``destination``.

        Args:
            origin: The starting point of the route.
            destination: The destination point of the route.
            alternatives: The number of alternate routes to calculate.

        Returns:
            RoutesResult: The result of the route calculation.
        """
        from ._apiclient.router.api.routing import calculate_routes
        from ._apiclient.router.models import (
            Avoid,
            Exclude,
            Return,
            RouterMode,
            RoutingMode,
            Traffic,
            TrafficMode,
            Units,
        )
        from ._apiclient.router.types import UNSET

        self._validate()

        if not origin.is_valid:
            raise ValueError("origin must be a valid 2D point")

        if not destination.is_valid:
            raise ValueError("destination must be a valid 2D point")

        if not 0 <= alternatives <= 6:
            raise ValueError(
                "Number of alternate routes must be between 0 and 6 inclusive"
            )

        # NOTE: Due to API client limitations, we can’t support departureTime=any and
        #       arrivalTime=any everywhere, so we choose to not support it at all.
        departure = self.departure_time.isoformat() if self.departure_time else UNSET
        arrival = self.arrival_time or UNSET

        response = calculate_routes.sync_detailed(
            client=self.client._routing_client,
            origin=_util.point_to_latlng(origin),
            destination=_util.point_to_latlng(destination),
            alternatives=alternatives,
            departure_time=(departure if self.direction == "outgoing" else UNSET),
            arrival_time=(arrival if self.direction == "incoming" else UNSET),
            transport_mode=RouterMode(self.transport_mode),
            routing_mode=RoutingMode(self.routing_mode),
            avoid=Avoid(
                features=",".join(self.avoid_features)
                if self.avoid_features
                else UNSET,
            ),
            exclude=Exclude(
                countries=",".join(self.exclude_countries)
                if self.exclude_countries
                else UNSET
            ),
            traffic=Traffic(
                mode=TrafficMode.DEFAULT
                if self.consider_traffic
                else TrafficMode.DISABLED
            ),
            lang=self.language.split(",") if self.language is not None else UNSET,
            units=Units(self.unit_system) if self.unit_system is not None else UNSET,
            return_=[Return.SUMMARY, Return.POLYLINE],
        )

        return RoutesResult.from_response(response)
