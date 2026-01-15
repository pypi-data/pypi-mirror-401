"""Contains internal utils for dealing with the client"""

import argparse
import inspect
import json
import logging
import re
import sys
from collections import Counter
from collections.abc import Callable, Iterable, MutableMapping
from enum import Enum
from functools import wraps
from http import HTTPStatus
from typing import Any, Protocol, TypeVar

import flexpolyline.decoding
import numpy as np
import pandas as pd
import shapely
from shapely import Point

from ._errors import CasaGeoError

T = TypeVar("T")

logger = logging.getLogger("casageo.tools")

ietf_bcp47_language_tag_pattern = re.compile(r"[A-Za-z0-9]+(-[A-Za-z0-9]+)*")
iso3166_alpha3_country_code_pattern = re.compile(r"[A-Z]{3}")


class Response(Protocol[T]):
    """A response from an endpoint"""

    status_code: HTTPStatus
    content: bytes
    headers: MutableMapping[str, str]
    parsed: T | None


def validate_ietf_bcp47_language_tag(string: str) -> None:
    if not ietf_bcp47_language_tag_pattern.fullmatch(string):
        raise ValueError(f"Invalid IETF BCP 47 language tag: {string!r}")


def validate_iso3166_alpha3_country_code(string: str) -> None:
    if not iso3166_alpha3_country_code_pattern.fullmatch(string):
        raise ValueError(f"Invalid ISO 3166-1 alpha-3 country code: {string!r}")


def load_json(response: Response[Any]) -> dict:
    if response.status_code != 200:
        raise CasaGeoError(
            f"Bad status code {response.status_code}: {response.content!r}"
        )
    data = json.loads(response.content)
    if "error" in data:
        raise CasaGeoError(data["error"])
    return data


def flexpolyline_points(encoded: str) -> np.ndarray:
    """
    Decode a flexpolyline into an array of points.

    While flexpolyline encodes points as lat-lng, this function returns an array
    of lng-lat points to match GeoPandas.

    If the input contains a third dimension, it will be reflected in the output.
    The type of the third dimension is ignored. The third dimension can be
    removed using ``shapely.force_2d()``.

    Args:
        encoded: The encoded flexpolyline.

    Returns:
        np.ndarray: An array of points with either (lng, lat) or (lng, lat, z)
        coordinates, depending on whether the input contained a third dimension.
    """
    return shapely.points([
        (lng, lat, *z) for lat, lng, *z in flexpolyline.decoding.iter_decode(encoded)
    ])


def point_to_latlng(p: Point) -> str:
    """
    Return a lat-lng string representation of a lng-lat Point object.

    The API expects coordinates in the geographic format.
    """
    return f"{p.y},{p.x}"


def lnglat_to_point(data: str) -> Point:
    # FIXME: This function expects a lng-lat string, while the inverse function
    #        produces a lat-lng string. This should at least be documented!
    try:
        lng, lat = (float(val) for val in data.split(","))
    except ValueError as err:
        raise CasaGeoError(
            f"Bad coordinate string {data!r} a good one looks like this 0.0,0.0"
        ) from err
    return Point(lng, lat)


def implicit_enum_parameters(func):
    """
    Decorator that allows parameters of enum type to accept values of
    their underlying type directly.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        signature = inspect.signature(func)
        bound_args = signature.bind(*args, **kwargs)
        for k, v in bound_args.arguments.items():
            param = signature.parameters[k]
            if (
                param != inspect.Parameter.empty
                and isinstance(param.annotation, type)
                and issubclass(param.annotation, Enum)
            ):
                bound_args.arguments[k] = param.annotation(v)

        return func(*bound_args.args, **bound_args.kwargs)

    return wrapper


def duplicates(inp: Iterable[T]) -> list[T]:
    ctr = Counter(inp)
    return [v for v, c in ctr.items() if c > 1]


def cli_throwing_main(
    parser: argparse.ArgumentParser,
    main: Callable[[argparse.Namespace], dict | pd.DataFrame],
):
    args = parser.parse_args()
    if not args.key:
        raise CasaGeoError(
            "Please specify a key in the environment variable CASAGEO_KEY or the --key argument"
        )

    f = sys.stdout
    if args.output:
        f = open(args.output, "w", encoding="utf-8")  # noqa: SIM115

    result = main(args)

    if isinstance(result, dict):
        json.dump(result, f, indent=args.indent, ensure_ascii=False)
    elif isinstance(result, pd.DataFrame):
        result.to_csv(f, sep=";")


def cli_main(
    parser: argparse.ArgumentParser,
    main: Callable[[argparse.Namespace], dict | pd.DataFrame],
):
    try:
        cli_throwing_main(parser, main)
    except Exception as e:
        # this is not pretty, but it will look pretty
        sys.exit(f"{e.__class__.__name__}: {e}")
