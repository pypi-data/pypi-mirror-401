from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.allow import Allow
from ...models.auth_error_response_schema import AuthErrorResponseSchema
from ...models.avoid import Avoid
from ...models.ev_empirical_model import EVEmpiricalModel
from ...models.ev_physical_model import EVPhysicalModel
from ...models.exclude import Exclude
from ...models.fuel import Fuel
from ...models.match_trace import MatchTrace
from ...models.return_ import Return
from ...models.router_mode import RouterMode
from ...models.router_route_response import RouterRouteResponse
from ...models.routing_error_response import RoutingErrorResponse
from ...models.scooter import Scooter
from ...models.spans import Spans
from ...models.taxi import Taxi
from ...models.truck import Truck
from ...models.units import Units
from ...models.vehicle import Vehicle
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: MatchTrace | Unset = UNSET,
    transport_mode: RouterMode,
    departure_time: str | Unset = UNSET,
    avoid: Avoid | Unset = UNSET,
    allow: Allow | Unset = UNSET,
    exclude: Exclude | Unset = UNSET,
    units: Units | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    return_: list[Return] | Unset = UNSET,
    spans: list[Spans] | Unset = UNSET,
    truck: Truck | Unset = UNSET,
    vehicle: Vehicle | Unset = UNSET,
    consumption_model: str | Unset = UNSET,
    ev: EVEmpiricalModel | EVPhysicalModel | Unset = UNSET,
    fuel: Fuel | Unset = UNSET,
    scooter: Scooter | Unset = UNSET,
    taxi: Taxi | Unset = UNSET,
    billing_tag: str | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_request_id, Unset):
        headers["X-Request-ID"] = x_request_id

    params: dict[str, Any] = {}

    json_transport_mode = transport_mode.value
    params["transportMode"] = json_transport_mode

    params["departureTime"] = departure_time

    json_avoid: dict[str, Any] | Unset = UNSET
    if not isinstance(avoid, Unset):
        json_avoid = avoid.to_dict()
    if not isinstance(json_avoid, Unset):
        params.update((f"avoid[{k}]", v) for k, v in json_avoid.items())

    json_allow: dict[str, Any] | Unset = UNSET
    if not isinstance(allow, Unset):
        json_allow = allow.to_dict()
    if not isinstance(json_allow, Unset):
        params.update((f"allow[{k}]", v) for k, v in json_allow.items())

    json_exclude: dict[str, Any] | Unset = UNSET
    if not isinstance(exclude, Unset):
        json_exclude = exclude.to_dict()
    if not isinstance(json_exclude, Unset):
        params.update((f"exclude[{k}]", v) for k, v in json_exclude.items())

    json_units: str | Unset = UNSET
    if not isinstance(units, Unset):
        json_units = units.value

    params["units"] = json_units

    json_lang: list[str] | Unset = UNSET
    if not isinstance(lang, Unset):
        json_lang = lang

    params["lang"] = json_lang

    json_return_: list[str] | Unset = UNSET
    if not isinstance(return_, Unset):
        json_return_ = []
        for return_item_data in return_:
            return_item = return_item_data.value
            json_return_.append(return_item)

    params["return"] = json_return_

    json_spans: list[str] | Unset = UNSET
    if not isinstance(spans, Unset):
        json_spans = []
        for spans_item_data in spans:
            spans_item = spans_item_data.value
            json_spans.append(spans_item)

    params["spans"] = json_spans

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
    elif isinstance(ev, EVEmpiricalModel):
        json_ev = ev.to_dict()
    else:
        json_ev = ev.to_dict()

    params["ev"] = json_ev

    json_fuel: dict[str, Any] | Unset = UNSET
    if not isinstance(fuel, Unset):
        json_fuel = fuel.to_dict()
    if not isinstance(json_fuel, Unset):
        params.update((f"fuel[{k}]", v) for k, v in json_fuel.items())

    json_scooter: dict[str, Any] | Unset = UNSET
    if not isinstance(scooter, Unset):
        json_scooter = scooter.to_dict()
    if not isinstance(json_scooter, Unset):
        params.update((f"scooter[{k}]", v) for k, v in json_scooter.items())

    json_taxi: dict[str, Any] | Unset = UNSET
    if not isinstance(taxi, Unset):
        json_taxi = taxi.to_dict()
    if not isinstance(json_taxi, Unset):
        params.update((f"taxi[{k}]", v) for k, v in json_taxi.items())

    params["billingTag"] = billing_tag

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/import",
        "params": params,
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    AuthErrorResponseSchema
    | AuthErrorResponseSchema
    | RoutingErrorResponse
    | RouterRouteResponse
    | RoutingErrorResponse
    | None
):
    if response.status_code == 200:
        response_200 = RouterRouteResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = RoutingErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = AuthErrorResponseSchema.from_dict(response.json())

        return response_401

    if response.status_code == 403:

        def _parse_response_403(
            data: object,
        ) -> AuthErrorResponseSchema | RoutingErrorResponse:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_routing_403_error_response_schema_type_0 = (
                    AuthErrorResponseSchema.from_dict(data)
                )

                return componentsschemas_routing_403_error_response_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_routing_403_error_response_schema_type_1 = (
                RoutingErrorResponse.from_dict(data)
            )

            return componentsschemas_routing_403_error_response_schema_type_1

        response_403 = _parse_response_403(response.json())

        return response_403

    if response.status_code == 500:
        response_500 = RoutingErrorResponse.from_dict(response.json())

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
    | RoutingErrorResponse
    | RouterRouteResponse
    | RoutingErrorResponse
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
    body: MatchTrace | Unset = UNSET,
    transport_mode: RouterMode,
    departure_time: str | Unset = UNSET,
    avoid: Avoid | Unset = UNSET,
    allow: Allow | Unset = UNSET,
    exclude: Exclude | Unset = UNSET,
    units: Units | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    return_: list[Return] | Unset = UNSET,
    spans: list[Spans] | Unset = UNSET,
    truck: Truck | Unset = UNSET,
    vehicle: Vehicle | Unset = UNSET,
    consumption_model: str | Unset = UNSET,
    ev: EVEmpiricalModel | EVPhysicalModel | Unset = UNSET,
    fuel: Fuel | Unset = UNSET,
    scooter: Scooter | Unset = UNSET,
    taxi: Taxi | Unset = UNSET,
    billing_tag: str | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[
    AuthErrorResponseSchema
    | AuthErrorResponseSchema
    | RoutingErrorResponse
    | RouterRouteResponse
    | RoutingErrorResponse
]:
    """Calculate a route from a sequence of trace points

     Creates a route from a sequence of trace points.

    Post body size limit is 10MiB.

    For best results, use 1Hz GPS data or any points that have a spacing of a few meters between them.
    For traces with less frequent points, the Route Import service will attempt to create an approximate
    reconstruction.
    In some situations, when consecutive points are too far apart (more than about 30 kilometers of on-
    road distance), they could be considered unreachable and one of them could fail to be matched.

    Args:
        transport_mode (RouterMode): Mode of transport to be used for route calculation.
        departure_time (str | Unset): Specifies the time either as

            * "**RFC 3339**, section 5.6 as defined by either `date-time` or `date-only` 'T'
            `partial-time` (ie no time-offset)", or
            * the special value `any` which stand for unspecified time
        avoid (Avoid | Unset):
        allow (Allow | Unset): Explicitly allow features that require users to opt in.
        exclude (Exclude | Unset): Options to exclude strictly during the route calculation.
        units (Units | Unset): Units of measurement used, for example, in guidance instructions.
            The default is `metric`.
        lang (list[str] | Unset):
        return_ (list[Return] | Unset):
        spans (list[Spans] | Unset):
        truck (Truck | Unset): Vehicle-specific parameters
        vehicle (Vehicle | Unset): Vehicle-specific parameters
        consumption_model (str | Unset): Extensible enum: `empirical` `physical` `...`
            Specifies which of the EV consumption models is being used. See the `ev` parameter for
            details on the models.

            * `empirical`
            * `physical`

            **Alpha**: Physical consumption model is in development. It may not be stable and is
            subject to change.
        ev (EVEmpiricalModel | EVPhysicalModel | Unset): EV properties to be used for calculating
            consumption.

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

            The following `ev` properties are additionally required in order to calculate State-of-
            Charge along the route:
            * `initialCharge`
            * `maxCharge`

            Route reachability based on State-of-Charge will be evaluated for the following
            constraints, if additionally provided,
            * `minChargeAtDestination`
            * `minChargeAtFirstChargingStation`
            * `minChargeAtChargingStation`

            The following properties are additionally required in order to calculate charging at
            charging station waypoints (see documentation for `via` parameter)
            * `chargingCurve`

            **Notes**:
            * Hybrid vehicles (EV + Other fuel types) are not supported. Consumption properties are
            not supported for combination of `ev` and `fuel` vehicles.
            * EV parameters are not supported in combination with pedestrian and bicycle
            `transportMode`.
        fuel (Fuel | Unset): **Disclaimer: This parameter is currently in beta release, and is
            therefore subject to breaking changes.**

            Fuel parameters to be used for calculating consumption and related CO2 emission, and toll
            calculation.

            The following attributes are required for calculating consumption:
              * `type`
              * `freeFlowSpeedTable`

            The following attribute is needed for fuel specific toll calculation (if not provided
            default toll instead of fuel specific toll will be returned):
              * `type`

            **Notes**:
            * Hybrid vehicles (EV + Other fuel types) are not supported. Consumption properties are
            not supported for combination of `ev` and `fuel` vehicles.
            * Fuel parameters are not supported in combination with pedestrian and bicycle
            `transportMode`.
        scooter (Scooter | Unset): Scooter-specific parameters
        taxi (Taxi | Unset): Taxi-specific parameters
        billing_tag (str | Unset):  Example: ABCD+EFGH.
        x_request_id (str | Unset):
        body (MatchTrace | Unset): Trace file with points and path match parameters Example:
            {'trace': [{'lat': 52.0, 'lng': 13.1}, {'lat': 52.1, 'lng': 13.2}, {'lat': 52.2, 'lng':
            13.3}], 'via': [{'index': 1}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthErrorResponseSchema | AuthErrorResponseSchema | RoutingErrorResponse | RouterRouteResponse | RoutingErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        transport_mode=transport_mode,
        departure_time=departure_time,
        avoid=avoid,
        allow=allow,
        exclude=exclude,
        units=units,
        lang=lang,
        return_=return_,
        spans=spans,
        truck=truck,
        vehicle=vehicle,
        consumption_model=consumption_model,
        ev=ev,
        fuel=fuel,
        scooter=scooter,
        taxi=taxi,
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
    body: MatchTrace | Unset = UNSET,
    transport_mode: RouterMode,
    departure_time: str | Unset = UNSET,
    avoid: Avoid | Unset = UNSET,
    allow: Allow | Unset = UNSET,
    exclude: Exclude | Unset = UNSET,
    units: Units | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    return_: list[Return] | Unset = UNSET,
    spans: list[Spans] | Unset = UNSET,
    truck: Truck | Unset = UNSET,
    vehicle: Vehicle | Unset = UNSET,
    consumption_model: str | Unset = UNSET,
    ev: EVEmpiricalModel | EVPhysicalModel | Unset = UNSET,
    fuel: Fuel | Unset = UNSET,
    scooter: Scooter | Unset = UNSET,
    taxi: Taxi | Unset = UNSET,
    billing_tag: str | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> (
    AuthErrorResponseSchema
    | AuthErrorResponseSchema
    | RoutingErrorResponse
    | RouterRouteResponse
    | RoutingErrorResponse
    | None
):
    """Calculate a route from a sequence of trace points

     Creates a route from a sequence of trace points.

    Post body size limit is 10MiB.

    For best results, use 1Hz GPS data or any points that have a spacing of a few meters between them.
    For traces with less frequent points, the Route Import service will attempt to create an approximate
    reconstruction.
    In some situations, when consecutive points are too far apart (more than about 30 kilometers of on-
    road distance), they could be considered unreachable and one of them could fail to be matched.

    Args:
        transport_mode (RouterMode): Mode of transport to be used for route calculation.
        departure_time (str | Unset): Specifies the time either as

            * "**RFC 3339**, section 5.6 as defined by either `date-time` or `date-only` 'T'
            `partial-time` (ie no time-offset)", or
            * the special value `any` which stand for unspecified time
        avoid (Avoid | Unset):
        allow (Allow | Unset): Explicitly allow features that require users to opt in.
        exclude (Exclude | Unset): Options to exclude strictly during the route calculation.
        units (Units | Unset): Units of measurement used, for example, in guidance instructions.
            The default is `metric`.
        lang (list[str] | Unset):
        return_ (list[Return] | Unset):
        spans (list[Spans] | Unset):
        truck (Truck | Unset): Vehicle-specific parameters
        vehicle (Vehicle | Unset): Vehicle-specific parameters
        consumption_model (str | Unset): Extensible enum: `empirical` `physical` `...`
            Specifies which of the EV consumption models is being used. See the `ev` parameter for
            details on the models.

            * `empirical`
            * `physical`

            **Alpha**: Physical consumption model is in development. It may not be stable and is
            subject to change.
        ev (EVEmpiricalModel | EVPhysicalModel | Unset): EV properties to be used for calculating
            consumption.

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

            The following `ev` properties are additionally required in order to calculate State-of-
            Charge along the route:
            * `initialCharge`
            * `maxCharge`

            Route reachability based on State-of-Charge will be evaluated for the following
            constraints, if additionally provided,
            * `minChargeAtDestination`
            * `minChargeAtFirstChargingStation`
            * `minChargeAtChargingStation`

            The following properties are additionally required in order to calculate charging at
            charging station waypoints (see documentation for `via` parameter)
            * `chargingCurve`

            **Notes**:
            * Hybrid vehicles (EV + Other fuel types) are not supported. Consumption properties are
            not supported for combination of `ev` and `fuel` vehicles.
            * EV parameters are not supported in combination with pedestrian and bicycle
            `transportMode`.
        fuel (Fuel | Unset): **Disclaimer: This parameter is currently in beta release, and is
            therefore subject to breaking changes.**

            Fuel parameters to be used for calculating consumption and related CO2 emission, and toll
            calculation.

            The following attributes are required for calculating consumption:
              * `type`
              * `freeFlowSpeedTable`

            The following attribute is needed for fuel specific toll calculation (if not provided
            default toll instead of fuel specific toll will be returned):
              * `type`

            **Notes**:
            * Hybrid vehicles (EV + Other fuel types) are not supported. Consumption properties are
            not supported for combination of `ev` and `fuel` vehicles.
            * Fuel parameters are not supported in combination with pedestrian and bicycle
            `transportMode`.
        scooter (Scooter | Unset): Scooter-specific parameters
        taxi (Taxi | Unset): Taxi-specific parameters
        billing_tag (str | Unset):  Example: ABCD+EFGH.
        x_request_id (str | Unset):
        body (MatchTrace | Unset): Trace file with points and path match parameters Example:
            {'trace': [{'lat': 52.0, 'lng': 13.1}, {'lat': 52.1, 'lng': 13.2}, {'lat': 52.2, 'lng':
            13.3}], 'via': [{'index': 1}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthErrorResponseSchema | AuthErrorResponseSchema | RoutingErrorResponse | RouterRouteResponse | RoutingErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        transport_mode=transport_mode,
        departure_time=departure_time,
        avoid=avoid,
        allow=allow,
        exclude=exclude,
        units=units,
        lang=lang,
        return_=return_,
        spans=spans,
        truck=truck,
        vehicle=vehicle,
        consumption_model=consumption_model,
        ev=ev,
        fuel=fuel,
        scooter=scooter,
        taxi=taxi,
        billing_tag=billing_tag,
        x_request_id=x_request_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: MatchTrace | Unset = UNSET,
    transport_mode: RouterMode,
    departure_time: str | Unset = UNSET,
    avoid: Avoid | Unset = UNSET,
    allow: Allow | Unset = UNSET,
    exclude: Exclude | Unset = UNSET,
    units: Units | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    return_: list[Return] | Unset = UNSET,
    spans: list[Spans] | Unset = UNSET,
    truck: Truck | Unset = UNSET,
    vehicle: Vehicle | Unset = UNSET,
    consumption_model: str | Unset = UNSET,
    ev: EVEmpiricalModel | EVPhysicalModel | Unset = UNSET,
    fuel: Fuel | Unset = UNSET,
    scooter: Scooter | Unset = UNSET,
    taxi: Taxi | Unset = UNSET,
    billing_tag: str | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[
    AuthErrorResponseSchema
    | AuthErrorResponseSchema
    | RoutingErrorResponse
    | RouterRouteResponse
    | RoutingErrorResponse
]:
    """Calculate a route from a sequence of trace points

     Creates a route from a sequence of trace points.

    Post body size limit is 10MiB.

    For best results, use 1Hz GPS data or any points that have a spacing of a few meters between them.
    For traces with less frequent points, the Route Import service will attempt to create an approximate
    reconstruction.
    In some situations, when consecutive points are too far apart (more than about 30 kilometers of on-
    road distance), they could be considered unreachable and one of them could fail to be matched.

    Args:
        transport_mode (RouterMode): Mode of transport to be used for route calculation.
        departure_time (str | Unset): Specifies the time either as

            * "**RFC 3339**, section 5.6 as defined by either `date-time` or `date-only` 'T'
            `partial-time` (ie no time-offset)", or
            * the special value `any` which stand for unspecified time
        avoid (Avoid | Unset):
        allow (Allow | Unset): Explicitly allow features that require users to opt in.
        exclude (Exclude | Unset): Options to exclude strictly during the route calculation.
        units (Units | Unset): Units of measurement used, for example, in guidance instructions.
            The default is `metric`.
        lang (list[str] | Unset):
        return_ (list[Return] | Unset):
        spans (list[Spans] | Unset):
        truck (Truck | Unset): Vehicle-specific parameters
        vehicle (Vehicle | Unset): Vehicle-specific parameters
        consumption_model (str | Unset): Extensible enum: `empirical` `physical` `...`
            Specifies which of the EV consumption models is being used. See the `ev` parameter for
            details on the models.

            * `empirical`
            * `physical`

            **Alpha**: Physical consumption model is in development. It may not be stable and is
            subject to change.
        ev (EVEmpiricalModel | EVPhysicalModel | Unset): EV properties to be used for calculating
            consumption.

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

            The following `ev` properties are additionally required in order to calculate State-of-
            Charge along the route:
            * `initialCharge`
            * `maxCharge`

            Route reachability based on State-of-Charge will be evaluated for the following
            constraints, if additionally provided,
            * `minChargeAtDestination`
            * `minChargeAtFirstChargingStation`
            * `minChargeAtChargingStation`

            The following properties are additionally required in order to calculate charging at
            charging station waypoints (see documentation for `via` parameter)
            * `chargingCurve`

            **Notes**:
            * Hybrid vehicles (EV + Other fuel types) are not supported. Consumption properties are
            not supported for combination of `ev` and `fuel` vehicles.
            * EV parameters are not supported in combination with pedestrian and bicycle
            `transportMode`.
        fuel (Fuel | Unset): **Disclaimer: This parameter is currently in beta release, and is
            therefore subject to breaking changes.**

            Fuel parameters to be used for calculating consumption and related CO2 emission, and toll
            calculation.

            The following attributes are required for calculating consumption:
              * `type`
              * `freeFlowSpeedTable`

            The following attribute is needed for fuel specific toll calculation (if not provided
            default toll instead of fuel specific toll will be returned):
              * `type`

            **Notes**:
            * Hybrid vehicles (EV + Other fuel types) are not supported. Consumption properties are
            not supported for combination of `ev` and `fuel` vehicles.
            * Fuel parameters are not supported in combination with pedestrian and bicycle
            `transportMode`.
        scooter (Scooter | Unset): Scooter-specific parameters
        taxi (Taxi | Unset): Taxi-specific parameters
        billing_tag (str | Unset):  Example: ABCD+EFGH.
        x_request_id (str | Unset):
        body (MatchTrace | Unset): Trace file with points and path match parameters Example:
            {'trace': [{'lat': 52.0, 'lng': 13.1}, {'lat': 52.1, 'lng': 13.2}, {'lat': 52.2, 'lng':
            13.3}], 'via': [{'index': 1}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthErrorResponseSchema | AuthErrorResponseSchema | RoutingErrorResponse | RouterRouteResponse | RoutingErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        transport_mode=transport_mode,
        departure_time=departure_time,
        avoid=avoid,
        allow=allow,
        exclude=exclude,
        units=units,
        lang=lang,
        return_=return_,
        spans=spans,
        truck=truck,
        vehicle=vehicle,
        consumption_model=consumption_model,
        ev=ev,
        fuel=fuel,
        scooter=scooter,
        taxi=taxi,
        billing_tag=billing_tag,
        x_request_id=x_request_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: MatchTrace | Unset = UNSET,
    transport_mode: RouterMode,
    departure_time: str | Unset = UNSET,
    avoid: Avoid | Unset = UNSET,
    allow: Allow | Unset = UNSET,
    exclude: Exclude | Unset = UNSET,
    units: Units | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    return_: list[Return] | Unset = UNSET,
    spans: list[Spans] | Unset = UNSET,
    truck: Truck | Unset = UNSET,
    vehicle: Vehicle | Unset = UNSET,
    consumption_model: str | Unset = UNSET,
    ev: EVEmpiricalModel | EVPhysicalModel | Unset = UNSET,
    fuel: Fuel | Unset = UNSET,
    scooter: Scooter | Unset = UNSET,
    taxi: Taxi | Unset = UNSET,
    billing_tag: str | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> (
    AuthErrorResponseSchema
    | AuthErrorResponseSchema
    | RoutingErrorResponse
    | RouterRouteResponse
    | RoutingErrorResponse
    | None
):
    """Calculate a route from a sequence of trace points

     Creates a route from a sequence of trace points.

    Post body size limit is 10MiB.

    For best results, use 1Hz GPS data or any points that have a spacing of a few meters between them.
    For traces with less frequent points, the Route Import service will attempt to create an approximate
    reconstruction.
    In some situations, when consecutive points are too far apart (more than about 30 kilometers of on-
    road distance), they could be considered unreachable and one of them could fail to be matched.

    Args:
        transport_mode (RouterMode): Mode of transport to be used for route calculation.
        departure_time (str | Unset): Specifies the time either as

            * "**RFC 3339**, section 5.6 as defined by either `date-time` or `date-only` 'T'
            `partial-time` (ie no time-offset)", or
            * the special value `any` which stand for unspecified time
        avoid (Avoid | Unset):
        allow (Allow | Unset): Explicitly allow features that require users to opt in.
        exclude (Exclude | Unset): Options to exclude strictly during the route calculation.
        units (Units | Unset): Units of measurement used, for example, in guidance instructions.
            The default is `metric`.
        lang (list[str] | Unset):
        return_ (list[Return] | Unset):
        spans (list[Spans] | Unset):
        truck (Truck | Unset): Vehicle-specific parameters
        vehicle (Vehicle | Unset): Vehicle-specific parameters
        consumption_model (str | Unset): Extensible enum: `empirical` `physical` `...`
            Specifies which of the EV consumption models is being used. See the `ev` parameter for
            details on the models.

            * `empirical`
            * `physical`

            **Alpha**: Physical consumption model is in development. It may not be stable and is
            subject to change.
        ev (EVEmpiricalModel | EVPhysicalModel | Unset): EV properties to be used for calculating
            consumption.

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

            The following `ev` properties are additionally required in order to calculate State-of-
            Charge along the route:
            * `initialCharge`
            * `maxCharge`

            Route reachability based on State-of-Charge will be evaluated for the following
            constraints, if additionally provided,
            * `minChargeAtDestination`
            * `minChargeAtFirstChargingStation`
            * `minChargeAtChargingStation`

            The following properties are additionally required in order to calculate charging at
            charging station waypoints (see documentation for `via` parameter)
            * `chargingCurve`

            **Notes**:
            * Hybrid vehicles (EV + Other fuel types) are not supported. Consumption properties are
            not supported for combination of `ev` and `fuel` vehicles.
            * EV parameters are not supported in combination with pedestrian and bicycle
            `transportMode`.
        fuel (Fuel | Unset): **Disclaimer: This parameter is currently in beta release, and is
            therefore subject to breaking changes.**

            Fuel parameters to be used for calculating consumption and related CO2 emission, and toll
            calculation.

            The following attributes are required for calculating consumption:
              * `type`
              * `freeFlowSpeedTable`

            The following attribute is needed for fuel specific toll calculation (if not provided
            default toll instead of fuel specific toll will be returned):
              * `type`

            **Notes**:
            * Hybrid vehicles (EV + Other fuel types) are not supported. Consumption properties are
            not supported for combination of `ev` and `fuel` vehicles.
            * Fuel parameters are not supported in combination with pedestrian and bicycle
            `transportMode`.
        scooter (Scooter | Unset): Scooter-specific parameters
        taxi (Taxi | Unset): Taxi-specific parameters
        billing_tag (str | Unset):  Example: ABCD+EFGH.
        x_request_id (str | Unset):
        body (MatchTrace | Unset): Trace file with points and path match parameters Example:
            {'trace': [{'lat': 52.0, 'lng': 13.1}, {'lat': 52.1, 'lng': 13.2}, {'lat': 52.2, 'lng':
            13.3}], 'via': [{'index': 1}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthErrorResponseSchema | AuthErrorResponseSchema | RoutingErrorResponse | RouterRouteResponse | RoutingErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            transport_mode=transport_mode,
            departure_time=departure_time,
            avoid=avoid,
            allow=allow,
            exclude=exclude,
            units=units,
            lang=lang,
            return_=return_,
            spans=spans,
            truck=truck,
            vehicle=vehicle,
            consumption_model=consumption_model,
            ev=ev,
            fuel=fuel,
            scooter=scooter,
            taxi=taxi,
            billing_tag=billing_tag,
            x_request_id=x_request_id,
        )
    ).parsed
