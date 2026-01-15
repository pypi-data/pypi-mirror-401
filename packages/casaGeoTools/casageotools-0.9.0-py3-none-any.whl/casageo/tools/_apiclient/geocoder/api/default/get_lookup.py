from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_lookup_show_item import GetLookupShowItem
from ...models.get_lookup_show_map_references_item import GetLookupShowMapReferencesItem
from ...models.get_lookup_show_nav_attributes_item import GetLookupShowNavAttributesItem
from ...models.get_lookup_show_related_item import GetLookupShowRelatedItem
from ...models.lookup_response import LookupResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    id: str,
    lang: list[str] | Unset = UNSET,
    political_view: str | Unset = UNSET,
    show: list[GetLookupShowItem] | Unset = UNSET,
    show_map_references: list[GetLookupShowMapReferencesItem] | Unset = UNSET,
    show_nav_attributes: list[GetLookupShowNavAttributesItem] | Unset = UNSET,
    show_related: list[GetLookupShowRelatedItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_request_id, Unset):
        headers["X-Request-ID"] = x_request_id

    params: dict[str, Any] = {}

    params["id"] = id

    json_lang: list[str] | Unset = UNSET
    if not isinstance(lang, Unset):
        json_lang = lang

    params["lang"] = json_lang

    params["politicalView"] = political_view

    json_show: list[str] | Unset = UNSET
    if not isinstance(show, Unset):
        json_show = []
        for show_item_data in show:
            show_item = show_item_data.value
            json_show.append(show_item)

    params["show"] = json_show

    json_show_map_references: list[str] | Unset = UNSET
    if not isinstance(show_map_references, Unset):
        json_show_map_references = []
        for show_map_references_item_data in show_map_references:
            show_map_references_item = show_map_references_item_data.value
            json_show_map_references.append(show_map_references_item)

    params["showMapReferences"] = json_show_map_references

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
        "url": "/lookup",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | LookupResponse | None:
    if response.status_code == 200:
        response_200 = LookupResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

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
) -> Response[ErrorResponse | LookupResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    id: str,
    lang: list[str] | Unset = UNSET,
    political_view: str | Unset = UNSET,
    show: list[GetLookupShowItem] | Unset = UNSET,
    show_map_references: list[GetLookupShowMapReferencesItem] | Unset = UNSET,
    show_nav_attributes: list[GetLookupShowNavAttributesItem] | Unset = UNSET,
    show_related: list[GetLookupShowRelatedItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[ErrorResponse | LookupResponse]:
    """Lookup By ID

     This endpoint looks up a known place using the HERE ID included in the request.

    Args:
        id (str):  Example: here:pds:place:276u33db-8097f3194e4b411081b761ea9a366776.
        lang (list[str] | Unset):
        political_view (str | Unset):
        show (list[GetLookupShowItem] | Unset):
        show_map_references (list[GetLookupShowMapReferencesItem] | Unset):
        show_nav_attributes (list[GetLookupShowNavAttributesItem] | Unset):
        show_related (list[GetLookupShowRelatedItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LookupResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        lang=lang,
        political_view=political_view,
        show=show,
        show_map_references=show_map_references,
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
    id: str,
    lang: list[str] | Unset = UNSET,
    political_view: str | Unset = UNSET,
    show: list[GetLookupShowItem] | Unset = UNSET,
    show_map_references: list[GetLookupShowMapReferencesItem] | Unset = UNSET,
    show_nav_attributes: list[GetLookupShowNavAttributesItem] | Unset = UNSET,
    show_related: list[GetLookupShowRelatedItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> ErrorResponse | LookupResponse | None:
    """Lookup By ID

     This endpoint looks up a known place using the HERE ID included in the request.

    Args:
        id (str):  Example: here:pds:place:276u33db-8097f3194e4b411081b761ea9a366776.
        lang (list[str] | Unset):
        political_view (str | Unset):
        show (list[GetLookupShowItem] | Unset):
        show_map_references (list[GetLookupShowMapReferencesItem] | Unset):
        show_nav_attributes (list[GetLookupShowNavAttributesItem] | Unset):
        show_related (list[GetLookupShowRelatedItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LookupResponse
    """

    return sync_detailed(
        client=client,
        id=id,
        lang=lang,
        political_view=political_view,
        show=show,
        show_map_references=show_map_references,
        show_nav_attributes=show_nav_attributes,
        show_related=show_related,
        x_request_id=x_request_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    id: str,
    lang: list[str] | Unset = UNSET,
    political_view: str | Unset = UNSET,
    show: list[GetLookupShowItem] | Unset = UNSET,
    show_map_references: list[GetLookupShowMapReferencesItem] | Unset = UNSET,
    show_nav_attributes: list[GetLookupShowNavAttributesItem] | Unset = UNSET,
    show_related: list[GetLookupShowRelatedItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[ErrorResponse | LookupResponse]:
    """Lookup By ID

     This endpoint looks up a known place using the HERE ID included in the request.

    Args:
        id (str):  Example: here:pds:place:276u33db-8097f3194e4b411081b761ea9a366776.
        lang (list[str] | Unset):
        political_view (str | Unset):
        show (list[GetLookupShowItem] | Unset):
        show_map_references (list[GetLookupShowMapReferencesItem] | Unset):
        show_nav_attributes (list[GetLookupShowNavAttributesItem] | Unset):
        show_related (list[GetLookupShowRelatedItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LookupResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        lang=lang,
        political_view=political_view,
        show=show,
        show_map_references=show_map_references,
        show_nav_attributes=show_nav_attributes,
        show_related=show_related,
        x_request_id=x_request_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    id: str,
    lang: list[str] | Unset = UNSET,
    political_view: str | Unset = UNSET,
    show: list[GetLookupShowItem] | Unset = UNSET,
    show_map_references: list[GetLookupShowMapReferencesItem] | Unset = UNSET,
    show_nav_attributes: list[GetLookupShowNavAttributesItem] | Unset = UNSET,
    show_related: list[GetLookupShowRelatedItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> ErrorResponse | LookupResponse | None:
    """Lookup By ID

     This endpoint looks up a known place using the HERE ID included in the request.

    Args:
        id (str):  Example: here:pds:place:276u33db-8097f3194e4b411081b761ea9a366776.
        lang (list[str] | Unset):
        political_view (str | Unset):
        show (list[GetLookupShowItem] | Unset):
        show_map_references (list[GetLookupShowMapReferencesItem] | Unset):
        show_nav_attributes (list[GetLookupShowNavAttributesItem] | Unset):
        show_related (list[GetLookupShowRelatedItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LookupResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            lang=lang,
            political_view=political_view,
            show=show,
            show_map_references=show_map_references,
            show_nav_attributes=show_nav_attributes,
            show_related=show_related,
            x_request_id=x_request_id,
        )
    ).parsed
