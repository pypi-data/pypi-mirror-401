from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.ev_station import EvStation
from ...models.fuel_station import FuelStation
from ...models.get_browse_ranking import GetBrowseRanking
from ...models.get_browse_show_item import GetBrowseShowItem
from ...models.open_search_browse_response import OpenSearchBrowseResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    at: str,
    categories: list[str] | Unset = UNSET,
    chains: list[str] | Unset = UNSET,
    food_types: list[str] | Unset = UNSET,
    fuel_station: FuelStation | Unset = UNSET,
    in_: str | Unset = UNSET,
    name: str | Unset = UNSET,
    ranking: GetBrowseRanking | Unset = UNSET,
    route: str | Unset = UNSET,
    ev_station: EvStation | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = UNSET,
    political_view: str | Unset = UNSET,
    show: list[GetBrowseShowItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_request_id, Unset):
        headers["X-Request-ID"] = x_request_id

    params: dict[str, Any] = {}

    params["at"] = at

    json_categories: list[str] | Unset = UNSET
    if not isinstance(categories, Unset):
        json_categories = categories

    params["categories"] = json_categories

    json_chains: list[str] | Unset = UNSET
    if not isinstance(chains, Unset):
        json_chains = chains

    params["chains"] = json_chains

    json_food_types: list[str] | Unset = UNSET
    if not isinstance(food_types, Unset):
        json_food_types = food_types

    params["foodTypes"] = json_food_types

    json_fuel_station: dict[str, Any] | Unset = UNSET
    if not isinstance(fuel_station, Unset):
        json_fuel_station = fuel_station.to_dict()
    if not isinstance(json_fuel_station, Unset):
        params.update((f"fuelStation[{k}]", v) for k, v in json_fuel_station.items())

    params["in"] = in_

    params["name"] = name

    json_ranking: str | Unset = UNSET
    if not isinstance(ranking, Unset):
        json_ranking = ranking.value

    params["ranking"] = json_ranking

    params["route"] = route

    json_ev_station: dict[str, Any] | Unset = UNSET
    if not isinstance(ev_station, Unset):
        json_ev_station = ev_station.to_dict()
    if not isinstance(json_ev_station, Unset):
        params.update((f"evStation[{k}]", v) for k, v in json_ev_station.items())

    json_lang: list[str] | Unset = UNSET
    if not isinstance(lang, Unset):
        json_lang = lang

    params["lang"] = json_lang

    params["limit"] = limit

    params["offset"] = offset

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
        "url": "/browse",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | OpenSearchBrowseResponse | None:
    if response.status_code == 200:
        response_200 = OpenSearchBrowseResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | OpenSearchBrowseResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    at: str,
    categories: list[str] | Unset = UNSET,
    chains: list[str] | Unset = UNSET,
    food_types: list[str] | Unset = UNSET,
    fuel_station: FuelStation | Unset = UNSET,
    in_: str | Unset = UNSET,
    name: str | Unset = UNSET,
    ranking: GetBrowseRanking | Unset = UNSET,
    route: str | Unset = UNSET,
    ev_station: EvStation | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = UNSET,
    political_view: str | Unset = UNSET,
    show: list[GetBrowseShowItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[ErrorResponse | OpenSearchBrowseResponse]:
    """Browse

     This endpoint provides search results for places based on different filters, such as categories
    or name, ranked by distance from a given search center. The only mandatory elements exposed in the
    response
    are ID and position. The other elements shown in the response samples section are only dataset
    attributes
    suggestions.

    Args:
        at (str):  Example: 52.5308,13.3856.
        categories (list[str] | Unset):
        chains (list[str] | Unset):
        food_types (list[str] | Unset):
        fuel_station (FuelStation | Unset):
        in_ (str | Unset):
        name (str | Unset):
        ranking (GetBrowseRanking | Unset):
        route (str | Unset):
        ev_station (EvStation | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 20.
        offset (int | Unset):
        political_view (str | Unset):
        show (list[GetBrowseShowItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OpenSearchBrowseResponse]
    """

    kwargs = _get_kwargs(
        at=at,
        categories=categories,
        chains=chains,
        food_types=food_types,
        fuel_station=fuel_station,
        in_=in_,
        name=name,
        ranking=ranking,
        route=route,
        ev_station=ev_station,
        lang=lang,
        limit=limit,
        offset=offset,
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
    at: str,
    categories: list[str] | Unset = UNSET,
    chains: list[str] | Unset = UNSET,
    food_types: list[str] | Unset = UNSET,
    fuel_station: FuelStation | Unset = UNSET,
    in_: str | Unset = UNSET,
    name: str | Unset = UNSET,
    ranking: GetBrowseRanking | Unset = UNSET,
    route: str | Unset = UNSET,
    ev_station: EvStation | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = UNSET,
    political_view: str | Unset = UNSET,
    show: list[GetBrowseShowItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> ErrorResponse | OpenSearchBrowseResponse | None:
    """Browse

     This endpoint provides search results for places based on different filters, such as categories
    or name, ranked by distance from a given search center. The only mandatory elements exposed in the
    response
    are ID and position. The other elements shown in the response samples section are only dataset
    attributes
    suggestions.

    Args:
        at (str):  Example: 52.5308,13.3856.
        categories (list[str] | Unset):
        chains (list[str] | Unset):
        food_types (list[str] | Unset):
        fuel_station (FuelStation | Unset):
        in_ (str | Unset):
        name (str | Unset):
        ranking (GetBrowseRanking | Unset):
        route (str | Unset):
        ev_station (EvStation | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 20.
        offset (int | Unset):
        political_view (str | Unset):
        show (list[GetBrowseShowItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OpenSearchBrowseResponse
    """

    return sync_detailed(
        client=client,
        at=at,
        categories=categories,
        chains=chains,
        food_types=food_types,
        fuel_station=fuel_station,
        in_=in_,
        name=name,
        ranking=ranking,
        route=route,
        ev_station=ev_station,
        lang=lang,
        limit=limit,
        offset=offset,
        political_view=political_view,
        show=show,
        x_request_id=x_request_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    at: str,
    categories: list[str] | Unset = UNSET,
    chains: list[str] | Unset = UNSET,
    food_types: list[str] | Unset = UNSET,
    fuel_station: FuelStation | Unset = UNSET,
    in_: str | Unset = UNSET,
    name: str | Unset = UNSET,
    ranking: GetBrowseRanking | Unset = UNSET,
    route: str | Unset = UNSET,
    ev_station: EvStation | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = UNSET,
    political_view: str | Unset = UNSET,
    show: list[GetBrowseShowItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[ErrorResponse | OpenSearchBrowseResponse]:
    """Browse

     This endpoint provides search results for places based on different filters, such as categories
    or name, ranked by distance from a given search center. The only mandatory elements exposed in the
    response
    are ID and position. The other elements shown in the response samples section are only dataset
    attributes
    suggestions.

    Args:
        at (str):  Example: 52.5308,13.3856.
        categories (list[str] | Unset):
        chains (list[str] | Unset):
        food_types (list[str] | Unset):
        fuel_station (FuelStation | Unset):
        in_ (str | Unset):
        name (str | Unset):
        ranking (GetBrowseRanking | Unset):
        route (str | Unset):
        ev_station (EvStation | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 20.
        offset (int | Unset):
        political_view (str | Unset):
        show (list[GetBrowseShowItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OpenSearchBrowseResponse]
    """

    kwargs = _get_kwargs(
        at=at,
        categories=categories,
        chains=chains,
        food_types=food_types,
        fuel_station=fuel_station,
        in_=in_,
        name=name,
        ranking=ranking,
        route=route,
        ev_station=ev_station,
        lang=lang,
        limit=limit,
        offset=offset,
        political_view=political_view,
        show=show,
        x_request_id=x_request_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    at: str,
    categories: list[str] | Unset = UNSET,
    chains: list[str] | Unset = UNSET,
    food_types: list[str] | Unset = UNSET,
    fuel_station: FuelStation | Unset = UNSET,
    in_: str | Unset = UNSET,
    name: str | Unset = UNSET,
    ranking: GetBrowseRanking | Unset = UNSET,
    route: str | Unset = UNSET,
    ev_station: EvStation | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = UNSET,
    political_view: str | Unset = UNSET,
    show: list[GetBrowseShowItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> ErrorResponse | OpenSearchBrowseResponse | None:
    """Browse

     This endpoint provides search results for places based on different filters, such as categories
    or name, ranked by distance from a given search center. The only mandatory elements exposed in the
    response
    are ID and position. The other elements shown in the response samples section are only dataset
    attributes
    suggestions.

    Args:
        at (str):  Example: 52.5308,13.3856.
        categories (list[str] | Unset):
        chains (list[str] | Unset):
        food_types (list[str] | Unset):
        fuel_station (FuelStation | Unset):
        in_ (str | Unset):
        name (str | Unset):
        ranking (GetBrowseRanking | Unset):
        route (str | Unset):
        ev_station (EvStation | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 20.
        offset (int | Unset):
        political_view (str | Unset):
        show (list[GetBrowseShowItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OpenSearchBrowseResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            at=at,
            categories=categories,
            chains=chains,
            food_types=food_types,
            fuel_station=fuel_station,
            in_=in_,
            name=name,
            ranking=ranking,
            route=route,
            ev_station=ev_station,
            lang=lang,
            limit=limit,
            offset=offset,
            political_view=political_view,
            show=show,
            x_request_id=x_request_id,
        )
    ).parsed
