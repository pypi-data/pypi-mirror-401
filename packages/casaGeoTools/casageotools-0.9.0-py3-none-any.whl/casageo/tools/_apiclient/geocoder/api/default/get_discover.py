from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.ev_station import EvStation
from ...models.fuel_station import FuelStation
from ...models.get_discover_mobility_mode import GetDiscoverMobilityMode
from ...models.get_discover_ranking import GetDiscoverRanking
from ...models.get_discover_show_item import GetDiscoverShowItem
from ...models.get_discover_with_item import GetDiscoverWithItem
from ...models.open_search_search_response import OpenSearchSearchResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: str,
    at: str | Unset = UNSET,
    fuel_station: FuelStation | Unset = UNSET,
    in_: str | Unset = UNSET,
    mobility_mode: GetDiscoverMobilityMode | Unset = UNSET,
    ranking: GetDiscoverRanking | Unset = UNSET,
    route: str | Unset = UNSET,
    with_: list[GetDiscoverWithItem] | Unset = UNSET,
    ev_station: EvStation | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = UNSET,
    political_view: str | Unset = UNSET,
    show: list[GetDiscoverShowItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_request_id, Unset):
        headers["X-Request-ID"] = x_request_id

    params: dict[str, Any] = {}

    params["q"] = q

    params["at"] = at

    json_fuel_station: dict[str, Any] | Unset = UNSET
    if not isinstance(fuel_station, Unset):
        json_fuel_station = fuel_station.to_dict()
    if not isinstance(json_fuel_station, Unset):
        params.update((f"fuelStation[{k}]", v) for k, v in json_fuel_station.items())

    params["in"] = in_

    json_mobility_mode: str | Unset = UNSET
    if not isinstance(mobility_mode, Unset):
        json_mobility_mode = mobility_mode.value

    params["mobilityMode"] = json_mobility_mode

    json_ranking: str | Unset = UNSET
    if not isinstance(ranking, Unset):
        json_ranking = ranking.value

    params["ranking"] = json_ranking

    params["route"] = route

    json_with_: list[str] | Unset = UNSET
    if not isinstance(with_, Unset):
        json_with_ = []
        for with_item_data in with_:
            with_item = with_item_data.value
            json_with_.append(with_item)

    params["with"] = json_with_

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
        "url": "/discover",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | OpenSearchSearchResponse | None:
    if response.status_code == 200:
        response_200 = OpenSearchSearchResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | OpenSearchSearchResponse]:
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
    fuel_station: FuelStation | Unset = UNSET,
    in_: str | Unset = UNSET,
    mobility_mode: GetDiscoverMobilityMode | Unset = UNSET,
    ranking: GetDiscoverRanking | Unset = UNSET,
    route: str | Unset = UNSET,
    with_: list[GetDiscoverWithItem] | Unset = UNSET,
    ev_station: EvStation | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = UNSET,
    political_view: str | Unset = UNSET,
    show: list[GetDiscoverShowItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[ErrorResponse | OpenSearchSearchResponse]:
    """Discover

     This endpoint processes a free-form text query for an address or place, and returns results in order
    of relevance.

    Args:
        q (str):  Example: Eismieze Berlin.
        at (str | Unset):  Example: 52.5308,13.3856.
        fuel_station (FuelStation | Unset):
        in_ (str | Unset):
        mobility_mode (GetDiscoverMobilityMode | Unset):
        ranking (GetDiscoverRanking | Unset):
        route (str | Unset):
        with_ (list[GetDiscoverWithItem] | Unset):
        ev_station (EvStation | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 20.
        offset (int | Unset):
        political_view (str | Unset):
        show (list[GetDiscoverShowItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OpenSearchSearchResponse]
    """

    kwargs = _get_kwargs(
        q=q,
        at=at,
        fuel_station=fuel_station,
        in_=in_,
        mobility_mode=mobility_mode,
        ranking=ranking,
        route=route,
        with_=with_,
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
    q: str,
    at: str | Unset = UNSET,
    fuel_station: FuelStation | Unset = UNSET,
    in_: str | Unset = UNSET,
    mobility_mode: GetDiscoverMobilityMode | Unset = UNSET,
    ranking: GetDiscoverRanking | Unset = UNSET,
    route: str | Unset = UNSET,
    with_: list[GetDiscoverWithItem] | Unset = UNSET,
    ev_station: EvStation | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = UNSET,
    political_view: str | Unset = UNSET,
    show: list[GetDiscoverShowItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> ErrorResponse | OpenSearchSearchResponse | None:
    """Discover

     This endpoint processes a free-form text query for an address or place, and returns results in order
    of relevance.

    Args:
        q (str):  Example: Eismieze Berlin.
        at (str | Unset):  Example: 52.5308,13.3856.
        fuel_station (FuelStation | Unset):
        in_ (str | Unset):
        mobility_mode (GetDiscoverMobilityMode | Unset):
        ranking (GetDiscoverRanking | Unset):
        route (str | Unset):
        with_ (list[GetDiscoverWithItem] | Unset):
        ev_station (EvStation | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 20.
        offset (int | Unset):
        political_view (str | Unset):
        show (list[GetDiscoverShowItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OpenSearchSearchResponse
    """

    return sync_detailed(
        client=client,
        q=q,
        at=at,
        fuel_station=fuel_station,
        in_=in_,
        mobility_mode=mobility_mode,
        ranking=ranking,
        route=route,
        with_=with_,
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
    q: str,
    at: str | Unset = UNSET,
    fuel_station: FuelStation | Unset = UNSET,
    in_: str | Unset = UNSET,
    mobility_mode: GetDiscoverMobilityMode | Unset = UNSET,
    ranking: GetDiscoverRanking | Unset = UNSET,
    route: str | Unset = UNSET,
    with_: list[GetDiscoverWithItem] | Unset = UNSET,
    ev_station: EvStation | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = UNSET,
    political_view: str | Unset = UNSET,
    show: list[GetDiscoverShowItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> Response[ErrorResponse | OpenSearchSearchResponse]:
    """Discover

     This endpoint processes a free-form text query for an address or place, and returns results in order
    of relevance.

    Args:
        q (str):  Example: Eismieze Berlin.
        at (str | Unset):  Example: 52.5308,13.3856.
        fuel_station (FuelStation | Unset):
        in_ (str | Unset):
        mobility_mode (GetDiscoverMobilityMode | Unset):
        ranking (GetDiscoverRanking | Unset):
        route (str | Unset):
        with_ (list[GetDiscoverWithItem] | Unset):
        ev_station (EvStation | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 20.
        offset (int | Unset):
        political_view (str | Unset):
        show (list[GetDiscoverShowItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OpenSearchSearchResponse]
    """

    kwargs = _get_kwargs(
        q=q,
        at=at,
        fuel_station=fuel_station,
        in_=in_,
        mobility_mode=mobility_mode,
        ranking=ranking,
        route=route,
        with_=with_,
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
    q: str,
    at: str | Unset = UNSET,
    fuel_station: FuelStation | Unset = UNSET,
    in_: str | Unset = UNSET,
    mobility_mode: GetDiscoverMobilityMode | Unset = UNSET,
    ranking: GetDiscoverRanking | Unset = UNSET,
    route: str | Unset = UNSET,
    with_: list[GetDiscoverWithItem] | Unset = UNSET,
    ev_station: EvStation | Unset = UNSET,
    lang: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = UNSET,
    political_view: str | Unset = UNSET,
    show: list[GetDiscoverShowItem] | Unset = UNSET,
    x_request_id: str | Unset = UNSET,
) -> ErrorResponse | OpenSearchSearchResponse | None:
    """Discover

     This endpoint processes a free-form text query for an address or place, and returns results in order
    of relevance.

    Args:
        q (str):  Example: Eismieze Berlin.
        at (str | Unset):  Example: 52.5308,13.3856.
        fuel_station (FuelStation | Unset):
        in_ (str | Unset):
        mobility_mode (GetDiscoverMobilityMode | Unset):
        ranking (GetDiscoverRanking | Unset):
        route (str | Unset):
        with_ (list[GetDiscoverWithItem] | Unset):
        ev_station (EvStation | Unset):
        lang (list[str] | Unset):
        limit (int | Unset):  Default: 20.
        offset (int | Unset):
        political_view (str | Unset):
        show (list[GetDiscoverShowItem] | Unset):
        x_request_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OpenSearchSearchResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            q=q,
            at=at,
            fuel_station=fuel_station,
            in_=in_,
            mobility_mode=mobility_mode,
            ranking=ranking,
            route=route,
            with_=with_,
            ev_station=ev_station,
            lang=lang,
            limit=limit,
            offset=offset,
            political_view=political_view,
            show=show,
            x_request_id=x_request_id,
        )
    ).parsed
