from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_geocode_address_names_mode import GetGeocodeAddressNamesMode
from ...models.get_geocode_postal_code_mode import GetGeocodePostalCodeMode
from ...models.get_geocode_show_item import GetGeocodeShowItem
from ...models.get_geocode_show_map_references_item import (
    GetGeocodeShowMapReferencesItem,
)
from ...models.get_geocode_show_nav_attributes_item import (
    GetGeocodeShowNavAttributesItem,
)
from ...models.get_geocode_show_related_item import GetGeocodeShowRelatedItem
from ...models.get_geocode_show_translations_item import GetGeocodeShowTranslationsItem
from ...models.get_geocode_types_item import GetGeocodeTypesItem
from ...models.get_geocode_with_item import GetGeocodeWithItem
from ...models.open_search_geocode_response import OpenSearchGeocodeResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    address_names_mode: GetGeocodeAddressNamesMode | Unset = UNSET,
    at: str | Unset = UNSET,
    in_: str | Unset = UNSET,
    postal_code_mode: GetGeocodePostalCodeMode | Unset = UNSET,
    q: str | Unset = UNSET,
    qq: str | Unset = UNSET,
    types: list[GetGeocodeTypesItem] | Unset = UNSET,
    with_: list[GetGeocodeWithItem] | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
    political_view: str | Unset = UNSET,
    show: list[GetGeocodeShowItem] | Unset = UNSET,
    show_map_references: list[GetGeocodeShowMapReferencesItem] | Unset = UNSET,
    show_nav_attributes: list[GetGeocodeShowNavAttributesItem] | Unset = UNSET,
    show_related: list[GetGeocodeShowRelatedItem] | Unset = UNSET,
    show_translations: list[GetGeocodeShowTranslationsItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_request_id, Unset):
        headers["X-Request-ID"] = x_request_id

    params: dict[str, Any] = {}

    json_address_names_mode: str | Unset = UNSET
    if not isinstance(address_names_mode, Unset):
        json_address_names_mode = address_names_mode.value

    params["addressNamesMode"] = json_address_names_mode

    params["at"] = at

    params["in"] = in_

    json_postal_code_mode: str | Unset = UNSET
    if not isinstance(postal_code_mode, Unset):
        json_postal_code_mode = postal_code_mode.value

    params["postalCodeMode"] = json_postal_code_mode

    params["q"] = q

    params["qq"] = qq

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

    json_show_translations: list[str] | Unset = UNSET
    if not isinstance(show_translations, Unset):
        json_show_translations = []
        for show_translations_item_data in show_translations:
            show_translations_item = show_translations_item_data.value
            json_show_translations.append(show_translations_item)

    params["showTranslations"] = json_show_translations

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/geocoder",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | OpenSearchGeocodeResponse | None:
    if response.status_code == 200:
        response_200 = OpenSearchGeocodeResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | OpenSearchGeocodeResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    address_names_mode: GetGeocodeAddressNamesMode | Unset = UNSET,
    at: str | Unset = UNSET,
    in_: str | Unset = UNSET,
    postal_code_mode: GetGeocodePostalCodeMode | Unset = UNSET,
    q: str | Unset = UNSET,
    qq: str | Unset = UNSET,
    types: list[GetGeocodeTypesItem] | Unset = UNSET,
    with_: list[GetGeocodeWithItem] | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
    political_view: str | Unset = UNSET,
    show: list[GetGeocodeShowItem] | Unset = UNSET,
    show_map_references: list[GetGeocodeShowMapReferencesItem] | Unset = UNSET,
    show_nav_attributes: list[GetGeocodeShowNavAttributesItem] | Unset = UNSET,
    show_related: list[GetGeocodeShowRelatedItem] | Unset = UNSET,
    show_translations: list[GetGeocodeShowTranslationsItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[ErrorResponse | OpenSearchGeocodeResponse]:
    """Geocode

     This endpoint allows you to find the geo-coordinates of a known address, place, locality or
    administrative area, even if the query is incomplete or partly incorrect. It also returns a
    complete postal address string and address details. It supports structured, unstructured and
    hybrid queries - combinations of structured and unstructured query elements.

    Args:
        address_names_mode (GetGeocodeAddressNamesMode | Unset):
        at (str | Unset):
        in_ (str | Unset):
        postal_code_mode (GetGeocodePostalCodeMode | Unset):
        q (str | Unset):  Example: Invalidenstraße 116 Berlin.
        qq (str | Unset):
        types (list[GetGeocodeTypesItem] | Unset):
        with_ (list[GetGeocodeWithItem] | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 20.
        political_view (str | Unset):
        show (list[GetGeocodeShowItem] | Unset):
        show_map_references (list[GetGeocodeShowMapReferencesItem] | Unset):
        show_nav_attributes (list[GetGeocodeShowNavAttributesItem] | Unset):
        show_related (list[GetGeocodeShowRelatedItem] | Unset):
        show_translations (list[GetGeocodeShowTranslationsItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OpenSearchGeocodeResponse]
    """

    kwargs = _get_kwargs(
        address_names_mode=address_names_mode,
        at=at,
        in_=in_,
        postal_code_mode=postal_code_mode,
        q=q,
        qq=qq,
        types=types,
        with_=with_,
        lang=lang,
        limit=limit,
        political_view=political_view,
        show=show,
        show_map_references=show_map_references,
        show_nav_attributes=show_nav_attributes,
        show_related=show_related,
        show_translations=show_translations,
        x_request_id=x_request_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    address_names_mode: GetGeocodeAddressNamesMode | Unset = UNSET,
    at: str | Unset = UNSET,
    in_: str | Unset = UNSET,
    postal_code_mode: GetGeocodePostalCodeMode | Unset = UNSET,
    q: str | Unset = UNSET,
    qq: str | Unset = UNSET,
    types: list[GetGeocodeTypesItem] | Unset = UNSET,
    with_: list[GetGeocodeWithItem] | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
    political_view: str | Unset = UNSET,
    show: list[GetGeocodeShowItem] | Unset = UNSET,
    show_map_references: list[GetGeocodeShowMapReferencesItem] | Unset = UNSET,
    show_nav_attributes: list[GetGeocodeShowNavAttributesItem] | Unset = UNSET,
    show_related: list[GetGeocodeShowRelatedItem] | Unset = UNSET,
    show_translations: list[GetGeocodeShowTranslationsItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> ErrorResponse | OpenSearchGeocodeResponse | None:
    """Geocode

     This endpoint allows you to find the geo-coordinates of a known address, place, locality or
    administrative area, even if the query is incomplete or partly incorrect. It also returns a
    complete postal address string and address details. It supports structured, unstructured and
    hybrid queries - combinations of structured and unstructured query elements.

    Args:
        address_names_mode (GetGeocodeAddressNamesMode | Unset):
        at (str | Unset):
        in_ (str | Unset):
        postal_code_mode (GetGeocodePostalCodeMode | Unset):
        q (str | Unset):  Example: Invalidenstraße 116 Berlin.
        qq (str | Unset):
        types (list[GetGeocodeTypesItem] | Unset):
        with_ (list[GetGeocodeWithItem] | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 20.
        political_view (str | Unset):
        show (list[GetGeocodeShowItem] | Unset):
        show_map_references (list[GetGeocodeShowMapReferencesItem] | Unset):
        show_nav_attributes (list[GetGeocodeShowNavAttributesItem] | Unset):
        show_related (list[GetGeocodeShowRelatedItem] | Unset):
        show_translations (list[GetGeocodeShowTranslationsItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OpenSearchGeocodeResponse
    """

    return sync_detailed(
        client=client,
        address_names_mode=address_names_mode,
        at=at,
        in_=in_,
        postal_code_mode=postal_code_mode,
        q=q,
        qq=qq,
        types=types,
        with_=with_,
        lang=lang,
        limit=limit,
        political_view=political_view,
        show=show,
        show_map_references=show_map_references,
        show_nav_attributes=show_nav_attributes,
        show_related=show_related,
        show_translations=show_translations,
        x_request_id=x_request_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    address_names_mode: GetGeocodeAddressNamesMode | Unset = UNSET,
    at: str | Unset = UNSET,
    in_: str | Unset = UNSET,
    postal_code_mode: GetGeocodePostalCodeMode | Unset = UNSET,
    q: str | Unset = UNSET,
    qq: str | Unset = UNSET,
    types: list[GetGeocodeTypesItem] | Unset = UNSET,
    with_: list[GetGeocodeWithItem] | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
    political_view: str | Unset = UNSET,
    show: list[GetGeocodeShowItem] | Unset = UNSET,
    show_map_references: list[GetGeocodeShowMapReferencesItem] | Unset = UNSET,
    show_nav_attributes: list[GetGeocodeShowNavAttributesItem] | Unset = UNSET,
    show_related: list[GetGeocodeShowRelatedItem] | Unset = UNSET,
    show_translations: list[GetGeocodeShowTranslationsItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[ErrorResponse | OpenSearchGeocodeResponse]:
    """Geocode

     This endpoint allows you to find the geo-coordinates of a known address, place, locality or
    administrative area, even if the query is incomplete or partly incorrect. It also returns a
    complete postal address string and address details. It supports structured, unstructured and
    hybrid queries - combinations of structured and unstructured query elements.

    Args:
        address_names_mode (GetGeocodeAddressNamesMode | Unset):
        at (str | Unset):
        in_ (str | Unset):
        postal_code_mode (GetGeocodePostalCodeMode | Unset):
        q (str | Unset):  Example: Invalidenstraße 116 Berlin.
        qq (str | Unset):
        types (list[GetGeocodeTypesItem] | Unset):
        with_ (list[GetGeocodeWithItem] | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 20.
        political_view (str | Unset):
        show (list[GetGeocodeShowItem] | Unset):
        show_map_references (list[GetGeocodeShowMapReferencesItem] | Unset):
        show_nav_attributes (list[GetGeocodeShowNavAttributesItem] | Unset):
        show_related (list[GetGeocodeShowRelatedItem] | Unset):
        show_translations (list[GetGeocodeShowTranslationsItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OpenSearchGeocodeResponse]
    """

    kwargs = _get_kwargs(
        address_names_mode=address_names_mode,
        at=at,
        in_=in_,
        postal_code_mode=postal_code_mode,
        q=q,
        qq=qq,
        types=types,
        with_=with_,
        lang=lang,
        limit=limit,
        political_view=political_view,
        show=show,
        show_map_references=show_map_references,
        show_nav_attributes=show_nav_attributes,
        show_related=show_related,
        show_translations=show_translations,
        x_request_id=x_request_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    address_names_mode: GetGeocodeAddressNamesMode | Unset = UNSET,
    at: str | Unset = UNSET,
    in_: str | Unset = UNSET,
    postal_code_mode: GetGeocodePostalCodeMode | Unset = UNSET,
    q: str | Unset = UNSET,
    qq: str | Unset = UNSET,
    types: list[GetGeocodeTypesItem] | Unset = UNSET,
    with_: list[GetGeocodeWithItem] | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
    political_view: str | Unset = UNSET,
    show: list[GetGeocodeShowItem] | Unset = UNSET,
    show_map_references: list[GetGeocodeShowMapReferencesItem] | Unset = UNSET,
    show_nav_attributes: list[GetGeocodeShowNavAttributesItem] | Unset = UNSET,
    show_related: list[GetGeocodeShowRelatedItem] | Unset = UNSET,
    show_translations: list[GetGeocodeShowTranslationsItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> ErrorResponse | OpenSearchGeocodeResponse | None:
    """Geocode

     This endpoint allows you to find the geo-coordinates of a known address, place, locality or
    administrative area, even if the query is incomplete or partly incorrect. It also returns a
    complete postal address string and address details. It supports structured, unstructured and
    hybrid queries - combinations of structured and unstructured query elements.

    Args:
        address_names_mode (GetGeocodeAddressNamesMode | Unset):
        at (str | Unset):
        in_ (str | Unset):
        postal_code_mode (GetGeocodePostalCodeMode | Unset):
        q (str | Unset):  Example: Invalidenstraße 116 Berlin.
        qq (str | Unset):
        types (list[GetGeocodeTypesItem] | Unset):
        with_ (list[GetGeocodeWithItem] | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 20.
        political_view (str | Unset):
        show (list[GetGeocodeShowItem] | Unset):
        show_map_references (list[GetGeocodeShowMapReferencesItem] | Unset):
        show_nav_attributes (list[GetGeocodeShowNavAttributesItem] | Unset):
        show_related (list[GetGeocodeShowRelatedItem] | Unset):
        show_translations (list[GetGeocodeShowTranslationsItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OpenSearchGeocodeResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            address_names_mode=address_names_mode,
            at=at,
            in_=in_,
            postal_code_mode=postal_code_mode,
            q=q,
            qq=qq,
            types=types,
            with_=with_,
            lang=lang,
            limit=limit,
            political_view=political_view,
            show=show,
            show_map_references=show_map_references,
            show_nav_attributes=show_nav_attributes,
            show_related=show_related,
            show_translations=show_translations,
            x_request_id=x_request_id,
        )
    ).parsed
