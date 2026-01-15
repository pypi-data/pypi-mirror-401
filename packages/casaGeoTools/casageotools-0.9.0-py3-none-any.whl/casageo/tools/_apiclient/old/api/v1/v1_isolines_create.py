from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v1_isolines_create_optimize_for import V1IsolinesCreateOptimizeFor
from ...models.v1_isolines_create_rangetype import V1IsolinesCreateRangetype
from ...models.v1_isolines_create_routing_mode import V1IsolinesCreateRoutingMode
from ...models.v1_isolines_create_transport_mode import V1IsolinesCreateTransportMode
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    allow: Union[Unset, str] = UNSET,
    arrival_time: Union[Unset, str] = UNSET,
    avoid: Union[Unset, str] = UNSET,
    departure_time: Union[Unset, str] = UNSET,
    destination: Union[Unset, str] = UNSET,
    exclude: Union[Unset, str] = UNSET,
    optimize_for: Union[
        Unset, V1IsolinesCreateOptimizeFor
    ] = V1IsolinesCreateOptimizeFor.BALANCED,
    origin: Union[Unset, str] = UNSET,
    rangetype: Union[Unset, V1IsolinesCreateRangetype] = UNSET,
    rangevalues: Union[Unset, str] = UNSET,
    routing_mode: Union[Unset, V1IsolinesCreateRoutingMode] = UNSET,
    shapemax_points: Union[Unset, int] = UNSET,
    transport_mode: Union[Unset, V1IsolinesCreateTransportMode] = UNSET,
    vehicle: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["allow"] = allow

    params["arrivalTime"] = arrival_time

    params["avoid"] = avoid

    params["departureTime"] = departure_time

    params["destination"] = destination

    params["exclude"] = exclude

    json_optimize_for: Union[Unset, str] = UNSET
    if not isinstance(optimize_for, Unset):
        json_optimize_for = optimize_for.value

    params["optimizeFor"] = json_optimize_for

    params["origin"] = origin

    json_rangetype: Union[Unset, str] = UNSET
    if not isinstance(rangetype, Unset):
        json_rangetype = rangetype.value

    params["range[type]"] = json_rangetype

    params["range[values]"] = rangevalues

    json_routing_mode: Union[Unset, str] = UNSET
    if not isinstance(routing_mode, Unset):
        json_routing_mode = routing_mode.value

    params["routingMode"] = json_routing_mode

    params["shape[maxPoints]"] = shapemax_points

    json_transport_mode: Union[Unset, str] = UNSET
    if not isinstance(transport_mode, Unset):
        json_transport_mode = transport_mode.value

    params["transportMode"] = json_transport_mode

    params["vehicle"] = vehicle

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/isolines",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Any]:
    if response.status_code == 200:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    allow: Union[Unset, str] = UNSET,
    arrival_time: Union[Unset, str] = UNSET,
    avoid: Union[Unset, str] = UNSET,
    departure_time: Union[Unset, str] = UNSET,
    destination: Union[Unset, str] = UNSET,
    exclude: Union[Unset, str] = UNSET,
    optimize_for: Union[
        Unset, V1IsolinesCreateOptimizeFor
    ] = V1IsolinesCreateOptimizeFor.BALANCED,
    origin: Union[Unset, str] = UNSET,
    rangetype: Union[Unset, V1IsolinesCreateRangetype] = UNSET,
    rangevalues: Union[Unset, str] = UNSET,
    routing_mode: Union[Unset, V1IsolinesCreateRoutingMode] = UNSET,
    shapemax_points: Union[Unset, int] = UNSET,
    transport_mode: Union[Unset, V1IsolinesCreateTransportMode] = UNSET,
    vehicle: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Isolines

    Args:
        allow (Union[Unset, str]):
        arrival_time (Union[Unset, str]):
        avoid (Union[Unset, str]):
        departure_time (Union[Unset, str]):
        destination (Union[Unset, str]):
        exclude (Union[Unset, str]):
        optimize_for (Union[Unset, V1IsolinesCreateOptimizeFor]):  Default:
            V1IsolinesCreateOptimizeFor.BALANCED.
        origin (Union[Unset, str]):
        rangetype (Union[Unset, V1IsolinesCreateRangetype]):
        rangevalues (Union[Unset, str]):
        routing_mode (Union[Unset, V1IsolinesCreateRoutingMode]):
        shapemax_points (Union[Unset, int]):
        transport_mode (Union[Unset, V1IsolinesCreateTransportMode]):
        vehicle (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        allow=allow,
        arrival_time=arrival_time,
        avoid=avoid,
        departure_time=departure_time,
        destination=destination,
        exclude=exclude,
        optimize_for=optimize_for,
        origin=origin,
        rangetype=rangetype,
        rangevalues=rangevalues,
        routing_mode=routing_mode,
        shapemax_points=shapemax_points,
        transport_mode=transport_mode,
        vehicle=vehicle,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    allow: Union[Unset, str] = UNSET,
    arrival_time: Union[Unset, str] = UNSET,
    avoid: Union[Unset, str] = UNSET,
    departure_time: Union[Unset, str] = UNSET,
    destination: Union[Unset, str] = UNSET,
    exclude: Union[Unset, str] = UNSET,
    optimize_for: Union[
        Unset, V1IsolinesCreateOptimizeFor
    ] = V1IsolinesCreateOptimizeFor.BALANCED,
    origin: Union[Unset, str] = UNSET,
    rangetype: Union[Unset, V1IsolinesCreateRangetype] = UNSET,
    rangevalues: Union[Unset, str] = UNSET,
    routing_mode: Union[Unset, V1IsolinesCreateRoutingMode] = UNSET,
    shapemax_points: Union[Unset, int] = UNSET,
    transport_mode: Union[Unset, V1IsolinesCreateTransportMode] = UNSET,
    vehicle: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Isolines

    Args:
        allow (Union[Unset, str]):
        arrival_time (Union[Unset, str]):
        avoid (Union[Unset, str]):
        departure_time (Union[Unset, str]):
        destination (Union[Unset, str]):
        exclude (Union[Unset, str]):
        optimize_for (Union[Unset, V1IsolinesCreateOptimizeFor]):  Default:
            V1IsolinesCreateOptimizeFor.BALANCED.
        origin (Union[Unset, str]):
        rangetype (Union[Unset, V1IsolinesCreateRangetype]):
        rangevalues (Union[Unset, str]):
        routing_mode (Union[Unset, V1IsolinesCreateRoutingMode]):
        shapemax_points (Union[Unset, int]):
        transport_mode (Union[Unset, V1IsolinesCreateTransportMode]):
        vehicle (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        allow=allow,
        arrival_time=arrival_time,
        avoid=avoid,
        departure_time=departure_time,
        destination=destination,
        exclude=exclude,
        optimize_for=optimize_for,
        origin=origin,
        rangetype=rangetype,
        rangevalues=rangevalues,
        routing_mode=routing_mode,
        shapemax_points=shapemax_points,
        transport_mode=transport_mode,
        vehicle=vehicle,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
