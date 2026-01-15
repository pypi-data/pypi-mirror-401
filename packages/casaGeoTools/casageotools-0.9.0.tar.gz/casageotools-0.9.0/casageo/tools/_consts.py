import argparse
import datetime
import os
from typing import Final

TABLE_ORDER: Final = [
    "id",
    "subid",
    "inputStr",
    "label",
    "street",
    "houseNumber",
    "postalCode",
    "city",
    "county",
    "state",
    "countryName",
    "access_lat",
    "access_lng",
    "pos_lat",
    "pos_lng",
    "resultType",
    "houseNumberType",
    "countryCode",
    "stateCode",
    "countyCode",
    "scoreQuery",
    "score_country",
    "score_city",
    "score_houseNumber",
    "score_postalCode",
    "score_streets",
]

ALLOWED_COLUMNS: Final = {
    "id",
    "street",
    "housenumber",
    "postalcode",
    "city",
    "ctrycode",
    "address_string",
    "_",
}

GEOCODE_COST: Final = 3

SERVER: Final = "https://cg-license.casageo.eu/"

ADDRESS_NAMES_MODES: Final = ["matched", "normalized"]
POSTAL_CODE_MODES: Final = ["cityLookup", "districtLookup"]

RANGE_TYPES: Final = ["time", "distance"]
TRANSPORT_MODES: Final = ["car", "pedestrian", "bicycle"]
ROUTING_MODES: Final = ["fast", "short"]
DIRECTION_TYPES: Final = ["outgoing", "incoming"]

AVOIDABLE_FEATURES: Final = [
    "carShuttleTrain",
    "controlledAccessHighway",
    "dirtRoad",
    "ferry",
    "seasonalClosure",
    "tollRoad",
    "tunnel",
    # "uTurns", # Not supported for pedestrian, bicycle and scooter transport modes.
]

UNIT_SYSTEMS: Final = ["metric", "imperial"]


def get_client_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser("casageoclient")
    # TODO: Command Line Interface
    return parser


def get_coder_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser("casageocoder")
    parser.add_argument(
        "--output",
        help="File to output to if not given will default to stdout.",
        default=None,
    )
    parser.add_argument(
        "--indent",
        help="The indent of the output json if not given wont be indented",
        default=None,
        type=int,
    )
    parser.add_argument(
        "--file", type=str, default="", help="Provide a csv seperated by ;"
    )
    parser.add_argument(
        "--format",
        type=str,
        default="",
        help="Provide a file format, the format is like a csv header, but there are only a few valid column names.",
    )
    parser.add_argument("--street", type=str, default="", help="Provide the street")
    parser.add_argument(
        "--housenumber", type=str, default="", help="Provide the house number"
    )
    parser.add_argument(
        "--postalcode", type=str, default="", help="Provide the postal code"
    )
    parser.add_argument("--city", type=str, default="", help="Provide the city")
    parser.add_argument(
        "--ctrycode", type=str, default="", help="Provide the country code"
    )
    parser.add_argument(
        "--get-info",
        action="store_true",
        help="Prints info about your license key",
    )
    parser.add_argument(
        "--key",
        type=str,
        help="Provide the API key in an argument instead of a file",
        default=os.getenv("CASAGEO_KEY"),
    )
    parser.add_argument(
        "--addrstr", type=str, default="", help="Provide the entire query as one string"
    )
    parser.add_argument("--lang", type=str, default=None, help="Provide a language")
    parser.add_argument(
        "--json", action="store_true", help="output as a json instead of a csv"
    )

    return parser


def get_spatial_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser("casageospatial")
    parser.add_argument(
        "--output",
        help="File to output to if not given will default to stdout.",
        default=None,
    )
    parser.add_argument(
        "--indent",
        help="The indent of the output json if not given wont be indented",
        default=None,
        type=int,
    )
    parser.add_argument(
        "--file", type=str, default="", help="Provide a csv seperated by ;"
    )
    parser.add_argument(
        "--key",
        help="Provide a casageo spatial apikey.",
        default=os.getenv("CASAGEO_KEY"),
    )
    parser.add_argument(
        "--lang", "-l", default="en-US", help="Output language for the data."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    routes_parser = subparsers.add_parser("routes")
    routes_parser.add_argument(
        "--raw",
        action="store_true",
        help="Output the raw json from the api instead of a geojson.",
    )

    routes_parser.add_argument(
        "--routing-mode",
        "-r",
        choices=ROUTING_MODES,
        default="fast",
    )
    routes_parser.add_argument(
        "--transport-mode",
        "-t",
        choices=TRANSPORT_MODES,
        default="car",
    )
    routes_parser.add_argument("pointa")
    routes_parser.add_argument("pointb")

    isolines_parser = subparsers.add_parser("isolines")

    isolines_parser.add_argument(
        "--routing-mode",
        "-r",
        choices=ROUTING_MODES,
        default="fast",
    )
    isolines_parser.add_argument(
        "--vehicle",
        "-v",
        choices=TRANSPORT_MODES,
        default="car",
    )
    isolines_parser.add_argument("--avoid", "-a", type=str)
    isolines_parser.add_argument(
        "--time",
        type=datetime.datetime.fromisoformat,
        help="Provide a date and time in ISO format.",
    )

    isolines_parser.add_argument(
        "--raw",
        action="store_true",
        help="Outputs the raw api response with minimal modifications.",
    )
    isolines_parser.add_argument("--rangetype", choices=RANGE_TYPES, default="time")
    isolines_parser.add_argument("point")
    isolines_parser.add_argument(
        "ranges",
        help="Provide comma seperated ranges in either meters or minutes depending on --range-type.",
    )

    # poi_parser = subparsers.add_parser("poi")
    #
    # poi_parser.add_argument("--limit", "-l", type=int, default=10)
    # poi_parser.add_argument(
    #     "--categories",
    #     "-c",
    #     type=str,
    #     default="100,200,300,400,500,600,700,800,900",
    #     help="https://www.here.com/docs/bundle/geocoding-and-search-api-developer-guide/page/topics-places/places-category-system-full.html",
    # )
    # poi_parser.add_argument("point", type=str)
    # poi_parser.add_argument("--raw", action="store_true", help="Output raw json")
    #
    # revgeocode_parser = subparsers.add_parser("revgeocode")
    # revgeocode_parser.add_argument("at", type=str, help="Specify a location.")
    # revgeocode_parser.add_argument("--raw", action="store_true", help="Output raw json")

    subparsers.add_parser("get-info")
    return parser
