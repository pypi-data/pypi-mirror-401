from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.health_response_fail_schema import HealthResponseFailSchema
from ...models.health_response_ok_schema import HealthResponseOKSchema
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    x_request_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_request_id, Unset):
        headers["X-Request-ID"] = x_request_id

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/health",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HealthResponseFailSchema | HealthResponseOKSchema:
    if response.status_code == 200:
        response_200 = HealthResponseOKSchema.from_dict(response.json())

        return response_200

    response_default = HealthResponseFailSchema.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HealthResponseFailSchema | HealthResponseOKSchema]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    x_request_id: str | Unset = UNSET,
) -> Response[HealthResponseFailSchema | HealthResponseOKSchema]:
    """Health status of the service

     Returns the health of the service

    Args:
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HealthResponseFailSchema | HealthResponseOKSchema]
    """

    kwargs = _get_kwargs(
        x_request_id=x_request_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    x_request_id: str | Unset = UNSET,
) -> HealthResponseFailSchema | HealthResponseOKSchema | None:
    """Health status of the service

     Returns the health of the service

    Args:
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HealthResponseFailSchema | HealthResponseOKSchema
    """

    return sync_detailed(
        client=client,
        x_request_id=x_request_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    x_request_id: str | Unset = UNSET,
) -> Response[HealthResponseFailSchema | HealthResponseOKSchema]:
    """Health status of the service

     Returns the health of the service

    Args:
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HealthResponseFailSchema | HealthResponseOKSchema]
    """

    kwargs = _get_kwargs(
        x_request_id=x_request_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    x_request_id: str | Unset = UNSET,
) -> HealthResponseFailSchema | HealthResponseOKSchema | None:
    """Health status of the service

     Returns the health of the service

    Args:
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HealthResponseFailSchema | HealthResponseOKSchema
    """

    return (
        await asyncio_detailed(
            client=client,
            x_request_id=x_request_id,
        )
    ).parsed
