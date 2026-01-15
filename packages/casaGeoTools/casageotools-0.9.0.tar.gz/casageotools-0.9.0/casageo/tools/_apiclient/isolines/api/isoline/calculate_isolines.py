import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.allow import Allow
from ...models.auth_error_response_schema import AuthErrorResponseSchema
from ...models.avoid import Avoid
from ...models.base_ev_empirical_model import BaseEVEmpiricalModel
from ...models.base_ev_physical_model import BaseEVPhysicalModel
from ...models.calculate_isolines_optimize_for import CalculateIsolinesOptimizeFor
from ...models.exclude import Exclude
from ...models.fuel import Fuel
from ...models.isoline_error_response import IsolineErrorResponse
from ...models.isoline_response import IsolineResponse
from ...models.not_allowed import NotAllowed
from ...models.range_ import Range
from ...models.router_mode import RouterMode
from ...models.routing_mode import RoutingMode
from ...models.server_internal import ServerInternal
from ...models.shape import Shape
from ...models.taxi import Taxi
from ...models.traffic import Traffic
from ...models.truck import Truck
from ...models.vehicle import Vehicle
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    range_: Range,
    transport_mode: RouterMode,
    origin: str | Unset = UNSET,
    departure_time: datetime.datetime | Unset = UNSET,
    destination: str | Unset = UNSET,
    arrival_time: datetime.datetime | Unset = UNSET,
    routing_mode: RoutingMode | Unset = UNSET,
    shape: Shape | Unset = UNSET,
    optimize_for: CalculateIsolinesOptimizeFor
    | Unset = CalculateIsolinesOptimizeFor.BALANCED,
    avoid: Avoid | Unset = UNSET,
    exclude: Exclude | Unset = UNSET,
    allow: Allow | Unset = UNSET,
    truck: Truck | Unset = UNSET,
    vehicle: Vehicle | Unset = UNSET,
    consumption_model: str | Unset = UNSET,
    ev: BaseEVEmpiricalModel | BaseEVPhysicalModel | Unset = UNSET,
    fuel: Fuel | Unset = UNSET,
    max_speed_on_segment: str | Unset = UNSET,
    taxi: Taxi | Unset = UNSET,
    traffic: Traffic | Unset = UNSET,
    billing_tag: str | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_request_id, Unset):
        headers["X-Request-ID"] = x_request_id

    params: dict[str, Any] = {}

    json_range_ = range_.to_dict()
    params.update((f"range[{k}]", v) for k, v in json_range_.items())

    json_transport_mode = transport_mode.value
    params["transportMode"] = json_transport_mode

    params["origin"] = origin

    json_departure_time: str | Unset = UNSET
    if not isinstance(departure_time, Unset):
        json_departure_time = departure_time.isoformat()
    params["departureTime"] = json_departure_time

    params["destination"] = destination

    json_arrival_time: str | Unset = UNSET
    if not isinstance(arrival_time, Unset):
        json_arrival_time = arrival_time.isoformat()
    params["arrivalTime"] = json_arrival_time

    json_routing_mode: str | Unset = UNSET
    if not isinstance(routing_mode, Unset):
        json_routing_mode = routing_mode.value

    params["routingMode"] = json_routing_mode

    json_shape: dict[str, Any] | Unset = UNSET
    if not isinstance(shape, Unset):
        json_shape = shape.to_dict()
    if not isinstance(json_shape, Unset):
        params.update((f"shape[{k}]", v) for k, v in json_shape.items())

    json_optimize_for: str | Unset = UNSET
    if not isinstance(optimize_for, Unset):
        json_optimize_for = optimize_for.value

    params["optimizeFor"] = json_optimize_for

    json_avoid: dict[str, Any] | Unset = UNSET
    if not isinstance(avoid, Unset):
        json_avoid = avoid.to_dict()
    if not isinstance(json_avoid, Unset):
        params.update((f"avoid[{k}]", v) for k, v in json_avoid.items())

    json_exclude: dict[str, Any] | Unset = UNSET
    if not isinstance(exclude, Unset):
        json_exclude = exclude.to_dict()
    if not isinstance(json_exclude, Unset):
        params.update((f"exclude[{k}]", v) for k, v in json_exclude.items())

    json_allow: dict[str, Any] | Unset = UNSET
    if not isinstance(allow, Unset):
        json_allow = allow.to_dict()
    if not isinstance(json_allow, Unset):
        params.update((f"allow[{k}]", v) for k, v in json_allow.items())

    json_truck: dict[str, Any] | Unset = UNSET
    if not isinstance(truck, Unset):
        json_truck = truck.to_dict()
    if not isinstance(json_truck, Unset):
        params.update((f"truck[{k}]", v) for k, v in json_truck.items())

    json_vehicle: dict[str, Any] | Unset = UNSET
    if not isinstance(vehicle, Unset):
        json_vehicle = vehicle.to_dict()
    if not isinstance(json_vehicle, Unset):
        params.update((f"vehicle[{k}]", v) for k, v in json_vehicle.items())

    params["consumptionModel"] = consumption_model

    json_ev: dict[str, Any] | Unset
    if isinstance(ev, Unset):
        json_ev = UNSET
    elif isinstance(ev, BaseEVEmpiricalModel):
        json_ev = ev.to_dict()
    else:
        json_ev = ev.to_dict()

    params["ev"] = json_ev

    json_fuel: dict[str, Any] | Unset = UNSET
    if not isinstance(fuel, Unset):
        json_fuel = fuel.to_dict()
    if not isinstance(json_fuel, Unset):
        params.update((f"fuel[{k}]", v) for k, v in json_fuel.items())

    params["maxSpeedOnSegment"] = max_speed_on_segment

    json_taxi: dict[str, Any] | Unset = UNSET
    if not isinstance(taxi, Unset):
        json_taxi = taxi.to_dict()
    if not isinstance(json_taxi, Unset):
        params.update((f"taxi[{k}]", v) for k, v in json_taxi.items())

    json_traffic: dict[str, Any] | Unset = UNSET
    if not isinstance(traffic, Unset):
        json_traffic = traffic.to_dict()
    if not isinstance(json_traffic, Unset):
        params.update((f"traffic[{k}]", v) for k, v in json_traffic.items())

    params["billingTag"] = billing_tag

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/isolines",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    AuthErrorResponseSchema
    | AuthErrorResponseSchema
    | NotAllowed
    | IsolineErrorResponse
    | IsolineResponse
    | ServerInternal
    | None
):
    if response.status_code == 200:
        response_200 = IsolineResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = IsolineErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = AuthErrorResponseSchema.from_dict(response.json())

        return response_401

    if response.status_code == 403:

        def _parse_response_403(data: object) -> AuthErrorResponseSchema | NotAllowed:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_isoline_403_error_response_schema_type_0 = (
                    AuthErrorResponseSchema.from_dict(data)
                )

                return componentsschemas_isoline_403_error_response_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_isoline_403_error_response_schema_type_1 = (
                NotAllowed.from_dict(data)
            )

            return componentsschemas_isoline_403_error_response_schema_type_1

        response_403 = _parse_response_403(response.json())

        return response_403

    if response.status_code == 500:
        response_500 = ServerInternal.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    AuthErrorResponseSchema
    | AuthErrorResponseSchema
    | NotAllowed
    | IsolineErrorResponse
    | IsolineResponse
    | ServerInternal
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    range_: Range,
    transport_mode: RouterMode,
    origin: str | Unset = UNSET,
    departure_time: datetime.datetime | Unset = UNSET,
    destination: str | Unset = UNSET,
    arrival_time: datetime.datetime | Unset = UNSET,
    routing_mode: RoutingMode | Unset = UNSET,
    shape: Shape | Unset = UNSET,
    optimize_for: CalculateIsolinesOptimizeFor
    | Unset = CalculateIsolinesOptimizeFor.BALANCED,
    avoid: Avoid | Unset = UNSET,
    exclude: Exclude | Unset = UNSET,
    allow: Allow | Unset = UNSET,
    truck: Truck | Unset = UNSET,
    vehicle: Vehicle | Unset = UNSET,
    consumption_model: str | Unset = UNSET,
    ev: BaseEVEmpiricalModel | BaseEVPhysicalModel | Unset = UNSET,
    fuel: Fuel | Unset = UNSET,
    max_speed_on_segment: str | Unset = UNSET,
    taxi: Taxi | Unset = UNSET,
    traffic: Traffic | Unset = UNSET,
    billing_tag: str | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[
    AuthErrorResponseSchema
    | AuthErrorResponseSchema
    | NotAllowed
    | IsolineErrorResponse
    | IsolineResponse
    | ServerInternal
]:
    """Get Isolines for specified ranges around a center point

     Retrieves a list of polylines that captures the approximate reachable area
    from the specified center point constrained by the provided parameters.

    Args:
        range_ (Range): Ranges specified in terms of distance, travel time or energy consumption.
        transport_mode (RouterMode): Mode of transport to be used for route calculation.
        origin (str | Unset): A location defining an origin, destination or via point for a route
            or an isoline.

            Format: `Place[WaypointOptions]`

            * Place: `{lat},{lng}[PlaceOptions]`
            * PlaceOptions: `;option1=value1;option2=value2...`
            * WaypointOptions: `!option1=value1!option2=value2...`

            A waypoint consists of:
            * Exactly one place
            * Optional settings for the place
            * Optional settings for the waypoint itself

            Supported place options:
            * `course`: int, degrees clock-wise from north. Indicates the desired direction from the
            place. For example, `90` indicating `east`. Often combined with `radius` and/or
            `minCourseDistance`. This parameter takes preference over `matchSideOfStreet`.
            * `sideOfStreetHint`: `{lat},{lng}`. Indicates the side of the street that should be used.
            For example, if the location is to the left of the street, the router will prefer using
            that side in case the street has dividers. For example,
            `52.511496,13.304140;sideOfStreetHint=52.512149,13.304076` indicates that the `north` side
            of the street should be preferred. This options is required, if `matchSideOfStreet` is set
            to `always`. Option cannot be combined with `radius`, `radiusPenalty` or `snapRadius`.
            * `displayLocation`: `{lat},{lng}`. Indicates the physical location of the POI. It is
            different from the originalLocation and location which are generally expected to be on the
            navigable road network, i.e., on segments.
            * `uTurnPermission`: enum `[allow, avoid]`. Specifies the U-Turn Permission mode at the
            stop-over waypoint. If unspecified, the permission will be determined by the global
            setting, avoid[features]=uTurns. This feature is not supported for pass-through waypoints
            and U-Turns are generally avoided in that case.
              + `allow` : Allow making a U-Turn at this stop-over waypoint
              + `avoid` : Avoid making a U-Turn at this stop-over waypoint
            * `matchSideOfStreet`: enum `[always, onlyIfDivided]`. Specifies how the location set by
            `sideOfStreetHint` should be handled. Requires `sideOfStreetHint` to be specified as well.
            Note the exception above when combined with `course`.
              + `always` : Always prefer the given side of street.
              + `onlyIfDivided`: Only prefer using side of street set by `sideOfStreetHint` in case
            the street has dividers. This is the default behavior.
            * `nameHint`: string. Causes the router to look for the place with the most similar name.
            The typical examples include: `North` being used to differentiate between interstates `I66
            North` and `I66 South`, `Downtown Avenue` being used to correctly select a residental
            street.
            * `radius`: int, meters. Sets the radius within which all locations are considered equally
            eligible for selection as waypoints. Typical use cases include scenarios with imprecise
            coordinates or user input provided on low resolution map displays. The value is capped at
            200 meters. Setting a higher value doesn't return an error. Can't be used with
            `snapRadius`.
            * `snapRadius`: int, meters. Sets the radius within which waypoints are matched to the
            most "significant" place. Candidates for matching are sorted in the order of significance
            which is based on the visibility on a zoomed-out map. A highway is considered more
            significant than a national road, while a national road is more significant than a city
            road. Typical use case - selecting waypoints on a  zoomed-out view of a map on a drag-and-
            drop interface, where only significant roads are visible. A big enough radius allows to
            match waypoints to such roads. Can't be used with `radius` or `radiusPenalty` parameters.
            * `radiusPenalty`: int, percentage 0-10000. Penalty as percentage: Used in conjunction
            with the `radius` parameter. Router will match the waypoint within the specified radius
            and apply a penalty to candidates based on their air distance to the waypoint. This
            penalty is proportional to the given percentage, where 100 is just the cost of the air
            distance, and 200 is twice the cost of the air distance. The penalty must be chosen so
            that, when multiplied by the radius, the result is less than or equal to 7200. Regardless,
            only values up to and including 10000 will be accepted. This means that a maximum penalty
            of 3600% is allowed for a radius of 200m, 7200% for 100m and 10000% for 72m and less.
            Higher values will result in an error response. `radiusPenalty` cannot be combined with
            `snapRadius`. **Alpha**: This parameter is in development. It may not be stable and is
            subject to change.

            * `minCourseDistance`: int, meters. Instructs the routing service to try to find a route
            that avoids actions for the indicated distance. For example, if the origin is determined
            by a moving vehicle, the user might not have time to react to early actions. Values
            greater than 2000 meters will be capped at 2000 meters.
            * `segmentIdHint`: string. Causes the router to try and match to the specified segment.
            Waypoint coordinates need to be on the segment, otherwise waypoint will be matched
            ignoring the segment hint. This parameter can be used when the waypoint is too close to
            more than one segment to force matching to a specific one.
            * `onRoadThreshold`: int, meters. allows specifying a distance within which the waypoint
            could be considered as being on a highway/bridge/tunnel/sliproad. Within this threshold,
            the attributes of the segments do not impact the matching. Outside the threshold only
            segments which aren't one of highway/bridge/tunnel/sliproad can be matched.

            Supported waypoint options:
            * `stopDuration`: desired duration for the stop, in seconds.
               `stopDuration` must be less than 50000.
            * `passThrough`: boolean. Asks the router to avoid the following during route calculation:
              + Introducing a stop at the waypoint.
              + Splitting the route into sections.
              + Changing the direction of travel.

            Following scenarios are not supported for `passThrough` parameter:
              + Setting both `stopDuration` to a value greater than 0 and `passThrough=true`.
              + Setting `passThrough=true` for `origin` or `destination` of a route.
              The default value is `false`.
        departure_time (datetime.datetime | Unset): **RFC 3339**, section 5.6 as defined by either
            `date-time` or `date-only` 'T' `partial-time` (ie no time-offset).
        destination (str | Unset): A location defining an origin, destination or via point for a
            route or an isoline.

            Format: `Place[WaypointOptions]`

            * Place: `{lat},{lng}[PlaceOptions]`
            * PlaceOptions: `;option1=value1;option2=value2...`
            * WaypointOptions: `!option1=value1!option2=value2...`

            A waypoint consists of:
            * Exactly one place
            * Optional settings for the place
            * Optional settings for the waypoint itself

            Supported place options:
            * `course`: int, degrees clock-wise from north. Indicates the desired direction from the
            place. For example, `90` indicating `east`. Often combined with `radius` and/or
            `minCourseDistance`. This parameter takes preference over `matchSideOfStreet`.
            * `sideOfStreetHint`: `{lat},{lng}`. Indicates the side of the street that should be used.
            For example, if the location is to the left of the street, the router will prefer using
            that side in case the street has dividers. For example,
            `52.511496,13.304140;sideOfStreetHint=52.512149,13.304076` indicates that the `north` side
            of the street should be preferred. This options is required, if `matchSideOfStreet` is set
            to `always`. Option cannot be combined with `radius`, `radiusPenalty` or `snapRadius`.
            * `displayLocation`: `{lat},{lng}`. Indicates the physical location of the POI. It is
            different from the originalLocation and location which are generally expected to be on the
            navigable road network, i.e., on segments.
            * `uTurnPermission`: enum `[allow, avoid]`. Specifies the U-Turn Permission mode at the
            stop-over waypoint. If unspecified, the permission will be determined by the global
            setting, avoid[features]=uTurns. This feature is not supported for pass-through waypoints
            and U-Turns are generally avoided in that case.
              + `allow` : Allow making a U-Turn at this stop-over waypoint
              + `avoid` : Avoid making a U-Turn at this stop-over waypoint
            * `matchSideOfStreet`: enum `[always, onlyIfDivided]`. Specifies how the location set by
            `sideOfStreetHint` should be handled. Requires `sideOfStreetHint` to be specified as well.
            Note the exception above when combined with `course`.
              + `always` : Always prefer the given side of street.
              + `onlyIfDivided`: Only prefer using side of street set by `sideOfStreetHint` in case
            the street has dividers. This is the default behavior.
            * `nameHint`: string. Causes the router to look for the place with the most similar name.
            The typical examples include: `North` being used to differentiate between interstates `I66
            North` and `I66 South`, `Downtown Avenue` being used to correctly select a residental
            street.
            * `radius`: int, meters. Sets the radius within which all locations are considered equally
            eligible for selection as waypoints. Typical use cases include scenarios with imprecise
            coordinates or user input provided on low resolution map displays. The value is capped at
            200 meters. Setting a higher value doesn't return an error. Can't be used with
            `snapRadius`.
            * `snapRadius`: int, meters. Sets the radius within which waypoints are matched to the
            most "significant" place. Candidates for matching are sorted in the order of significance
            which is based on the visibility on a zoomed-out map. A highway is considered more
            significant than a national road, while a national road is more significant than a city
            road. Typical use case - selecting waypoints on a  zoomed-out view of a map on a drag-and-
            drop interface, where only significant roads are visible. A big enough radius allows to
            match waypoints to such roads. Can't be used with `radius` or `radiusPenalty` parameters.
            * `radiusPenalty`: int, percentage 0-10000. Penalty as percentage: Used in conjunction
            with the `radius` parameter. Router will match the waypoint within the specified radius
            and apply a penalty to candidates based on their air distance to the waypoint. This
            penalty is proportional to the given percentage, where 100 is just the cost of the air
            distance, and 200 is twice the cost of the air distance. The penalty must be chosen so
            that, when multiplied by the radius, the result is less than or equal to 7200. Regardless,
            only values up to and including 10000 will be accepted. This means that a maximum penalty
            of 3600% is allowed for a radius of 200m, 7200% for 100m and 10000% for 72m and less.
            Higher values will result in an error response. `radiusPenalty` cannot be combined with
            `snapRadius`. **Alpha**: This parameter is in development. It may not be stable and is
            subject to change.

            * `minCourseDistance`: int, meters. Instructs the routing service to try to find a route
            that avoids actions for the indicated distance. For example, if the origin is determined
            by a moving vehicle, the user might not have time to react to early actions. Values
            greater than 2000 meters will be capped at 2000 meters.
            * `segmentIdHint`: string. Causes the router to try and match to the specified segment.
            Waypoint coordinates need to be on the segment, otherwise waypoint will be matched
            ignoring the segment hint. This parameter can be used when the waypoint is too close to
            more than one segment to force matching to a specific one.
            * `onRoadThreshold`: int, meters. allows specifying a distance within which the waypoint
            could be considered as being on a highway/bridge/tunnel/sliproad. Within this threshold,
            the attributes of the segments do not impact the matching. Outside the threshold only
            segments which aren't one of highway/bridge/tunnel/sliproad can be matched.

            Supported waypoint options:
            * `stopDuration`: desired duration for the stop, in seconds.
               `stopDuration` must be less than 50000.
            * `passThrough`: boolean. Asks the router to avoid the following during route calculation:
              + Introducing a stop at the waypoint.
              + Splitting the route into sections.
              + Changing the direction of travel.

            Following scenarios are not supported for `passThrough` parameter:
              + Setting both `stopDuration` to a value greater than 0 and `passThrough=true`.
              + Setting `passThrough=true` for `origin` or `destination` of a route.
              The default value is `false`.
        arrival_time (datetime.datetime | Unset): **RFC 3339**, section 5.6 as defined by either
            `date-time` or `date-only` 'T' `partial-time` (ie no time-offset).
        routing_mode (RoutingMode | Unset): Specifies which optimization is applied during the
            calculation.

            * `fast`: Route calculation from start to destination optimized by travel time. In many
              cases, the route returned by `fast` mode may not be the route with the fastest
              possible travel time. For example, the routing service may favor a route that remains on
              a highway, even if a faster travel time can be achieved by taking a detour or shortcut
              through an inconvenient side road.
            * `short`: Route calculation from start to destination disregarding any speed information.
              In this mode, the distance of the route is minimized, while keeping the route sensible.
              This includes, for example, penalizing turns. Because of that, the resulting route will
              not necessarily be the one with minimal distance.

            Notes:
            * The following Transport modes only support `fast` routingMode
              - `bicycle`
              - `bus`
              - `pedestrian`
              - `privateBus`
              - `scooter`
              - `taxi`
        shape (Shape | Unset): A struct used to control the shape of the returned isolines.
        optimize_for (CalculateIsolinesOptimizeFor | Unset):  Default:
            CalculateIsolinesOptimizeFor.BALANCED.
        avoid (Avoid | Unset):
        exclude (Exclude | Unset): Options to exclude strictly during the route calculation.
        allow (Allow | Unset): Explicitly allow features that require users to opt in.
        truck (Truck | Unset): Vehicle-specific parameters
        vehicle (Vehicle | Unset): Vehicle-specific parameters
        consumption_model (str | Unset): Extensible enum: `empirical` `physical` `...`
            Specifies which of the EV consumption models is being used. See the `ev` parameter for
            details on the models.

            * `empirical`
            * `physical`

            **Alpha**: Physical consumption model is in development. It may not be stable and is
            subject to change.
        ev (BaseEVEmpiricalModel | BaseEVPhysicalModel | Unset): EV parameters to be used for
            calculating consumption and for calculating isolines for EV.

            There are two consumption models (`empirical`, `physical`). Set the `consumptionModel`
            parameter to choose which model to use.

            Required `empirical` model properties:
            * `freeFlowSpeedTable`

            Required `physical` model properties:
            * `driveEfficiency`
            * `recuperationEfficiency`

            When using the physical model, certain properties of the `vehicle` parameter are also
            required (see documentation for the `vehicle` parameter for more details):
            * `rollingResistanceCoefficient`
            * `airDragCoefficient`
            * `currentWeight`
            * `frontalArea` or combination of `width` and `height`
        fuel (Fuel | Unset): Fuel parameters to be used for calculating consumption and
            consumption-based isolines for fuel-based vehicles
            using empirical consumption model.

            Attributes:
            * `type`
            * `freeFlowSpeedTable`
            * `trafficSpeedTable`
            * `additionalConsumption`
            * `ascent`
        max_speed_on_segment (str | Unset): A comma separated list of segments with restrictions
            on maximum baseSpeed.

            Each entry has the following structure:
            `{segmentId}(#{direction})?;speed={maxBaseSpeed}`

            The individual parts are:
            * segmentId: The identifier of the referenced topology segment inside the catalog,
            example: `here:cm:segment:207551710`
            * direction (optional): Either '*' for bidirectional (default), '+' for positive
            direction, or '-' for negative direction
            * maxBaseSpeed: New value in m/s of baseSpeed on segment

            Example of a parameter value excluding two segments:
            `here:cm:segment:207551710#+;speed=10,here:cm:segment:76771992;speed=1`

            **Notes**:
            - It does not increase default baseSpeed on segment. If the value is greater than the
            default base speed, then such penalty will have no effect.
            - Minimum valid value for speed is 1
            - Using segments with a modified base speed does not trigger any notifications
            - Maximum number of penalized segments in one request cannot be greater than 1000.
              "penalized segments" refer to segments that have a restrictions on maximum baseSpeed
            with `maxSpeedOnSegment`
              or avoided with `avoid[segments]`
            - In case the same segment is penalized multiple times through values provided in the
            query string and/or the POST body,
              then the most restrictive value will be applied.
        taxi (Taxi | Unset): Taxi-specific parameters
        traffic (Traffic | Unset): Traffic specific parameters.
        billing_tag (str | Unset):  Example: ABCD+EFGH.
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthErrorResponseSchema | AuthErrorResponseSchema | NotAllowed | IsolineErrorResponse | IsolineResponse | ServerInternal]
    """

    kwargs = _get_kwargs(
        range_=range_,
        transport_mode=transport_mode,
        origin=origin,
        departure_time=departure_time,
        destination=destination,
        arrival_time=arrival_time,
        routing_mode=routing_mode,
        shape=shape,
        optimize_for=optimize_for,
        avoid=avoid,
        exclude=exclude,
        allow=allow,
        truck=truck,
        vehicle=vehicle,
        consumption_model=consumption_model,
        ev=ev,
        fuel=fuel,
        max_speed_on_segment=max_speed_on_segment,
        taxi=taxi,
        traffic=traffic,
        billing_tag=billing_tag,
        x_request_id=x_request_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    range_: Range,
    transport_mode: RouterMode,
    origin: str | Unset = UNSET,
    departure_time: datetime.datetime | Unset = UNSET,
    destination: str | Unset = UNSET,
    arrival_time: datetime.datetime | Unset = UNSET,
    routing_mode: RoutingMode | Unset = UNSET,
    shape: Shape | Unset = UNSET,
    optimize_for: CalculateIsolinesOptimizeFor
    | Unset = CalculateIsolinesOptimizeFor.BALANCED,
    avoid: Avoid | Unset = UNSET,
    exclude: Exclude | Unset = UNSET,
    allow: Allow | Unset = UNSET,
    truck: Truck | Unset = UNSET,
    vehicle: Vehicle | Unset = UNSET,
    consumption_model: str | Unset = UNSET,
    ev: BaseEVEmpiricalModel | BaseEVPhysicalModel | Unset = UNSET,
    fuel: Fuel | Unset = UNSET,
    max_speed_on_segment: str | Unset = UNSET,
    taxi: Taxi | Unset = UNSET,
    traffic: Traffic | Unset = UNSET,
    billing_tag: str | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> (
    AuthErrorResponseSchema
    | AuthErrorResponseSchema
    | NotAllowed
    | IsolineErrorResponse
    | IsolineResponse
    | ServerInternal
    | None
):
    """Get Isolines for specified ranges around a center point

     Retrieves a list of polylines that captures the approximate reachable area
    from the specified center point constrained by the provided parameters.

    Args:
        range_ (Range): Ranges specified in terms of distance, travel time or energy consumption.
        transport_mode (RouterMode): Mode of transport to be used for route calculation.
        origin (str | Unset): A location defining an origin, destination or via point for a route
            or an isoline.

            Format: `Place[WaypointOptions]`

            * Place: `{lat},{lng}[PlaceOptions]`
            * PlaceOptions: `;option1=value1;option2=value2...`
            * WaypointOptions: `!option1=value1!option2=value2...`

            A waypoint consists of:
            * Exactly one place
            * Optional settings for the place
            * Optional settings for the waypoint itself

            Supported place options:
            * `course`: int, degrees clock-wise from north. Indicates the desired direction from the
            place. For example, `90` indicating `east`. Often combined with `radius` and/or
            `minCourseDistance`. This parameter takes preference over `matchSideOfStreet`.
            * `sideOfStreetHint`: `{lat},{lng}`. Indicates the side of the street that should be used.
            For example, if the location is to the left of the street, the router will prefer using
            that side in case the street has dividers. For example,
            `52.511496,13.304140;sideOfStreetHint=52.512149,13.304076` indicates that the `north` side
            of the street should be preferred. This options is required, if `matchSideOfStreet` is set
            to `always`. Option cannot be combined with `radius`, `radiusPenalty` or `snapRadius`.
            * `displayLocation`: `{lat},{lng}`. Indicates the physical location of the POI. It is
            different from the originalLocation and location which are generally expected to be on the
            navigable road network, i.e., on segments.
            * `uTurnPermission`: enum `[allow, avoid]`. Specifies the U-Turn Permission mode at the
            stop-over waypoint. If unspecified, the permission will be determined by the global
            setting, avoid[features]=uTurns. This feature is not supported for pass-through waypoints
            and U-Turns are generally avoided in that case.
              + `allow` : Allow making a U-Turn at this stop-over waypoint
              + `avoid` : Avoid making a U-Turn at this stop-over waypoint
            * `matchSideOfStreet`: enum `[always, onlyIfDivided]`. Specifies how the location set by
            `sideOfStreetHint` should be handled. Requires `sideOfStreetHint` to be specified as well.
            Note the exception above when combined with `course`.
              + `always` : Always prefer the given side of street.
              + `onlyIfDivided`: Only prefer using side of street set by `sideOfStreetHint` in case
            the street has dividers. This is the default behavior.
            * `nameHint`: string. Causes the router to look for the place with the most similar name.
            The typical examples include: `North` being used to differentiate between interstates `I66
            North` and `I66 South`, `Downtown Avenue` being used to correctly select a residental
            street.
            * `radius`: int, meters. Sets the radius within which all locations are considered equally
            eligible for selection as waypoints. Typical use cases include scenarios with imprecise
            coordinates or user input provided on low resolution map displays. The value is capped at
            200 meters. Setting a higher value doesn't return an error. Can't be used with
            `snapRadius`.
            * `snapRadius`: int, meters. Sets the radius within which waypoints are matched to the
            most "significant" place. Candidates for matching are sorted in the order of significance
            which is based on the visibility on a zoomed-out map. A highway is considered more
            significant than a national road, while a national road is more significant than a city
            road. Typical use case - selecting waypoints on a  zoomed-out view of a map on a drag-and-
            drop interface, where only significant roads are visible. A big enough radius allows to
            match waypoints to such roads. Can't be used with `radius` or `radiusPenalty` parameters.
            * `radiusPenalty`: int, percentage 0-10000. Penalty as percentage: Used in conjunction
            with the `radius` parameter. Router will match the waypoint within the specified radius
            and apply a penalty to candidates based on their air distance to the waypoint. This
            penalty is proportional to the given percentage, where 100 is just the cost of the air
            distance, and 200 is twice the cost of the air distance. The penalty must be chosen so
            that, when multiplied by the radius, the result is less than or equal to 7200. Regardless,
            only values up to and including 10000 will be accepted. This means that a maximum penalty
            of 3600% is allowed for a radius of 200m, 7200% for 100m and 10000% for 72m and less.
            Higher values will result in an error response. `radiusPenalty` cannot be combined with
            `snapRadius`. **Alpha**: This parameter is in development. It may not be stable and is
            subject to change.

            * `minCourseDistance`: int, meters. Instructs the routing service to try to find a route
            that avoids actions for the indicated distance. For example, if the origin is determined
            by a moving vehicle, the user might not have time to react to early actions. Values
            greater than 2000 meters will be capped at 2000 meters.
            * `segmentIdHint`: string. Causes the router to try and match to the specified segment.
            Waypoint coordinates need to be on the segment, otherwise waypoint will be matched
            ignoring the segment hint. This parameter can be used when the waypoint is too close to
            more than one segment to force matching to a specific one.
            * `onRoadThreshold`: int, meters. allows specifying a distance within which the waypoint
            could be considered as being on a highway/bridge/tunnel/sliproad. Within this threshold,
            the attributes of the segments do not impact the matching. Outside the threshold only
            segments which aren't one of highway/bridge/tunnel/sliproad can be matched.

            Supported waypoint options:
            * `stopDuration`: desired duration for the stop, in seconds.
               `stopDuration` must be less than 50000.
            * `passThrough`: boolean. Asks the router to avoid the following during route calculation:
              + Introducing a stop at the waypoint.
              + Splitting the route into sections.
              + Changing the direction of travel.

            Following scenarios are not supported for `passThrough` parameter:
              + Setting both `stopDuration` to a value greater than 0 and `passThrough=true`.
              + Setting `passThrough=true` for `origin` or `destination` of a route.
              The default value is `false`.
        departure_time (datetime.datetime | Unset): **RFC 3339**, section 5.6 as defined by either
            `date-time` or `date-only` 'T' `partial-time` (ie no time-offset).
        destination (str | Unset): A location defining an origin, destination or via point for a
            route or an isoline.

            Format: `Place[WaypointOptions]`

            * Place: `{lat},{lng}[PlaceOptions]`
            * PlaceOptions: `;option1=value1;option2=value2...`
            * WaypointOptions: `!option1=value1!option2=value2...`

            A waypoint consists of:
            * Exactly one place
            * Optional settings for the place
            * Optional settings for the waypoint itself

            Supported place options:
            * `course`: int, degrees clock-wise from north. Indicates the desired direction from the
            place. For example, `90` indicating `east`. Often combined with `radius` and/or
            `minCourseDistance`. This parameter takes preference over `matchSideOfStreet`.
            * `sideOfStreetHint`: `{lat},{lng}`. Indicates the side of the street that should be used.
            For example, if the location is to the left of the street, the router will prefer using
            that side in case the street has dividers. For example,
            `52.511496,13.304140;sideOfStreetHint=52.512149,13.304076` indicates that the `north` side
            of the street should be preferred. This options is required, if `matchSideOfStreet` is set
            to `always`. Option cannot be combined with `radius`, `radiusPenalty` or `snapRadius`.
            * `displayLocation`: `{lat},{lng}`. Indicates the physical location of the POI. It is
            different from the originalLocation and location which are generally expected to be on the
            navigable road network, i.e., on segments.
            * `uTurnPermission`: enum `[allow, avoid]`. Specifies the U-Turn Permission mode at the
            stop-over waypoint. If unspecified, the permission will be determined by the global
            setting, avoid[features]=uTurns. This feature is not supported for pass-through waypoints
            and U-Turns are generally avoided in that case.
              + `allow` : Allow making a U-Turn at this stop-over waypoint
              + `avoid` : Avoid making a U-Turn at this stop-over waypoint
            * `matchSideOfStreet`: enum `[always, onlyIfDivided]`. Specifies how the location set by
            `sideOfStreetHint` should be handled. Requires `sideOfStreetHint` to be specified as well.
            Note the exception above when combined with `course`.
              + `always` : Always prefer the given side of street.
              + `onlyIfDivided`: Only prefer using side of street set by `sideOfStreetHint` in case
            the street has dividers. This is the default behavior.
            * `nameHint`: string. Causes the router to look for the place with the most similar name.
            The typical examples include: `North` being used to differentiate between interstates `I66
            North` and `I66 South`, `Downtown Avenue` being used to correctly select a residental
            street.
            * `radius`: int, meters. Sets the radius within which all locations are considered equally
            eligible for selection as waypoints. Typical use cases include scenarios with imprecise
            coordinates or user input provided on low resolution map displays. The value is capped at
            200 meters. Setting a higher value doesn't return an error. Can't be used with
            `snapRadius`.
            * `snapRadius`: int, meters. Sets the radius within which waypoints are matched to the
            most "significant" place. Candidates for matching are sorted in the order of significance
            which is based on the visibility on a zoomed-out map. A highway is considered more
            significant than a national road, while a national road is more significant than a city
            road. Typical use case - selecting waypoints on a  zoomed-out view of a map on a drag-and-
            drop interface, where only significant roads are visible. A big enough radius allows to
            match waypoints to such roads. Can't be used with `radius` or `radiusPenalty` parameters.
            * `radiusPenalty`: int, percentage 0-10000. Penalty as percentage: Used in conjunction
            with the `radius` parameter. Router will match the waypoint within the specified radius
            and apply a penalty to candidates based on their air distance to the waypoint. This
            penalty is proportional to the given percentage, where 100 is just the cost of the air
            distance, and 200 is twice the cost of the air distance. The penalty must be chosen so
            that, when multiplied by the radius, the result is less than or equal to 7200. Regardless,
            only values up to and including 10000 will be accepted. This means that a maximum penalty
            of 3600% is allowed for a radius of 200m, 7200% for 100m and 10000% for 72m and less.
            Higher values will result in an error response. `radiusPenalty` cannot be combined with
            `snapRadius`. **Alpha**: This parameter is in development. It may not be stable and is
            subject to change.

            * `minCourseDistance`: int, meters. Instructs the routing service to try to find a route
            that avoids actions for the indicated distance. For example, if the origin is determined
            by a moving vehicle, the user might not have time to react to early actions. Values
            greater than 2000 meters will be capped at 2000 meters.
            * `segmentIdHint`: string. Causes the router to try and match to the specified segment.
            Waypoint coordinates need to be on the segment, otherwise waypoint will be matched
            ignoring the segment hint. This parameter can be used when the waypoint is too close to
            more than one segment to force matching to a specific one.
            * `onRoadThreshold`: int, meters. allows specifying a distance within which the waypoint
            could be considered as being on a highway/bridge/tunnel/sliproad. Within this threshold,
            the attributes of the segments do not impact the matching. Outside the threshold only
            segments which aren't one of highway/bridge/tunnel/sliproad can be matched.

            Supported waypoint options:
            * `stopDuration`: desired duration for the stop, in seconds.
               `stopDuration` must be less than 50000.
            * `passThrough`: boolean. Asks the router to avoid the following during route calculation:
              + Introducing a stop at the waypoint.
              + Splitting the route into sections.
              + Changing the direction of travel.

            Following scenarios are not supported for `passThrough` parameter:
              + Setting both `stopDuration` to a value greater than 0 and `passThrough=true`.
              + Setting `passThrough=true` for `origin` or `destination` of a route.
              The default value is `false`.
        arrival_time (datetime.datetime | Unset): **RFC 3339**, section 5.6 as defined by either
            `date-time` or `date-only` 'T' `partial-time` (ie no time-offset).
        routing_mode (RoutingMode | Unset): Specifies which optimization is applied during the
            calculation.

            * `fast`: Route calculation from start to destination optimized by travel time. In many
              cases, the route returned by `fast` mode may not be the route with the fastest
              possible travel time. For example, the routing service may favor a route that remains on
              a highway, even if a faster travel time can be achieved by taking a detour or shortcut
              through an inconvenient side road.
            * `short`: Route calculation from start to destination disregarding any speed information.
              In this mode, the distance of the route is minimized, while keeping the route sensible.
              This includes, for example, penalizing turns. Because of that, the resulting route will
              not necessarily be the one with minimal distance.

            Notes:
            * The following Transport modes only support `fast` routingMode
              - `bicycle`
              - `bus`
              - `pedestrian`
              - `privateBus`
              - `scooter`
              - `taxi`
        shape (Shape | Unset): A struct used to control the shape of the returned isolines.
        optimize_for (CalculateIsolinesOptimizeFor | Unset):  Default:
            CalculateIsolinesOptimizeFor.BALANCED.
        avoid (Avoid | Unset):
        exclude (Exclude | Unset): Options to exclude strictly during the route calculation.
        allow (Allow | Unset): Explicitly allow features that require users to opt in.
        truck (Truck | Unset): Vehicle-specific parameters
        vehicle (Vehicle | Unset): Vehicle-specific parameters
        consumption_model (str | Unset): Extensible enum: `empirical` `physical` `...`
            Specifies which of the EV consumption models is being used. See the `ev` parameter for
            details on the models.

            * `empirical`
            * `physical`

            **Alpha**: Physical consumption model is in development. It may not be stable and is
            subject to change.
        ev (BaseEVEmpiricalModel | BaseEVPhysicalModel | Unset): EV parameters to be used for
            calculating consumption and for calculating isolines for EV.

            There are two consumption models (`empirical`, `physical`). Set the `consumptionModel`
            parameter to choose which model to use.

            Required `empirical` model properties:
            * `freeFlowSpeedTable`

            Required `physical` model properties:
            * `driveEfficiency`
            * `recuperationEfficiency`

            When using the physical model, certain properties of the `vehicle` parameter are also
            required (see documentation for the `vehicle` parameter for more details):
            * `rollingResistanceCoefficient`
            * `airDragCoefficient`
            * `currentWeight`
            * `frontalArea` or combination of `width` and `height`
        fuel (Fuel | Unset): Fuel parameters to be used for calculating consumption and
            consumption-based isolines for fuel-based vehicles
            using empirical consumption model.

            Attributes:
            * `type`
            * `freeFlowSpeedTable`
            * `trafficSpeedTable`
            * `additionalConsumption`
            * `ascent`
        max_speed_on_segment (str | Unset): A comma separated list of segments with restrictions
            on maximum baseSpeed.

            Each entry has the following structure:
            `{segmentId}(#{direction})?;speed={maxBaseSpeed}`

            The individual parts are:
            * segmentId: The identifier of the referenced topology segment inside the catalog,
            example: `here:cm:segment:207551710`
            * direction (optional): Either '*' for bidirectional (default), '+' for positive
            direction, or '-' for negative direction
            * maxBaseSpeed: New value in m/s of baseSpeed on segment

            Example of a parameter value excluding two segments:
            `here:cm:segment:207551710#+;speed=10,here:cm:segment:76771992;speed=1`

            **Notes**:
            - It does not increase default baseSpeed on segment. If the value is greater than the
            default base speed, then such penalty will have no effect.
            - Minimum valid value for speed is 1
            - Using segments with a modified base speed does not trigger any notifications
            - Maximum number of penalized segments in one request cannot be greater than 1000.
              "penalized segments" refer to segments that have a restrictions on maximum baseSpeed
            with `maxSpeedOnSegment`
              or avoided with `avoid[segments]`
            - In case the same segment is penalized multiple times through values provided in the
            query string and/or the POST body,
              then the most restrictive value will be applied.
        taxi (Taxi | Unset): Taxi-specific parameters
        traffic (Traffic | Unset): Traffic specific parameters.
        billing_tag (str | Unset):  Example: ABCD+EFGH.
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthErrorResponseSchema | AuthErrorResponseSchema | NotAllowed | IsolineErrorResponse | IsolineResponse | ServerInternal
    """

    return sync_detailed(
        client=client,
        range_=range_,
        transport_mode=transport_mode,
        origin=origin,
        departure_time=departure_time,
        destination=destination,
        arrival_time=arrival_time,
        routing_mode=routing_mode,
        shape=shape,
        optimize_for=optimize_for,
        avoid=avoid,
        exclude=exclude,
        allow=allow,
        truck=truck,
        vehicle=vehicle,
        consumption_model=consumption_model,
        ev=ev,
        fuel=fuel,
        max_speed_on_segment=max_speed_on_segment,
        taxi=taxi,
        traffic=traffic,
        billing_tag=billing_tag,
        x_request_id=x_request_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    range_: Range,
    transport_mode: RouterMode,
    origin: str | Unset = UNSET,
    departure_time: datetime.datetime | Unset = UNSET,
    destination: str | Unset = UNSET,
    arrival_time: datetime.datetime | Unset = UNSET,
    routing_mode: RoutingMode | Unset = UNSET,
    shape: Shape | Unset = UNSET,
    optimize_for: CalculateIsolinesOptimizeFor
    | Unset = CalculateIsolinesOptimizeFor.BALANCED,
    avoid: Avoid | Unset = UNSET,
    exclude: Exclude | Unset = UNSET,
    allow: Allow | Unset = UNSET,
    truck: Truck | Unset = UNSET,
    vehicle: Vehicle | Unset = UNSET,
    consumption_model: str | Unset = UNSET,
    ev: BaseEVEmpiricalModel | BaseEVPhysicalModel | Unset = UNSET,
    fuel: Fuel | Unset = UNSET,
    max_speed_on_segment: str | Unset = UNSET,
    taxi: Taxi | Unset = UNSET,
    traffic: Traffic | Unset = UNSET,
    billing_tag: str | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[
    AuthErrorResponseSchema
    | AuthErrorResponseSchema
    | NotAllowed
    | IsolineErrorResponse
    | IsolineResponse
    | ServerInternal
]:
    """Get Isolines for specified ranges around a center point

     Retrieves a list of polylines that captures the approximate reachable area
    from the specified center point constrained by the provided parameters.

    Args:
        range_ (Range): Ranges specified in terms of distance, travel time or energy consumption.
        transport_mode (RouterMode): Mode of transport to be used for route calculation.
        origin (str | Unset): A location defining an origin, destination or via point for a route
            or an isoline.

            Format: `Place[WaypointOptions]`

            * Place: `{lat},{lng}[PlaceOptions]`
            * PlaceOptions: `;option1=value1;option2=value2...`
            * WaypointOptions: `!option1=value1!option2=value2...`

            A waypoint consists of:
            * Exactly one place
            * Optional settings for the place
            * Optional settings for the waypoint itself

            Supported place options:
            * `course`: int, degrees clock-wise from north. Indicates the desired direction from the
            place. For example, `90` indicating `east`. Often combined with `radius` and/or
            `minCourseDistance`. This parameter takes preference over `matchSideOfStreet`.
            * `sideOfStreetHint`: `{lat},{lng}`. Indicates the side of the street that should be used.
            For example, if the location is to the left of the street, the router will prefer using
            that side in case the street has dividers. For example,
            `52.511496,13.304140;sideOfStreetHint=52.512149,13.304076` indicates that the `north` side
            of the street should be preferred. This options is required, if `matchSideOfStreet` is set
            to `always`. Option cannot be combined with `radius`, `radiusPenalty` or `snapRadius`.
            * `displayLocation`: `{lat},{lng}`. Indicates the physical location of the POI. It is
            different from the originalLocation and location which are generally expected to be on the
            navigable road network, i.e., on segments.
            * `uTurnPermission`: enum `[allow, avoid]`. Specifies the U-Turn Permission mode at the
            stop-over waypoint. If unspecified, the permission will be determined by the global
            setting, avoid[features]=uTurns. This feature is not supported for pass-through waypoints
            and U-Turns are generally avoided in that case.
              + `allow` : Allow making a U-Turn at this stop-over waypoint
              + `avoid` : Avoid making a U-Turn at this stop-over waypoint
            * `matchSideOfStreet`: enum `[always, onlyIfDivided]`. Specifies how the location set by
            `sideOfStreetHint` should be handled. Requires `sideOfStreetHint` to be specified as well.
            Note the exception above when combined with `course`.
              + `always` : Always prefer the given side of street.
              + `onlyIfDivided`: Only prefer using side of street set by `sideOfStreetHint` in case
            the street has dividers. This is the default behavior.
            * `nameHint`: string. Causes the router to look for the place with the most similar name.
            The typical examples include: `North` being used to differentiate between interstates `I66
            North` and `I66 South`, `Downtown Avenue` being used to correctly select a residental
            street.
            * `radius`: int, meters. Sets the radius within which all locations are considered equally
            eligible for selection as waypoints. Typical use cases include scenarios with imprecise
            coordinates or user input provided on low resolution map displays. The value is capped at
            200 meters. Setting a higher value doesn't return an error. Can't be used with
            `snapRadius`.
            * `snapRadius`: int, meters. Sets the radius within which waypoints are matched to the
            most "significant" place. Candidates for matching are sorted in the order of significance
            which is based on the visibility on a zoomed-out map. A highway is considered more
            significant than a national road, while a national road is more significant than a city
            road. Typical use case - selecting waypoints on a  zoomed-out view of a map on a drag-and-
            drop interface, where only significant roads are visible. A big enough radius allows to
            match waypoints to such roads. Can't be used with `radius` or `radiusPenalty` parameters.
            * `radiusPenalty`: int, percentage 0-10000. Penalty as percentage: Used in conjunction
            with the `radius` parameter. Router will match the waypoint within the specified radius
            and apply a penalty to candidates based on their air distance to the waypoint. This
            penalty is proportional to the given percentage, where 100 is just the cost of the air
            distance, and 200 is twice the cost of the air distance. The penalty must be chosen so
            that, when multiplied by the radius, the result is less than or equal to 7200. Regardless,
            only values up to and including 10000 will be accepted. This means that a maximum penalty
            of 3600% is allowed for a radius of 200m, 7200% for 100m and 10000% for 72m and less.
            Higher values will result in an error response. `radiusPenalty` cannot be combined with
            `snapRadius`. **Alpha**: This parameter is in development. It may not be stable and is
            subject to change.

            * `minCourseDistance`: int, meters. Instructs the routing service to try to find a route
            that avoids actions for the indicated distance. For example, if the origin is determined
            by a moving vehicle, the user might not have time to react to early actions. Values
            greater than 2000 meters will be capped at 2000 meters.
            * `segmentIdHint`: string. Causes the router to try and match to the specified segment.
            Waypoint coordinates need to be on the segment, otherwise waypoint will be matched
            ignoring the segment hint. This parameter can be used when the waypoint is too close to
            more than one segment to force matching to a specific one.
            * `onRoadThreshold`: int, meters. allows specifying a distance within which the waypoint
            could be considered as being on a highway/bridge/tunnel/sliproad. Within this threshold,
            the attributes of the segments do not impact the matching. Outside the threshold only
            segments which aren't one of highway/bridge/tunnel/sliproad can be matched.

            Supported waypoint options:
            * `stopDuration`: desired duration for the stop, in seconds.
               `stopDuration` must be less than 50000.
            * `passThrough`: boolean. Asks the router to avoid the following during route calculation:
              + Introducing a stop at the waypoint.
              + Splitting the route into sections.
              + Changing the direction of travel.

            Following scenarios are not supported for `passThrough` parameter:
              + Setting both `stopDuration` to a value greater than 0 and `passThrough=true`.
              + Setting `passThrough=true` for `origin` or `destination` of a route.
              The default value is `false`.
        departure_time (datetime.datetime | Unset): **RFC 3339**, section 5.6 as defined by either
            `date-time` or `date-only` 'T' `partial-time` (ie no time-offset).
        destination (str | Unset): A location defining an origin, destination or via point for a
            route or an isoline.

            Format: `Place[WaypointOptions]`

            * Place: `{lat},{lng}[PlaceOptions]`
            * PlaceOptions: `;option1=value1;option2=value2...`
            * WaypointOptions: `!option1=value1!option2=value2...`

            A waypoint consists of:
            * Exactly one place
            * Optional settings for the place
            * Optional settings for the waypoint itself

            Supported place options:
            * `course`: int, degrees clock-wise from north. Indicates the desired direction from the
            place. For example, `90` indicating `east`. Often combined with `radius` and/or
            `minCourseDistance`. This parameter takes preference over `matchSideOfStreet`.
            * `sideOfStreetHint`: `{lat},{lng}`. Indicates the side of the street that should be used.
            For example, if the location is to the left of the street, the router will prefer using
            that side in case the street has dividers. For example,
            `52.511496,13.304140;sideOfStreetHint=52.512149,13.304076` indicates that the `north` side
            of the street should be preferred. This options is required, if `matchSideOfStreet` is set
            to `always`. Option cannot be combined with `radius`, `radiusPenalty` or `snapRadius`.
            * `displayLocation`: `{lat},{lng}`. Indicates the physical location of the POI. It is
            different from the originalLocation and location which are generally expected to be on the
            navigable road network, i.e., on segments.
            * `uTurnPermission`: enum `[allow, avoid]`. Specifies the U-Turn Permission mode at the
            stop-over waypoint. If unspecified, the permission will be determined by the global
            setting, avoid[features]=uTurns. This feature is not supported for pass-through waypoints
            and U-Turns are generally avoided in that case.
              + `allow` : Allow making a U-Turn at this stop-over waypoint
              + `avoid` : Avoid making a U-Turn at this stop-over waypoint
            * `matchSideOfStreet`: enum `[always, onlyIfDivided]`. Specifies how the location set by
            `sideOfStreetHint` should be handled. Requires `sideOfStreetHint` to be specified as well.
            Note the exception above when combined with `course`.
              + `always` : Always prefer the given side of street.
              + `onlyIfDivided`: Only prefer using side of street set by `sideOfStreetHint` in case
            the street has dividers. This is the default behavior.
            * `nameHint`: string. Causes the router to look for the place with the most similar name.
            The typical examples include: `North` being used to differentiate between interstates `I66
            North` and `I66 South`, `Downtown Avenue` being used to correctly select a residental
            street.
            * `radius`: int, meters. Sets the radius within which all locations are considered equally
            eligible for selection as waypoints. Typical use cases include scenarios with imprecise
            coordinates or user input provided on low resolution map displays. The value is capped at
            200 meters. Setting a higher value doesn't return an error. Can't be used with
            `snapRadius`.
            * `snapRadius`: int, meters. Sets the radius within which waypoints are matched to the
            most "significant" place. Candidates for matching are sorted in the order of significance
            which is based on the visibility on a zoomed-out map. A highway is considered more
            significant than a national road, while a national road is more significant than a city
            road. Typical use case - selecting waypoints on a  zoomed-out view of a map on a drag-and-
            drop interface, where only significant roads are visible. A big enough radius allows to
            match waypoints to such roads. Can't be used with `radius` or `radiusPenalty` parameters.
            * `radiusPenalty`: int, percentage 0-10000. Penalty as percentage: Used in conjunction
            with the `radius` parameter. Router will match the waypoint within the specified radius
            and apply a penalty to candidates based on their air distance to the waypoint. This
            penalty is proportional to the given percentage, where 100 is just the cost of the air
            distance, and 200 is twice the cost of the air distance. The penalty must be chosen so
            that, when multiplied by the radius, the result is less than or equal to 7200. Regardless,
            only values up to and including 10000 will be accepted. This means that a maximum penalty
            of 3600% is allowed for a radius of 200m, 7200% for 100m and 10000% for 72m and less.
            Higher values will result in an error response. `radiusPenalty` cannot be combined with
            `snapRadius`. **Alpha**: This parameter is in development. It may not be stable and is
            subject to change.

            * `minCourseDistance`: int, meters. Instructs the routing service to try to find a route
            that avoids actions for the indicated distance. For example, if the origin is determined
            by a moving vehicle, the user might not have time to react to early actions. Values
            greater than 2000 meters will be capped at 2000 meters.
            * `segmentIdHint`: string. Causes the router to try and match to the specified segment.
            Waypoint coordinates need to be on the segment, otherwise waypoint will be matched
            ignoring the segment hint. This parameter can be used when the waypoint is too close to
            more than one segment to force matching to a specific one.
            * `onRoadThreshold`: int, meters. allows specifying a distance within which the waypoint
            could be considered as being on a highway/bridge/tunnel/sliproad. Within this threshold,
            the attributes of the segments do not impact the matching. Outside the threshold only
            segments which aren't one of highway/bridge/tunnel/sliproad can be matched.

            Supported waypoint options:
            * `stopDuration`: desired duration for the stop, in seconds.
               `stopDuration` must be less than 50000.
            * `passThrough`: boolean. Asks the router to avoid the following during route calculation:
              + Introducing a stop at the waypoint.
              + Splitting the route into sections.
              + Changing the direction of travel.

            Following scenarios are not supported for `passThrough` parameter:
              + Setting both `stopDuration` to a value greater than 0 and `passThrough=true`.
              + Setting `passThrough=true` for `origin` or `destination` of a route.
              The default value is `false`.
        arrival_time (datetime.datetime | Unset): **RFC 3339**, section 5.6 as defined by either
            `date-time` or `date-only` 'T' `partial-time` (ie no time-offset).
        routing_mode (RoutingMode | Unset): Specifies which optimization is applied during the
            calculation.

            * `fast`: Route calculation from start to destination optimized by travel time. In many
              cases, the route returned by `fast` mode may not be the route with the fastest
              possible travel time. For example, the routing service may favor a route that remains on
              a highway, even if a faster travel time can be achieved by taking a detour or shortcut
              through an inconvenient side road.
            * `short`: Route calculation from start to destination disregarding any speed information.
              In this mode, the distance of the route is minimized, while keeping the route sensible.
              This includes, for example, penalizing turns. Because of that, the resulting route will
              not necessarily be the one with minimal distance.

            Notes:
            * The following Transport modes only support `fast` routingMode
              - `bicycle`
              - `bus`
              - `pedestrian`
              - `privateBus`
              - `scooter`
              - `taxi`
        shape (Shape | Unset): A struct used to control the shape of the returned isolines.
        optimize_for (CalculateIsolinesOptimizeFor | Unset):  Default:
            CalculateIsolinesOptimizeFor.BALANCED.
        avoid (Avoid | Unset):
        exclude (Exclude | Unset): Options to exclude strictly during the route calculation.
        allow (Allow | Unset): Explicitly allow features that require users to opt in.
        truck (Truck | Unset): Vehicle-specific parameters
        vehicle (Vehicle | Unset): Vehicle-specific parameters
        consumption_model (str | Unset): Extensible enum: `empirical` `physical` `...`
            Specifies which of the EV consumption models is being used. See the `ev` parameter for
            details on the models.

            * `empirical`
            * `physical`

            **Alpha**: Physical consumption model is in development. It may not be stable and is
            subject to change.
        ev (BaseEVEmpiricalModel | BaseEVPhysicalModel | Unset): EV parameters to be used for
            calculating consumption and for calculating isolines for EV.

            There are two consumption models (`empirical`, `physical`). Set the `consumptionModel`
            parameter to choose which model to use.

            Required `empirical` model properties:
            * `freeFlowSpeedTable`

            Required `physical` model properties:
            * `driveEfficiency`
            * `recuperationEfficiency`

            When using the physical model, certain properties of the `vehicle` parameter are also
            required (see documentation for the `vehicle` parameter for more details):
            * `rollingResistanceCoefficient`
            * `airDragCoefficient`
            * `currentWeight`
            * `frontalArea` or combination of `width` and `height`
        fuel (Fuel | Unset): Fuel parameters to be used for calculating consumption and
            consumption-based isolines for fuel-based vehicles
            using empirical consumption model.

            Attributes:
            * `type`
            * `freeFlowSpeedTable`
            * `trafficSpeedTable`
            * `additionalConsumption`
            * `ascent`
        max_speed_on_segment (str | Unset): A comma separated list of segments with restrictions
            on maximum baseSpeed.

            Each entry has the following structure:
            `{segmentId}(#{direction})?;speed={maxBaseSpeed}`

            The individual parts are:
            * segmentId: The identifier of the referenced topology segment inside the catalog,
            example: `here:cm:segment:207551710`
            * direction (optional): Either '*' for bidirectional (default), '+' for positive
            direction, or '-' for negative direction
            * maxBaseSpeed: New value in m/s of baseSpeed on segment

            Example of a parameter value excluding two segments:
            `here:cm:segment:207551710#+;speed=10,here:cm:segment:76771992;speed=1`

            **Notes**:
            - It does not increase default baseSpeed on segment. If the value is greater than the
            default base speed, then such penalty will have no effect.
            - Minimum valid value for speed is 1
            - Using segments with a modified base speed does not trigger any notifications
            - Maximum number of penalized segments in one request cannot be greater than 1000.
              "penalized segments" refer to segments that have a restrictions on maximum baseSpeed
            with `maxSpeedOnSegment`
              or avoided with `avoid[segments]`
            - In case the same segment is penalized multiple times through values provided in the
            query string and/or the POST body,
              then the most restrictive value will be applied.
        taxi (Taxi | Unset): Taxi-specific parameters
        traffic (Traffic | Unset): Traffic specific parameters.
        billing_tag (str | Unset):  Example: ABCD+EFGH.
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthErrorResponseSchema | AuthErrorResponseSchema | NotAllowed | IsolineErrorResponse | IsolineResponse | ServerInternal]
    """

    kwargs = _get_kwargs(
        range_=range_,
        transport_mode=transport_mode,
        origin=origin,
        departure_time=departure_time,
        destination=destination,
        arrival_time=arrival_time,
        routing_mode=routing_mode,
        shape=shape,
        optimize_for=optimize_for,
        avoid=avoid,
        exclude=exclude,
        allow=allow,
        truck=truck,
        vehicle=vehicle,
        consumption_model=consumption_model,
        ev=ev,
        fuel=fuel,
        max_speed_on_segment=max_speed_on_segment,
        taxi=taxi,
        traffic=traffic,
        billing_tag=billing_tag,
        x_request_id=x_request_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    range_: Range,
    transport_mode: RouterMode,
    origin: str | Unset = UNSET,
    departure_time: datetime.datetime | Unset = UNSET,
    destination: str | Unset = UNSET,
    arrival_time: datetime.datetime | Unset = UNSET,
    routing_mode: RoutingMode | Unset = UNSET,
    shape: Shape | Unset = UNSET,
    optimize_for: CalculateIsolinesOptimizeFor
    | Unset = CalculateIsolinesOptimizeFor.BALANCED,
    avoid: Avoid | Unset = UNSET,
    exclude: Exclude | Unset = UNSET,
    allow: Allow | Unset = UNSET,
    truck: Truck | Unset = UNSET,
    vehicle: Vehicle | Unset = UNSET,
    consumption_model: str | Unset = UNSET,
    ev: BaseEVEmpiricalModel | BaseEVPhysicalModel | Unset = UNSET,
    fuel: Fuel | Unset = UNSET,
    max_speed_on_segment: str | Unset = UNSET,
    taxi: Taxi | Unset = UNSET,
    traffic: Traffic | Unset = UNSET,
    billing_tag: str | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> (
    AuthErrorResponseSchema
    | AuthErrorResponseSchema
    | NotAllowed
    | IsolineErrorResponse
    | IsolineResponse
    | ServerInternal
    | None
):
    """Get Isolines for specified ranges around a center point

     Retrieves a list of polylines that captures the approximate reachable area
    from the specified center point constrained by the provided parameters.

    Args:
        range_ (Range): Ranges specified in terms of distance, travel time or energy consumption.
        transport_mode (RouterMode): Mode of transport to be used for route calculation.
        origin (str | Unset): A location defining an origin, destination or via point for a route
            or an isoline.

            Format: `Place[WaypointOptions]`

            * Place: `{lat},{lng}[PlaceOptions]`
            * PlaceOptions: `;option1=value1;option2=value2...`
            * WaypointOptions: `!option1=value1!option2=value2...`

            A waypoint consists of:
            * Exactly one place
            * Optional settings for the place
            * Optional settings for the waypoint itself

            Supported place options:
            * `course`: int, degrees clock-wise from north. Indicates the desired direction from the
            place. For example, `90` indicating `east`. Often combined with `radius` and/or
            `minCourseDistance`. This parameter takes preference over `matchSideOfStreet`.
            * `sideOfStreetHint`: `{lat},{lng}`. Indicates the side of the street that should be used.
            For example, if the location is to the left of the street, the router will prefer using
            that side in case the street has dividers. For example,
            `52.511496,13.304140;sideOfStreetHint=52.512149,13.304076` indicates that the `north` side
            of the street should be preferred. This options is required, if `matchSideOfStreet` is set
            to `always`. Option cannot be combined with `radius`, `radiusPenalty` or `snapRadius`.
            * `displayLocation`: `{lat},{lng}`. Indicates the physical location of the POI. It is
            different from the originalLocation and location which are generally expected to be on the
            navigable road network, i.e., on segments.
            * `uTurnPermission`: enum `[allow, avoid]`. Specifies the U-Turn Permission mode at the
            stop-over waypoint. If unspecified, the permission will be determined by the global
            setting, avoid[features]=uTurns. This feature is not supported for pass-through waypoints
            and U-Turns are generally avoided in that case.
              + `allow` : Allow making a U-Turn at this stop-over waypoint
              + `avoid` : Avoid making a U-Turn at this stop-over waypoint
            * `matchSideOfStreet`: enum `[always, onlyIfDivided]`. Specifies how the location set by
            `sideOfStreetHint` should be handled. Requires `sideOfStreetHint` to be specified as well.
            Note the exception above when combined with `course`.
              + `always` : Always prefer the given side of street.
              + `onlyIfDivided`: Only prefer using side of street set by `sideOfStreetHint` in case
            the street has dividers. This is the default behavior.
            * `nameHint`: string. Causes the router to look for the place with the most similar name.
            The typical examples include: `North` being used to differentiate between interstates `I66
            North` and `I66 South`, `Downtown Avenue` being used to correctly select a residental
            street.
            * `radius`: int, meters. Sets the radius within which all locations are considered equally
            eligible for selection as waypoints. Typical use cases include scenarios with imprecise
            coordinates or user input provided on low resolution map displays. The value is capped at
            200 meters. Setting a higher value doesn't return an error. Can't be used with
            `snapRadius`.
            * `snapRadius`: int, meters. Sets the radius within which waypoints are matched to the
            most "significant" place. Candidates for matching are sorted in the order of significance
            which is based on the visibility on a zoomed-out map. A highway is considered more
            significant than a national road, while a national road is more significant than a city
            road. Typical use case - selecting waypoints on a  zoomed-out view of a map on a drag-and-
            drop interface, where only significant roads are visible. A big enough radius allows to
            match waypoints to such roads. Can't be used with `radius` or `radiusPenalty` parameters.
            * `radiusPenalty`: int, percentage 0-10000. Penalty as percentage: Used in conjunction
            with the `radius` parameter. Router will match the waypoint within the specified radius
            and apply a penalty to candidates based on their air distance to the waypoint. This
            penalty is proportional to the given percentage, where 100 is just the cost of the air
            distance, and 200 is twice the cost of the air distance. The penalty must be chosen so
            that, when multiplied by the radius, the result is less than or equal to 7200. Regardless,
            only values up to and including 10000 will be accepted. This means that a maximum penalty
            of 3600% is allowed for a radius of 200m, 7200% for 100m and 10000% for 72m and less.
            Higher values will result in an error response. `radiusPenalty` cannot be combined with
            `snapRadius`. **Alpha**: This parameter is in development. It may not be stable and is
            subject to change.

            * `minCourseDistance`: int, meters. Instructs the routing service to try to find a route
            that avoids actions for the indicated distance. For example, if the origin is determined
            by a moving vehicle, the user might not have time to react to early actions. Values
            greater than 2000 meters will be capped at 2000 meters.
            * `segmentIdHint`: string. Causes the router to try and match to the specified segment.
            Waypoint coordinates need to be on the segment, otherwise waypoint will be matched
            ignoring the segment hint. This parameter can be used when the waypoint is too close to
            more than one segment to force matching to a specific one.
            * `onRoadThreshold`: int, meters. allows specifying a distance within which the waypoint
            could be considered as being on a highway/bridge/tunnel/sliproad. Within this threshold,
            the attributes of the segments do not impact the matching. Outside the threshold only
            segments which aren't one of highway/bridge/tunnel/sliproad can be matched.

            Supported waypoint options:
            * `stopDuration`: desired duration for the stop, in seconds.
               `stopDuration` must be less than 50000.
            * `passThrough`: boolean. Asks the router to avoid the following during route calculation:
              + Introducing a stop at the waypoint.
              + Splitting the route into sections.
              + Changing the direction of travel.

            Following scenarios are not supported for `passThrough` parameter:
              + Setting both `stopDuration` to a value greater than 0 and `passThrough=true`.
              + Setting `passThrough=true` for `origin` or `destination` of a route.
              The default value is `false`.
        departure_time (datetime.datetime | Unset): **RFC 3339**, section 5.6 as defined by either
            `date-time` or `date-only` 'T' `partial-time` (ie no time-offset).
        destination (str | Unset): A location defining an origin, destination or via point for a
            route or an isoline.

            Format: `Place[WaypointOptions]`

            * Place: `{lat},{lng}[PlaceOptions]`
            * PlaceOptions: `;option1=value1;option2=value2...`
            * WaypointOptions: `!option1=value1!option2=value2...`

            A waypoint consists of:
            * Exactly one place
            * Optional settings for the place
            * Optional settings for the waypoint itself

            Supported place options:
            * `course`: int, degrees clock-wise from north. Indicates the desired direction from the
            place. For example, `90` indicating `east`. Often combined with `radius` and/or
            `minCourseDistance`. This parameter takes preference over `matchSideOfStreet`.
            * `sideOfStreetHint`: `{lat},{lng}`. Indicates the side of the street that should be used.
            For example, if the location is to the left of the street, the router will prefer using
            that side in case the street has dividers. For example,
            `52.511496,13.304140;sideOfStreetHint=52.512149,13.304076` indicates that the `north` side
            of the street should be preferred. This options is required, if `matchSideOfStreet` is set
            to `always`. Option cannot be combined with `radius`, `radiusPenalty` or `snapRadius`.
            * `displayLocation`: `{lat},{lng}`. Indicates the physical location of the POI. It is
            different from the originalLocation and location which are generally expected to be on the
            navigable road network, i.e., on segments.
            * `uTurnPermission`: enum `[allow, avoid]`. Specifies the U-Turn Permission mode at the
            stop-over waypoint. If unspecified, the permission will be determined by the global
            setting, avoid[features]=uTurns. This feature is not supported for pass-through waypoints
            and U-Turns are generally avoided in that case.
              + `allow` : Allow making a U-Turn at this stop-over waypoint
              + `avoid` : Avoid making a U-Turn at this stop-over waypoint
            * `matchSideOfStreet`: enum `[always, onlyIfDivided]`. Specifies how the location set by
            `sideOfStreetHint` should be handled. Requires `sideOfStreetHint` to be specified as well.
            Note the exception above when combined with `course`.
              + `always` : Always prefer the given side of street.
              + `onlyIfDivided`: Only prefer using side of street set by `sideOfStreetHint` in case
            the street has dividers. This is the default behavior.
            * `nameHint`: string. Causes the router to look for the place with the most similar name.
            The typical examples include: `North` being used to differentiate between interstates `I66
            North` and `I66 South`, `Downtown Avenue` being used to correctly select a residental
            street.
            * `radius`: int, meters. Sets the radius within which all locations are considered equally
            eligible for selection as waypoints. Typical use cases include scenarios with imprecise
            coordinates or user input provided on low resolution map displays. The value is capped at
            200 meters. Setting a higher value doesn't return an error. Can't be used with
            `snapRadius`.
            * `snapRadius`: int, meters. Sets the radius within which waypoints are matched to the
            most "significant" place. Candidates for matching are sorted in the order of significance
            which is based on the visibility on a zoomed-out map. A highway is considered more
            significant than a national road, while a national road is more significant than a city
            road. Typical use case - selecting waypoints on a  zoomed-out view of a map on a drag-and-
            drop interface, where only significant roads are visible. A big enough radius allows to
            match waypoints to such roads. Can't be used with `radius` or `radiusPenalty` parameters.
            * `radiusPenalty`: int, percentage 0-10000. Penalty as percentage: Used in conjunction
            with the `radius` parameter. Router will match the waypoint within the specified radius
            and apply a penalty to candidates based on their air distance to the waypoint. This
            penalty is proportional to the given percentage, where 100 is just the cost of the air
            distance, and 200 is twice the cost of the air distance. The penalty must be chosen so
            that, when multiplied by the radius, the result is less than or equal to 7200. Regardless,
            only values up to and including 10000 will be accepted. This means that a maximum penalty
            of 3600% is allowed for a radius of 200m, 7200% for 100m and 10000% for 72m and less.
            Higher values will result in an error response. `radiusPenalty` cannot be combined with
            `snapRadius`. **Alpha**: This parameter is in development. It may not be stable and is
            subject to change.

            * `minCourseDistance`: int, meters. Instructs the routing service to try to find a route
            that avoids actions for the indicated distance. For example, if the origin is determined
            by a moving vehicle, the user might not have time to react to early actions. Values
            greater than 2000 meters will be capped at 2000 meters.
            * `segmentIdHint`: string. Causes the router to try and match to the specified segment.
            Waypoint coordinates need to be on the segment, otherwise waypoint will be matched
            ignoring the segment hint. This parameter can be used when the waypoint is too close to
            more than one segment to force matching to a specific one.
            * `onRoadThreshold`: int, meters. allows specifying a distance within which the waypoint
            could be considered as being on a highway/bridge/tunnel/sliproad. Within this threshold,
            the attributes of the segments do not impact the matching. Outside the threshold only
            segments which aren't one of highway/bridge/tunnel/sliproad can be matched.

            Supported waypoint options:
            * `stopDuration`: desired duration for the stop, in seconds.
               `stopDuration` must be less than 50000.
            * `passThrough`: boolean. Asks the router to avoid the following during route calculation:
              + Introducing a stop at the waypoint.
              + Splitting the route into sections.
              + Changing the direction of travel.

            Following scenarios are not supported for `passThrough` parameter:
              + Setting both `stopDuration` to a value greater than 0 and `passThrough=true`.
              + Setting `passThrough=true` for `origin` or `destination` of a route.
              The default value is `false`.
        arrival_time (datetime.datetime | Unset): **RFC 3339**, section 5.6 as defined by either
            `date-time` or `date-only` 'T' `partial-time` (ie no time-offset).
        routing_mode (RoutingMode | Unset): Specifies which optimization is applied during the
            calculation.

            * `fast`: Route calculation from start to destination optimized by travel time. In many
              cases, the route returned by `fast` mode may not be the route with the fastest
              possible travel time. For example, the routing service may favor a route that remains on
              a highway, even if a faster travel time can be achieved by taking a detour or shortcut
              through an inconvenient side road.
            * `short`: Route calculation from start to destination disregarding any speed information.
              In this mode, the distance of the route is minimized, while keeping the route sensible.
              This includes, for example, penalizing turns. Because of that, the resulting route will
              not necessarily be the one with minimal distance.

            Notes:
            * The following Transport modes only support `fast` routingMode
              - `bicycle`
              - `bus`
              - `pedestrian`
              - `privateBus`
              - `scooter`
              - `taxi`
        shape (Shape | Unset): A struct used to control the shape of the returned isolines.
        optimize_for (CalculateIsolinesOptimizeFor | Unset):  Default:
            CalculateIsolinesOptimizeFor.BALANCED.
        avoid (Avoid | Unset):
        exclude (Exclude | Unset): Options to exclude strictly during the route calculation.
        allow (Allow | Unset): Explicitly allow features that require users to opt in.
        truck (Truck | Unset): Vehicle-specific parameters
        vehicle (Vehicle | Unset): Vehicle-specific parameters
        consumption_model (str | Unset): Extensible enum: `empirical` `physical` `...`
            Specifies which of the EV consumption models is being used. See the `ev` parameter for
            details on the models.

            * `empirical`
            * `physical`

            **Alpha**: Physical consumption model is in development. It may not be stable and is
            subject to change.
        ev (BaseEVEmpiricalModel | BaseEVPhysicalModel | Unset): EV parameters to be used for
            calculating consumption and for calculating isolines for EV.

            There are two consumption models (`empirical`, `physical`). Set the `consumptionModel`
            parameter to choose which model to use.

            Required `empirical` model properties:
            * `freeFlowSpeedTable`

            Required `physical` model properties:
            * `driveEfficiency`
            * `recuperationEfficiency`

            When using the physical model, certain properties of the `vehicle` parameter are also
            required (see documentation for the `vehicle` parameter for more details):
            * `rollingResistanceCoefficient`
            * `airDragCoefficient`
            * `currentWeight`
            * `frontalArea` or combination of `width` and `height`
        fuel (Fuel | Unset): Fuel parameters to be used for calculating consumption and
            consumption-based isolines for fuel-based vehicles
            using empirical consumption model.

            Attributes:
            * `type`
            * `freeFlowSpeedTable`
            * `trafficSpeedTable`
            * `additionalConsumption`
            * `ascent`
        max_speed_on_segment (str | Unset): A comma separated list of segments with restrictions
            on maximum baseSpeed.

            Each entry has the following structure:
            `{segmentId}(#{direction})?;speed={maxBaseSpeed}`

            The individual parts are:
            * segmentId: The identifier of the referenced topology segment inside the catalog,
            example: `here:cm:segment:207551710`
            * direction (optional): Either '*' for bidirectional (default), '+' for positive
            direction, or '-' for negative direction
            * maxBaseSpeed: New value in m/s of baseSpeed on segment

            Example of a parameter value excluding two segments:
            `here:cm:segment:207551710#+;speed=10,here:cm:segment:76771992;speed=1`

            **Notes**:
            - It does not increase default baseSpeed on segment. If the value is greater than the
            default base speed, then such penalty will have no effect.
            - Minimum valid value for speed is 1
            - Using segments with a modified base speed does not trigger any notifications
            - Maximum number of penalized segments in one request cannot be greater than 1000.
              "penalized segments" refer to segments that have a restrictions on maximum baseSpeed
            with `maxSpeedOnSegment`
              or avoided with `avoid[segments]`
            - In case the same segment is penalized multiple times through values provided in the
            query string and/or the POST body,
              then the most restrictive value will be applied.
        taxi (Taxi | Unset): Taxi-specific parameters
        traffic (Traffic | Unset): Traffic specific parameters.
        billing_tag (str | Unset):  Example: ABCD+EFGH.
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthErrorResponseSchema | AuthErrorResponseSchema | NotAllowed | IsolineErrorResponse | IsolineResponse | ServerInternal
    """

    return (
        await asyncio_detailed(
            client=client,
            range_=range_,
            transport_mode=transport_mode,
            origin=origin,
            departure_time=departure_time,
            destination=destination,
            arrival_time=arrival_time,
            routing_mode=routing_mode,
            shape=shape,
            optimize_for=optimize_for,
            avoid=avoid,
            exclude=exclude,
            allow=allow,
            truck=truck,
            vehicle=vehicle,
            consumption_model=consumption_model,
            ev=ev,
            fuel=fuel,
            max_speed_on_segment=max_speed_on_segment,
            taxi=taxi,
            traffic=traffic,
            billing_tag=billing_tag,
            x_request_id=x_request_id,
        )
    ).parsed
