import argparse
import datetime
from urllib.parse import urljoin

from . import _consts, _util
from ._apiclient.geocoder import AuthenticatedClient as GeocodingClient
from ._apiclient.isolines import AuthenticatedClient as IsolinesClient
from ._apiclient.old import AuthenticatedClient as V1Client
from ._apiclient.router import AuthenticatedClient as RoutingClient
from ._errors import CasaGeoError
from ._types import CasaGeoResult


class AccountResult(CasaGeoResult):
    """
    Represents the result of an account lookup operation.
    """

    def username(self) -> str:
        """Return the username associated with the account."""
        return self._data.get("user", "")

    def account_type(self) -> str:
        """Return a string describing the type of the account."""
        return self._data.get("note", "")

    def credits(self) -> int:
        """Return the number of available credits."""
        return self._data.get("credits", 0)

    def expires(self) -> datetime.datetime | None:
        """Return the expiration date and time of the account."""
        try:
            return datetime.datetime.fromisoformat(self._data["expires"])
        except (KeyError, ValueError):
            return None


class CasaGeoClient:
    """
    The casaGeo API client.

    The ``preferred_*`` attributes are used as default values by
    CasaGeoCoder, CasaGeoSpatial, etc. when making API requests.

    Attributes:
        preferred_language:
            The preferred language for responses. This must be a valid IETF
            BCP47 language tag, such as "en-US", or a comma-separated list of
            such tags in order of preference.

        preferred_political_view:
            The preferred political view for responses. This must be a valid ISO
            3166-1 alpha-3 country code.

        preferred_unit_system:
            The preferred unit system for responses, either ``"metric"`` or
            ``"imperial"``.

    Parameters:
        key: Your casaGeo API license key.
    """

    def __init__(
        self,
        key: str,
        *,
        preferred_language: str | None = None,
        preferred_political_view: str | None = None,
        preferred_unit_system: str | None = None,
    ):
        server = _consts.SERVER
        server_api_v1 = urljoin(server, "api/v1/")

        self._v1_client = V1Client(base_url=server, token=key, prefix="")
        self._geocoding_client = GeocodingClient(
            base_url=server_api_v1, token=key, prefix=""
        )
        self._isolines_client = IsolinesClient(
            base_url=server_api_v1, token=key, prefix=""
        )
        self._routing_client = RoutingClient(
            base_url=server_api_v1, token=key, prefix=""
        )

        self.preferred_language = preferred_language
        self.preferred_political_view = preferred_political_view
        self.preferred_unit_system = preferred_unit_system

    @AccountResult.wrap_errors()
    def account_info(self) -> AccountResult:
        """
        Query the server for account information.

        Returns:
            AccountResult: An AccountResult instance.
        """
        from ._apiclient.old.api.v1 import v1_accountinfo_retrieve

        return AccountResult.from_response(
            v1_accountinfo_retrieve.sync_detailed(client=self._v1_client)
        )


def _main(args: argparse.Namespace):
    cga = CasaGeoClient(args.key, preferred_language=args.lang)
    match args.command:
        case "account-info":
            return cga.account_info().json()
        case _:
            raise CasaGeoError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    _util.cli_main(_consts.get_client_parser(), _main)
