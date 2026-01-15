import math
from collections.abc import Sequence
from dataclasses import KW_ONLY, dataclass
from typing import Any

import shapely
from geopandas import GeoDataFrame
from pandas import DataFrame
from shapely import MultiPoint, Point, Polygon

from . import _consts, _util
from ._client import CasaGeoClient
from ._errors import CasaGeoError
from ._types import CasaGeoResult


def _qq(fields: dict[str, str | None]) -> str:
    return ";".join(f"{key}={val}" for key, val in fields.items() if val is not None)


def _coords(pos: dict) -> tuple[float, float]:
    return (pos.get("lng", math.nan), pos.get("lat", math.nan))


def _item_position(item: dict) -> Point | None:
    try:
        return Point(_coords(item["position"]))
    except KeyError:
        return None


def _item_navigation(item: dict) -> MultiPoint | None:
    try:
        return MultiPoint([_coords(pos) for pos in item["access"]])
    except KeyError:
        return None


def _item_mapview(item: dict) -> Polygon | None:
    try:
        mv = item["mapView"]
        return shapely.box(mv["west"], mv["south"], mv["east"], mv["north"])
    except KeyError:
        return None


class AddressResult(CasaGeoResult):
    """
    Represents the result of a CasaGeoCoder.address() query.
    """

    def dataframe(
        self,
        id_: Any | None = None,
        *,
        address_details: bool = False,
        coordinates: bool = False,
        match_quality: bool = False,
    ) -> GeoDataFrame:
        """
        Return the result as a GeoDataFrame.

        The dataframe will contain the following columns:

        - *id* (str | Any): Fixed identifier added to each row. Can be
          overridden using the ``id_`` parameter.
        - *subid* (int): Numeric index of the result value starting from zero.
        - *address* (str): Localized display name of this result item.
        - *hereid* (str): Unique identifier for the result item in the HERE
          database.
        - *politicalview* (str): ISO 3166-1 alpha-3 country code representing
          the political view of the query.
        - *resulttype* (str): The type of the result item, one of "addressBlock",
          "administrativeArea", "houseNumber", "intersection", "locality",
          "place", "postalCodePoint" or "street".
        - *position* (Point): The coordinates of a pin on a map corresponding to
          the item.
        - *navigation* (MultiPoint): The coordinates of the item’s registered
          navigation points.
        - *distance* (int): The distance from the search context position to the
          result item in meters.
        - *relevance* (float): The relevance of the result to the query as a
          number between 0 and 1.
        - *timestamp* (datetime): Timestamp of when this result was created.

        When ``address_details`` is ``True``, the dataframe also contains the
        following columns:

        - *postaladdress* (str): Full address of the item, formatted
          according to the regional postal rules. May not include all address
          components.
        - *country* (str): Name of the country.
        - *countrycode* (str): ISO 3166-1 alpha-3 country code of the country.
        - *state* (str): Name of the state within the country.
        - *statecode* (str): Code or abbreviation of the state.
        - *county* (str): Name of the county or subdivision within the state.
        - *countycode* (str): Code or abbreviation of the county.
        - *city* (str): Name of the city.
        - *district* (str): Name of the district within the city.
        - *subdistrict* (str): Name of the subdistrict within the city.
        - *street* (str): Name of the street.
        - *streets* (list[str]): List of street names on an intersection.
        - *block* (str): Name of the city block.
        - *subblock* (str): Name of the subblock within the city block.
        - *postalcode* (str): Postal code associated with the item.
        - *housenumber* (str): House number, including associated qualifiers.
        - *building* (str): Name of the building.
        - *unit* (str): Information about the unit within the building.

        When ``coordinates`` is True, the dataframe also contains the following
        columns:

        - *position_lng* (float): Longitude of the item’s position.
        - *position_lat* (float): Latitude of the item’s position.
        - *navigation_lng* (list[float]): Longitudes of the item’s navigation
          points.
        - *navigation_lat* (list[float]): Latitudes of the item’s navigation
          points.

        When ``match_quality`` is ``True``, the dataframe also contains the
        columns below. Each of the values is a number between 0 and 1,
        indicating how well the output field matches the corresponding input
        field.

        - *mq_country* (float): Match quality of the ``country`` field.
        - *mq_countrycode* (float): Match quality of the ``countrycode`` field.
        - *mq_state* (float): Match quality of the ``state`` field.
        - *mq_statecode* (float): Match quality of the ``statecode`` field.
        - *mq_county* (float): Match quality of the ``county`` field.
        - *mq_countycode* (float): Match quality of the ``countycode`` field.
        - *mq_city* (float): Match quality of the ``city`` field.
        - *mq_district* (float): Match quality of the ``district`` field.
        - *mq_subdistrict* (float): Match quality of the ``subdistrict`` field.
        - *mq_streets* (list[float]): Match quality of the ``streets`` field
          against each street name in the input query.
        - *mq_block* (float): Match quality of the ``block`` field.
        - *mq_subblock* (float): Match quality of the ``subblock`` field.
        - *mq_postalcode* (float): Match quality of the ``postalcode`` field.
        - *mq_housenumber* (float): Match quality of the ``housenumber`` field.
          If the requested house number could not be found, this indicates the
          numeric difference between the requested house number and the returned
          house number.
        - *mq_building* (float): Match quality of the ``building`` field.
        - *mq_unit* (float): Match quality of the ``unit`` field.
        - *mq_placename* (float): Match quality of the result place name against
          the input query.
        - *mq_ontologyname* (float): Match quality of the result ontology name
          against the input query.

        Args:
            id_: Fixed identifier to be added to each row.
            address_details: Include additional address details in the result.
            coordinates: Include numeric coordinate columns in the result.
            match_quality: Include match quality scores in the result.

        Returns:
            GeoDataFrame: The list of determined locations as a GeoDataFrame.
        """
        #             mq_street: float
        #                 The match quality of the determined streets as a number from 0
        #                 to 1. If the input contains multiple street names, the field
        #                 score is calculated for each of them individually, but only the
        #                 first result is returned.

        if id_ is None:
            id_ = str(self._uuid)

        data: list[dict] = []
        for index, item in enumerate(self._data.get("items", [])):
            data.append(row := {})

            address = item.get("address", {})
            scoring = item.get("scoring", {})

            if True:
                # fmt: off
                row["id"]               = id_
                row["subid"]            = index
                row["address"]          = item.get("title")
                row["hereid"]           = item.get("id")
                row["politicalview"]    = item.get("politicalView")
                row["resulttype"]       = item.get("resultType")
                row["position"]         = _item_position(item)
                row["navigation"]       = _item_navigation(item)
                row["distance"]         = item.get("distance")
                row["relevance"]        = scoring.get("queryScore")
                row["timestamp"]        = self._timestamp
                # fmt: on

            if address_details:
                # fmt: off
                row["postaladdress"]    = address.get("label")
                row["country"]          = address.get("countryName")
                row["countrycode"]      = address.get("countryCode")
                row["state"]            = address.get("state")
                row["statecode"]        = address.get("stateCode")
                row["county"]           = address.get("county")
                row["countycode"]       = address.get("countyCode")
                row["city"]             = address.get("city")
                row["district"]         = address.get("district")
                row["subdistrict"]      = address.get("subdistrict")
                row["street"]           = address.get("street")
                row["streets"]          = address.get("streets")
                row["block"]            = address.get("block")
                row["subblock"]         = address.get("subblock")
                row["postalcode"]       = address.get("postalCode")
                row["housenumber"]      = address.get("houseNumber")
                row["building"]         = address.get("building")
                row["unit"]             = address.get("unit")
                # fmt: on

            if coordinates:
                position = item.get("position", {})
                access = item.get("access", None)
                # fmt: off
                row["position_lng"]     = position.get("lng")
                row["position_lat"]     = position.get("lat")
                row["navigation_lng"]   = [p.get("lng", math.nan) for p in access] if access is not None else None
                row["navigation_lat"]   = [p.get("lat", math.nan) for p in access] if access is not None else None
                # fmt: on

            if match_quality:
                score = scoring.get("fieldScore", {})
                # fmt: off
                row["mq_country"]       = score.get("countryName")
                row["mq_countrycode"]   = score.get("countryCode")
                row["mq_state"]         = score.get("state")
                row["mq_statecode"]     = score.get("stateCode")
                row["mq_county"]        = score.get("county")
                row["mq_countycode"]    = score.get("countyCode")
                row["mq_city"]          = score.get("city")
                row["mq_district"]      = score.get("district")
                row["mq_subdistrict"]   = score.get("subdistrict")
                row["mq_streets"]       = score.get("streets")
                # row["mq_street"]      = _get_first(score.get("streets"))
                row["mq_block"]         = score.get("block")
                row["mq_subblock"]      = score.get("subblock")
                row["mq_postalcode"]    = score.get("postalCode")
                row["mq_housenumber"]   = score.get("houseNumber")
                row["mq_building"]      = score.get("building")
                row["mq_unit"]          = score.get("unit")
                row["mq_placename"]     = score.get("placeName")
                row["mq_ontologyname"]  = score.get("ontologyName")
                # fmt: on

        if not data:
            return GeoDataFrame()

        return GeoDataFrame(data, geometry="position", crs="EPSG:4326")


