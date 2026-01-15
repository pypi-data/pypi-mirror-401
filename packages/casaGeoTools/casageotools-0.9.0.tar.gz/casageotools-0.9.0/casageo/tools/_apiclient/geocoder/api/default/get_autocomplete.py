from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_autocomplete_postal_code_mode import GetAutocompletePostalCodeMode
from ...models.get_autocomplete_show_item import GetAutocompleteShowItem
from ...models.get_autocomplete_types_item import GetAutocompleteTypesItem
from ...models.open_search_autocomplete_response import OpenSearchAutocompleteResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: str,
    at: str | Unset = UNSET,
    in_: str | Unset = UNSET,
    postal_code_mode: GetAutocompletePostalCodeMode | Unset = UNSET,
    types: list[GetAutocompleteTypesItem] | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 5,
    political_view: str | Unset = UNSET,
    show: list[GetAutocompleteShowItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_request_id, Unset):
        headers["X-Request-ID"] = x_request_id

    params: dict[str, Any] = {}

    params["q"] = q

    params["at"] = at

    params["in"] = in_

    json_postal_code_mode: str | Unset = UNSET
    if not isinstance(postal_code_mode, Unset):
        json_postal_code_mode = postal_code_mode.value

    params["postalCodeMode"] = json_postal_code_mode

    json_types: list[str] | Unset = UNSET
    if not isinstance(types, Unset):
        json_types = []
        for types_item_data in types:
            types_item = types_item_data.value
            json_types.append(types_item)

    params["types"] = json_types

    json_lang: list[str] | Unset = UNSET
    if not isinstance(lang, Unset):
        json_lang = lang

    params["lang"] = json_lang

    params["limit"] = limit

    params["politicalView"] = political_view

    json_show: list[str] | Unset = UNSET
    if not isinstance(show, Unset):
        json_show = []
        for show_item_data in show:
            show_item = show_item_data.value
            json_show.append(show_item)

    params["show"] = json_show

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/autocomplete",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | OpenSearchAutocompleteResponse | None:
    if response.status_code == 200:
        response_200 = OpenSearchAutocompleteResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 405:
        response_405 = ErrorResponse.from_dict(response.json())

        return response_405

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if response.status_code == 503:
        response_503 = ErrorResponse.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | OpenSearchAutocompleteResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    q: str,
    at: str | Unset = UNSET,
    in_: str | Unset = UNSET,
    postal_code_mode: GetAutocompletePostalCodeMode | Unset = UNSET,
    types: list[GetAutocompleteTypesItem] | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 5,
    political_view: str | Unset = UNSET,
    show: list[GetAutocompleteShowItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[ErrorResponse | OpenSearchAutocompleteResponse]:
    """Autocomplete

     This endpoint completes entered keystrokes to a valid street address or
    administrative area to speed-up entering address queries.

    Args:
        q (str):  Example: Berlin Pariser 20.
        at (str | Unset):
        in_ (str | Unset):
        postal_code_mode (GetAutocompletePostalCodeMode | Unset):
        types (list[GetAutocompleteTypesItem] | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 5.
        political_view (str | Unset):
        show (list[GetAutocompleteShowItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OpenSearchAutocompleteResponse]
    """

    kwargs = _get_kwargs(
        q=q,
        at=at,
        in_=in_,
        postal_code_mode=postal_code_mode,
        types=types,
        lang=lang,
        limit=limit,
        political_view=political_view,
        show=show,
        x_request_id=x_request_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    q: str,
    at: str | Unset = UNSET,
    in_: str | Unset = UNSET,
    postal_code_mode: GetAutocompletePostalCodeMode | Unset = UNSET,
    types: list[GetAutocompleteTypesItem] | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 5,
    political_view: str | Unset = UNSET,
    show: list[GetAutocompleteShowItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> ErrorResponse | OpenSearchAutocompleteResponse | None:
    """Autocomplete

     This endpoint completes entered keystrokes to a valid street address or
    administrative area to speed-up entering address queries.

    Args:
        q (str):  Example: Berlin Pariser 20.
        at (str | Unset):
        in_ (str | Unset):
        postal_code_mode (GetAutocompletePostalCodeMode | Unset):
        types (list[GetAutocompleteTypesItem] | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 5.
        political_view (str | Unset):
        show (list[GetAutocompleteShowItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OpenSearchAutocompleteResponse
    """

    return sync_detailed(
        client=client,
        q=q,
        at=at,
        in_=in_,
        postal_code_mode=postal_code_mode,
        types=types,
        lang=lang,
        limit=limit,
        political_view=political_view,
        show=show,
        x_request_id=x_request_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    q: str,
    at: str | Unset = UNSET,
    in_: str | Unset = UNSET,
    postal_code_mode: GetAutocompletePostalCodeMode | Unset = UNSET,
    types: list[GetAutocompleteTypesItem] | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 5,
    political_view: str | Unset = UNSET,
    show: list[GetAutocompleteShowItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[ErrorResponse | OpenSearchAutocompleteResponse]:
    """Autocomplete

     This endpoint completes entered keystrokes to a valid street address or
    administrative area to speed-up entering address queries.

    Args:
        q (str):  Example: Berlin Pariser 20.
        at (str | Unset):
        in_ (str | Unset):
        postal_code_mode (GetAutocompletePostalCodeMode | Unset):
        types (list[GetAutocompleteTypesItem] | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 5.
        political_view (str | Unset):
        show (list[GetAutocompleteShowItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OpenSearchAutocompleteResponse]
    """

    kwargs = _get_kwargs(
        q=q,
        at=at,
        in_=in_,
        postal_code_mode=postal_code_mode,
        types=types,
        lang=lang,
        limit=limit,
        political_view=political_view,
        show=show,
        x_request_id=x_request_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    q: str,
    at: str | Unset = UNSET,
    in_: str | Unset = UNSET,
    postal_code_mode: GetAutocompletePostalCodeMode | Unset = UNSET,
    types: list[GetAutocompleteTypesItem] | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 5,
    political_view: str | Unset = UNSET,
    show: list[GetAutocompleteShowItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> ErrorResponse | OpenSearchAutocompleteResponse | None:
    """Autocomplete

     This endpoint completes entered keystrokes to a valid street address or
    administrative area to speed-up entering address queries.

    Args:
        q (str):  Example: Berlin Pariser 20.
        at (str | Unset):
        in_ (str | Unset):
        postal_code_mode (GetAutocompletePostalCodeMode | Unset):
        types (list[GetAutocompleteTypesItem] | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 5.
        political_view (str | Unset):
        show (list[GetAutocompleteShowItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OpenSearchAutocompleteResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            q=q,
            at=at,
            in_=in_,
            postal_code_mode=postal_code_mode,
            types=types,
            lang=lang,
            limit=limit,
            political_view=political_view,
            show=show,
            x_request_id=x_request_id,
        )
    ).parsed
