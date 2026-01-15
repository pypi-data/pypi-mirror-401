from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v1_routes_create_routing_mode import V1RoutesCreateRoutingMode
from ...models.v1_routes_create_transport_mode import V1RoutesCreateTransportMode
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    arrival_time: Union[Unset, str] = UNSET,
    departure_time: Union[Unset, str] = UNSET,
    destination: str,
    origin: str,
    return_: Union[Unset, str] = UNSET,
    routing_mode: Union[
        Unset, V1RoutesCreateRoutingMode
    ] = V1RoutesCreateRoutingMode.FAST,
    transport_mode: V1RoutesCreateTransportMode,
    via: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["arrivalTime"] = arrival_time

    params["departureTime"] = departure_time

    params["destination"] = destination

    params["origin"] = origin

    params["return"] = return_

    json_routing_mode: Union[Unset, str] = UNSET
    if not isinstance(routing_mode, Unset):
        json_routing_mode = routing_mode.value

    params["routingMode"] = json_routing_mode

    json_transport_mode = transport_mode.value
    params["transportMode"] = json_transport_mode

    params["via"] = via

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/routes",
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
    arrival_time: Union[Unset, str] = UNSET,
    departure_time: Union[Unset, str] = UNSET,
    destination: str,
    origin: str,
    return_: Union[Unset, str] = UNSET,
    routing_mode: Union[
        Unset, V1RoutesCreateRoutingMode
    ] = V1RoutesCreateRoutingMode.FAST,
    transport_mode: V1RoutesCreateTransportMode,
    via: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Routes

    Args:
        arrival_time (Union[Unset, str]):
        departure_time (Union[Unset, str]):
        destination (str):
        origin (str):
        return_ (Union[Unset, str]):
        routing_mode (Union[Unset, V1RoutesCreateRoutingMode]):  Default:
            V1RoutesCreateRoutingMode.FAST.
        transport_mode (V1RoutesCreateTransportMode):
        via (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        arrival_time=arrival_time,
        departure_time=departure_time,
        destination=destination,
        origin=origin,
        return_=return_,
        routing_mode=routing_mode,
        transport_mode=transport_mode,
        via=via,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    arrival_time: Union[Unset, str] = UNSET,
    departure_time: Union[Unset, str] = UNSET,
    destination: str,
    origin: str,
    return_: Union[Unset, str] = UNSET,
    routing_mode: Union[
        Unset, V1RoutesCreateRoutingMode
    ] = V1RoutesCreateRoutingMode.FAST,
    transport_mode: V1RoutesCreateTransportMode,
    via: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Routes

    Args:
        arrival_time (Union[Unset, str]):
        departure_time (Union[Unset, str]):
        destination (str):
        origin (str):
        return_ (Union[Unset, str]):
        routing_mode (Union[Unset, V1RoutesCreateRoutingMode]):  Default:
            V1RoutesCreateRoutingMode.FAST.
        transport_mode (V1RoutesCreateTransportMode):
        via (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        arrival_time=arrival_time,
        departure_time=departure_time,
        destination=destination,
        origin=origin,
        return_=return_,
        routing_mode=routing_mode,
        transport_mode=transport_mode,
        via=via,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