class _PoiResult(CasaGeoResult):
    """
    Represents the result of a CasaGeoSpatial.poi() query.
    """

    # https://www.here.com/docs/bundle/geocoding-and-search-api-developer-guide/page/topics/endpoint-discover-brief.html
    # https://www.here.com/docs/bundle/geocoding-and-search-api-v7-api-reference/page/index.html#/paths/~1discover/get

    def dataframe(self, id_: Any | None = None) -> GeoDataFrame:
        if id_ is None:
            id_ = str(self._uuid)

        data: list[dict] = []
        for index, item in enumerate(self._data.get("items", [])):
            data.append(row := {})

            # TODO: Address information.

            if True:
                # fmt: off
                row["id"]               = id_
                row["subid"]            = index
                row["title"]            = item.get("title")
                row["hereid"]           = item.get("id")
                row["resulttype"]       = item.get("resultType")
                row["position"]         = _item_position(item)
                row["access"]           = _item_navigation(item)
                row["distance"]         = item.get("distance")
                # fmt: on

        if not data:
            return GeoDataFrame()

        return GeoDataFrame(data, geometry="position", crs="EPSG:4326")


class _RevgeocodeResult(CasaGeoResult):
    """
    Represents the result of a CasaGeoSpatial.revgeocode() query.
    """

    # https://www.here.com/docs/bundle/geocoding-and-search-api-developer-guide/page/topics/endpoint-reverse-geocode-brief.html
    # https://www.here.com/docs/bundle/geocoding-and-search-api-v7-api-reference/page/index.html#/paths/~1revgeocode/get

    def first_title(self) -> str | None:
        try:
            return self._data["items"][0]["title"]
        except (KeyError, IndexError):
            return None

    def dataframe(self, id_: Any | None = None) -> GeoDataFrame:
        if id_ is None:
            id_ = str(self._uuid)

        data: list[dict] = []
        for index, item in enumerate(self._data.get("items", [])):
            data.append(row := {})

            # TODO: Address information.

            if True:
                # fmt: off
                row["id"]               = id_
                row["subid"]            = index
                row["title"]            = item.get("title")
                row["hereid"]           = item.get("id")
                row["resulttype"]       = item.get("resultType")
                row["position"]         = _item_position(item)
                row["access"]           = _item_navigation(item)
                row["distance"]         = item.get("distance")
                row["mapview"]          = _item_mapview(item)
                # fmt: on

        if not data:
            return GeoDataFrame()

        return GeoDataFrame(data, geometry="position", crs="EPSG:4326")


