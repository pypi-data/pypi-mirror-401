from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_revgeocode_show_item import GetRevgeocodeShowItem
from ...models.get_revgeocode_show_map_references_item import (
    GetRevgeocodeShowMapReferencesItem,
)
from ...models.get_revgeocode_show_nav_attributes_item import (
    GetRevgeocodeShowNavAttributesItem,
)
from ...models.get_revgeocode_show_related_item import GetRevgeocodeShowRelatedItem
from ...models.get_revgeocode_types_item import GetRevgeocodeTypesItem
from ...models.get_revgeocode_with_item import GetRevgeocodeWithItem
from ...models.open_search_reverse_geocode_response import (
    OpenSearchReverseGeocodeResponse,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    at: str | Unset = UNSET,
    bearing: int | Unset = UNSET,
    in_: str | Unset = UNSET,
    types: list[GetRevgeocodeTypesItem] | Unset = UNSET,
    with_: list[GetRevgeocodeWithItem] | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 1,
    political_view: str | Unset = UNSET,
    show_map_references: list[GetRevgeocodeShowMapReferencesItem] | Unset = UNSET,
    show: list[GetRevgeocodeShowItem] | Unset = UNSET,
    show_nav_attributes: list[GetRevgeocodeShowNavAttributesItem] | Unset = UNSET,
    show_related: list[GetRevgeocodeShowRelatedItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_request_id, Unset):
        headers["X-Request-ID"] = x_request_id

    params: dict[str, Any] = {}

    params["at"] = at

    params["bearing"] = bearing

    params["in"] = in_

    json_types: list[str] | Unset = UNSET
    if not isinstance(types, Unset):
        json_types = []
        for types_item_data in types:
            types_item = types_item_data.value
            json_types.append(types_item)

    params["types"] = json_types

    json_with_: list[str] | Unset = UNSET
    if not isinstance(with_, Unset):
        json_with_ = []
        for with_item_data in with_:
            with_item = with_item_data.value
            json_with_.append(with_item)

    params["with"] = json_with_

    json_lang: list[str] | Unset = UNSET
    if not isinstance(lang, Unset):
        json_lang = lang

    params["lang"] = json_lang

    params["limit"] = limit

    params["politicalView"] = political_view

    json_show_map_references: list[str] | Unset = UNSET
    if not isinstance(show_map_references, Unset):
        json_show_map_references = []
        for show_map_references_item_data in show_map_references:
            show_map_references_item = show_map_references_item_data.value
            json_show_map_references.append(show_map_references_item)

    params["showMapReferences"] = json_show_map_references

    json_show: list[str] | Unset = UNSET
    if not isinstance(show, Unset):
        json_show = []
        for show_item_data in show:
            show_item = show_item_data.value
            json_show.append(show_item)

    params["show"] = json_show

    json_show_nav_attributes: list[str] | Unset = UNSET
    if not isinstance(show_nav_attributes, Unset):
        json_show_nav_attributes = []
        for show_nav_attributes_item_data in show_nav_attributes:
            show_nav_attributes_item = show_nav_attributes_item_data.value
            json_show_nav_attributes.append(show_nav_attributes_item)

    params["showNavAttributes"] = json_show_nav_attributes

    json_show_related: list[str] | Unset = UNSET
    if not isinstance(show_related, Unset):
        json_show_related = []
        for show_related_item_data in show_related:
            show_related_item = show_related_item_data.value
            json_show_related.append(show_related_item)

    params["showRelated"] = json_show_related

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/revgeocode",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | OpenSearchReverseGeocodeResponse | None:
    if response.status_code == 200:
        response_200 = OpenSearchReverseGeocodeResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | OpenSearchReverseGeocodeResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    at: str | Unset = UNSET,
    bearing: int | Unset = UNSET,
    in_: str | Unset = UNSET,
    types: list[GetRevgeocodeTypesItem] | Unset = UNSET,
    with_: list[GetRevgeocodeWithItem] | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 1,
    political_view: str | Unset = UNSET,
    show_map_references: list[GetRevgeocodeShowMapReferencesItem] | Unset = UNSET,
    show: list[GetRevgeocodeShowItem] | Unset = UNSET,
    show_nav_attributes: list[GetRevgeocodeShowNavAttributesItem] | Unset = UNSET,
    show_related: list[GetRevgeocodeShowRelatedItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[ErrorResponse | OpenSearchReverseGeocodeResponse]:
    """Reverse Geocode

     This endpoint returns the nearest address to geo coordinates specified in the request.

    Args:
        at (str | Unset):  Example: 52.5308,13.3856.
        bearing (int | Unset):  Example: 42.
        in_ (str | Unset):
        types (list[GetRevgeocodeTypesItem] | Unset):
        with_ (list[GetRevgeocodeWithItem] | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 1.
        political_view (str | Unset):
        show_map_references (list[GetRevgeocodeShowMapReferencesItem] | Unset):
        show (list[GetRevgeocodeShowItem] | Unset):
        show_nav_attributes (list[GetRevgeocodeShowNavAttributesItem] | Unset):
        show_related (list[GetRevgeocodeShowRelatedItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OpenSearchReverseGeocodeResponse]
    """

    kwargs = _get_kwargs(
        at=at,
        bearing=bearing,
        in_=in_,
        types=types,
        with_=with_,
        lang=lang,
        limit=limit,
        political_view=political_view,
        show_map_references=show_map_references,
        show=show,
        show_nav_attributes=show_nav_attributes,
        show_related=show_related,
        x_request_id=x_request_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    at: str | Unset = UNSET,
    bearing: int | Unset = UNSET,
    in_: str | Unset = UNSET,
    types: list[GetRevgeocodeTypesItem] | Unset = UNSET,
    with_: list[GetRevgeocodeWithItem] | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 1,
    political_view: str | Unset = UNSET,
    show_map_references: list[GetRevgeocodeShowMapReferencesItem] | Unset = UNSET,
    show: list[GetRevgeocodeShowItem] | Unset = UNSET,
    show_nav_attributes: list[GetRevgeocodeShowNavAttributesItem] | Unset = UNSET,
    show_related: list[GetRevgeocodeShowRelatedItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> ErrorResponse | OpenSearchReverseGeocodeResponse | None:
    """Reverse Geocode

     This endpoint returns the nearest address to geo coordinates specified in the request.

    Args:
        at (str | Unset):  Example: 52.5308,13.3856.
        bearing (int | Unset):  Example: 42.
        in_ (str | Unset):
        types (list[GetRevgeocodeTypesItem] | Unset):
        with_ (list[GetRevgeocodeWithItem] | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 1.
        political_view (str | Unset):
        show_map_references (list[GetRevgeocodeShowMapReferencesItem] | Unset):
        show (list[GetRevgeocodeShowItem] | Unset):
        show_nav_attributes (list[GetRevgeocodeShowNavAttributesItem] | Unset):
        show_related (list[GetRevgeocodeShowRelatedItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OpenSearchReverseGeocodeResponse
    """

    return sync_detailed(
        client=client,
        at=at,
        bearing=bearing,
        in_=in_,
        types=types,
        with_=with_,
        lang=lang,
        limit=limit,
        political_view=political_view,
        show_map_references=show_map_references,
        show=show,
        show_nav_attributes=show_nav_attributes,
        show_related=show_related,
        x_request_id=x_request_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    at: str | Unset = UNSET,
    bearing: int | Unset = UNSET,
    in_: str | Unset = UNSET,
    types: list[GetRevgeocodeTypesItem] | Unset = UNSET,
    with_: list[GetRevgeocodeWithItem] | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 1,
    political_view: str | Unset = UNSET,
    show_map_references: list[GetRevgeocodeShowMapReferencesItem] | Unset = UNSET,
    show: list[GetRevgeocodeShowItem] | Unset = UNSET,
    show_nav_attributes: list[GetRevgeocodeShowNavAttributesItem] | Unset = UNSET,
    show_related: list[GetRevgeocodeShowRelatedItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[ErrorResponse | OpenSearchReverseGeocodeResponse]:
    """Reverse Geocode

     This endpoint returns the nearest address to geo coordinates specified in the request.

    Args:
        at (str | Unset):  Example: 52.5308,13.3856.
        bearing (int | Unset):  Example: 42.
        in_ (str | Unset):
        types (list[GetRevgeocodeTypesItem] | Unset):
        with_ (list[GetRevgeocodeWithItem] | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 1.
        political_view (str | Unset):
        show_map_references (list[GetRevgeocodeShowMapReferencesItem] | Unset):
        show (list[GetRevgeocodeShowItem] | Unset):
        show_nav_attributes (list[GetRevgeocodeShowNavAttributesItem] | Unset):
        show_related (list[GetRevgeocodeShowRelatedItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OpenSearchReverseGeocodeResponse]
    """

    kwargs = _get_kwargs(
        at=at,
        bearing=bearing,
        in_=in_,
        types=types,
        with_=with_,
        lang=lang,
        limit=limit,
        political_view=political_view,
        show_map_references=show_map_references,
        show=show,
        show_nav_attributes=show_nav_attributes,
        show_related=show_related,
        x_request_id=x_request_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    at: str | Unset = UNSET,
    bearing: int | Unset = UNSET,
    in_: str | Unset = UNSET,
    types: list[GetRevgeocodeTypesItem] | Unset = UNSET,
    with_: list[GetRevgeocodeWithItem] | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 1,
    political_view: str | Unset = UNSET,
    show_map_references: list[GetRevgeocodeShowMapReferencesItem] | Unset = UNSET,
    show: list[GetRevgeocodeShowItem] | Unset = UNSET,
    show_nav_attributes: list[GetRevgeocodeShowNavAttributesItem] | Unset = UNSET,
    show_related: list[GetRevgeocodeShowRelatedItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> ErrorResponse | OpenSearchReverseGeocodeResponse | None:
    """Reverse Geocode

     This endpoint returns the nearest address to geo coordinates specified in the request.

    Args:
        at (str | Unset):  Example: 52.5308,13.3856.
        bearing (int | Unset):  Example: 42.
        in_ (str | Unset):
        types (list[GetRevgeocodeTypesItem] | Unset):
        with_ (list[GetRevgeocodeWithItem] | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 1.
        political_view (str | Unset):
        show_map_references (list[GetRevgeocodeShowMapReferencesItem] | Unset):
        show (list[GetRevgeocodeShowItem] | Unset):
        show_nav_attributes (list[GetRevgeocodeShowNavAttributesItem] | Unset):
        show_related (list[GetRevgeocodeShowRelatedItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OpenSearchReverseGeocodeResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            at=at,
            bearing=bearing,
            in_=in_,
            types=types,
            with_=with_,
            lang=lang,
            limit=limit,
            political_view=political_view,
            show_map_references=show_map_references,
            show=show,
            show_nav_attributes=show_nav_attributes,
            show_related=show_related,
            x_request_id=x_request_id,
        )
    ).parsed
