import functools
import json
import logging
import os
import unittest
from contextlib import contextmanager
from datetime import datetime
from unittest.mock import patch

import httpx
from shapely import Point

from casageo.coder import CasaGeoCoder
from casageo.spatial import CasaGeoSpatial
from casageo.tools import CasaGeoClient, CasaGeoError

API_KEY = "XXXXX-XXXXX-XXXXX-XXXXX"
FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

POINT_IZET = Point(9.4854461, 53.9580118)
POINT_HH = Point(10.008223, 53.553089)

casageo_logger = logging.getLogger("casageo.tools")
casageo_logger.setLevel(logging.ERROR)  # Ignore warnings about caught errors.


@functools.cache
def load_fixture(name: str):
    with open(os.path.join(FIXTURE_DIR, f"{name}.json"), mode="rb") as f:
        return json.load(f)


@contextmanager
def mock_request(apiclient, fixture):
    # TODO: Remove the need for the apiclient parameter by unifying the API clients.
    with patch("httpx.Client.request", autospec=True) as mock:
        mock.return_value = httpx.Response(**fixture["response"])
        yield mock
        mock.assert_called_once_with(apiclient.get_httpx_client(), **fixture["request"])


class TestAccountInfo(unittest.TestCase):
    def setUp(self):
        self.client = CasaGeoClient(API_KEY)
        self.client.preferred_language = "de,en"

    def test_account_info_success(self):
        with mock_request(self.client._v1_client, load_fixture("account_info_1")):
            result = self.client.account_info()
        self.assertTrue(result)
        self.assertEqual("testuser", result.username())
        self.assertEqual("Professional", result.account_type())
        self.assertEqual(43359, result.credits())
        self.assertEqual(
            datetime.fromisoformat("2026-11-18T15:45:09Z"), result.expires()
        )

    def test_account_info_failure(self):
        with patch("httpx.Client.request", return_value=httpx.Response(500)):
            result = self.client.account_info()

        self.assertFalse(result)
        self.assertIsInstance(result.error(), CasaGeoError)
        self.assertEqual("Bad status code 500: b''", str(result.error()))


class TestCoder(unittest.TestCase):
    def setUp(self):
        self.client = CasaGeoClient(API_KEY)
        self.client.preferred_language = "de,en"

        self.cgc = CasaGeoCoder(self.client)

    def test_address(self):
        with mock_request(
            self.client._geocoding_client, load_fixture("coder_address_1")
        ):
            result = self.cgc.address("Fraunhoferstr. 3, 25524 Itzehoe DEU")

        self.assertTrue(result)
        # TODO: More assertions.

        df = result.dataframe()
        self.assertEqual(1, len(df))
        self.assertEqual(
            "Fraunhoferstraße 3, 25524 Itzehoe, Deutschland", df["address"][0]
        )
        # TODO: More assertions.

        # TODO: Test the results of dataframe() parameters.


class TestSpatialClient(unittest.TestCase):
    def setUp(self):
        self.client = CasaGeoClient(API_KEY)
        self.client.preferred_language = "de,en"

        self.cgs = CasaGeoSpatial(self.client)
        self.cgs.transport_mode = "car"
        self.cgs.routing_mode = "fast"

    def test_isolines(self):
        with mock_request(
            self.client._isolines_client, load_fixture("spatial_isolines_1")
        ):
            result = self.cgs.isolines(POINT_HH, [3, 9, 15], range_type="time")

        self.assertTrue(result)
        # TODO: More assertions.

        df = result.dataframe(departure_info=True)
        self.assertEqual(3, len(df))
        # TODO: More assertions.

    def test_routes(self):
        with mock_request(
            self.client._routing_client, load_fixture("spatial_routes_1")
        ):
            result = self.cgs.routes(POINT_IZET, POINT_HH)

        self.assertTrue(result)
        # TODO: More assertions.

        df = result.dataframe(departure_info=True, arrival_info=True)
        self.assertEqual(1, len(df))
        # TODO: More assertions.


if __name__ == "__main__":
    unittest.main()