@dataclass
class CasaGeoCoder:
    """
    Provides geocoding operations.

    Attributes:
        client:
            The client object authorizing these queries.

        language:
            The preferred language for the response.

            This must be a valid IETF BCP47 language tag, such as "en-US", or a
            comma-separated list of such tags in order of preference.

        political_view:
            The political view of the query regarding disputed territories.

            This must be a valid ISO 3166-1 alpha-3 country code.

        position:
            The search context position.

        limit:
            Limit on the number of results to return for each query. Must be
            between 1 and 100. ``None`` means to use the API’s default value.

        countries:
            If set, the search is limited to the specified countries. Must be a
            sequence of valid ISO 3166-1 alpha-3 country codes.

        address_names_mode:
            How to handle places with multiple names.

            - ``None``: Prefer matched names for administrative places and
              normalized names for street names.
            - ``"matched"``: Prefer names that match the input query.
            - ``"normalized"``: Prefer the official names of places.

        postal_code_mode:
            How to handle postal codes spanning multiple cities or districts.

            - ``None``: Return only one result per postal code, leaving the city
              or district name blank if necessary.
            - ``"cityLookup"``: When a postal code spans multiple cities, return
              all possible combinations of the postal code with the
              corresponding city names.
            - ``"districtLookup"``: When a postal code spans multiple districts,
              return all possible combinations of the postal code with the
              corresponding city and district names.
    """

    client: CasaGeoClient
    _: KW_ONLY
    language: str | None = None
    political_view: str | None = None
    position: Point | None = None
    limit: int | None = None
    countries: Sequence[str] | None = None
    address_names_mode: str | None = None
    postal_code_mode: str | None = None

    def __post_init__(self) -> None:
        # Check that self.client is not a string, because the beta version of
        # this class took the license key as the first parameter.
        if not isinstance(self.client, CasaGeoClient):
            raise TypeError("client must be a CasaGeoClient instance")
        if self.political_view is None:
            self.political_view = self.client.preferred_political_view

    def _validate(self) -> None:

        if self.language is not None:
            if not self.language:
                raise ValueError("language must not be empty")
            for tag in self.language.split(","):
                _util.validate_ietf_bcp47_language_tag(tag)

        if self.political_view is not None:
            _util.validate_iso3166_alpha3_country_code(self.political_view)

        if self.position is not None:
            if not self.position.is_valid:
                raise ValueError("position must be a valid 2D point")

        if self.limit is not None:
            if not 1 <= self.limit <= 100:
                raise ValueError("limit must be between 1 and 100 inclusive")

        if self.countries is not None:
            if not self.countries:
                raise ValueError("countries must not be empty")
            for ctr in self.countries:
                _util.validate_iso3166_alpha3_country_code(ctr)

        if self.address_names_mode is not None:
            if self.address_names_mode not in _consts.ADDRESS_NAMES_MODES:
                raise ValueError(
                    f"address_names_mode must be one of {_consts.ADDRESS_NAMES_MODES}, got {self.address_names_mode!r}"
                )

        if self.postal_code_mode is not None:
            if self.postal_code_mode not in _consts.POSTAL_CODE_MODES:
                raise ValueError(
                    f"postal_code_mode must be one of {_consts.POSTAL_CODE_MODES}, got {self.postal_code_mode!r}"
                )

    @AddressResult.wrap_errors()
    def address(
        self,
        address: str | None = None,
        *,
        country: str | None = None,
        state: str | None = None,
        county: str | None = None,
        city: str | None = None,
        district: str | None = None,
        street: str | None = None,
        housenumber: str | None = None,
        postalcode: str | None = None,
    ) -> AddressResult:
        """
        Geocode an address and return the API response as an AddressResult object.

        You can supply either a free-form address string or a combination of
        country, state, county, city, district, street, house number and postal
        code. It is currently not possible to supply structured parameters
        and a free-form address string at the same time, but this restriction
        will be lifted in a future version.

        If the input data combines street and house number information into a
        single field, you can pass the resulting string to the ``street``
        parameter and leave the ``housenumber`` parameter unset.

        The structured parameters are not hard filters, meaning it is possible to
        receive results from outside the specified country or city. The
        possibility to add hard filters to queries will be added in a future
        version.

        Args:
            address: A free-form address string.
            country: The name of a country.
            state: The name of a state or province.
            county: The name of a county.
            city: The name of a city.
            district: The name of a city district.
            street: The name of a street.
            housenumber: The house number.
            postalcode: The postal code.

        Returns:
            AddressResult: An AddressResult instance.
        """
        from ._apiclient.geocoder.api.default import get_geocode
        from ._apiclient.geocoder.models import (
            GetGeocodeAddressNamesMode,
            GetGeocodePostalCodeMode,
        )
        from ._apiclient.geocoder.types import UNSET

        def _or_unset(val, /):
            return val if val is not None else UNSET

        self._validate()

        fields = {
            "country": country,
            "state": state,
            "county": county,
            "city": city,
            "district": district,
            "street": street,
            "houseNumber": housenumber,
            "postalCode": postalcode,
        }

        response = get_geocode.sync_detailed(
            client=self.client._geocoding_client,
            q=_or_unset(address),
            qq=_qq(fields) or UNSET,
            at=(
                _util.point_to_latlng(self.position)
                if self.position is not None
                else UNSET
            ),
            in_=(
                ("countryCode:" + ",".join(self.countries))
                if self.countries is not None
                else UNSET
            ),
            # types=(...),
            # with_=(...),
            lang=(self.language.split(",") if self.language is not None else UNSET),
            limit=_or_unset(self.limit),
            political_view=_or_unset(self.political_view),
            address_names_mode=(
                GetGeocodeAddressNamesMode(self.address_names_mode)
                if self.address_names_mode is not None
                else UNSET
            ),
            postal_code_mode=(
                GetGeocodePostalCodeMode(self.postal_code_mode)
                if self.postal_code_mode is not None
                else UNSET
            ),
        )

        return AddressResult.from_response(response)

    # https://www.here.com/docs/bundle/geocoding-and-search-api-developer-guide/page/topics/endpoint-discover-brief.html
    # https://www.here.com/docs/bundle/geocoding-and-search-api-v7-api-reference/page/index.html#/paths/~1discover/get
    @_PoiResult.wrap_errors()
    def _poi(self, position: Point, *, limit: int = 20) -> _PoiResult:
        # TODO: Implement API parameter 'query: str' for a proper discover() method.
        from ._apiclient.old.api.v1 import v1_poi_retrieve

        result = v1_poi_retrieve.sync_detailed(
            client=self.client._v1_client,
            at=_util.point_to_latlng(position),
            limit=limit,
        )
        return _PoiResult.from_response(result)

    # https://www.here.com/docs/bundle/geocoding-and-search-api-developer-guide/page/topics/endpoint-reverse-geocode-brief.html
    # https://www.here.com/docs/bundle/geocoding-and-search-api-v7-api-reference/page/index.html#/paths/~1revgeocode/get
    @_RevgeocodeResult.wrap_errors()
    def _revgeocode(self, position: Point) -> _RevgeocodeResult:
        # TODO: Implement API parameter 'type: Iterable[str] | None = None'.
        # TODO: Implement API parameter 'limit: int = 1'.
        from ._apiclient.old.api.v1 import v1_revgeocode_retrieve
        from ._apiclient.old.types import UNSET

        result = v1_revgeocode_retrieve.sync_detailed(
            client=self.client._v1_client,
            at=_util.point_to_latlng(position),
            lang=(self.language if self.language is not None else UNSET),
        )
        return _RevgeocodeResult.from_response(result)

    def _bulk_address_json(self, address_df: DataFrame) -> dict:
        """
        Geocode all addresses in the input dataframe and return a dict.

        Warning: If a request errors, it may drop the previous data.
        """
        if not (info := self.client.account_info()):
            raise CasaGeoError(
                "Could not retrieve account information for bulk cost calculation"
            ) from info.error()

        estimated_cost = len(address_df) * _consts.GEOCODE_COST
        if info.credits() < estimated_cost:
            raise CasaGeoError(
                f"Insufficient credits to geocode {len(address_df)} addresses"
            )
        out = {}
        for i, row in address_df.iterrows():
            out[i] = self.address(**row.to_dict()).json()
            out[i]["id"] = row["id"]
        return out
