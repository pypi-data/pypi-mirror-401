import argparse

import pandas as pd

# noinspection PyProtectedMember
from casageo.tools import CasaGeoClient, CasaGeoError, _consts, _util

# noinspection PyProtectedMember
from casageo.tools._spatial import CasaGeoSpatial, IsolinesResult, RoutesResult

__all__ = [
    "CasaGeoSpatial",
    "IsolinesResult",
    "RoutesResult",
]


def _main(args: argparse.Namespace) -> dict | pd.DataFrame:
    cga = CasaGeoClient(args.key, preferred_language=args.lang)
    cgs = CasaGeoSpatial(cga)
    match args.command:
        case "isolines":
            cgs.transport_mode = args.transport_mode
            cgs.routing_mode = args.routing_mode
            isolines_result = cgs.isolines(
                _util.lnglat_to_point(args.point),
                [float(x) for x in args.range.split(",")],
                range_type=args.rangetype,
            )
            if args.raw:
                return isolines_result.json()
            else:
                return isolines_result.dataframe()
        case "routes":
            cgs.routing_mode = args.routing_mode
            cgs.transport_mode = args.transport_mode
            routes_result = cgs.routes(
                _util.lnglat_to_point(args.pointa),
                _util.lnglat_to_point(args.pointb),
            )
            if args.raw:
                return routes_result.json()
            else:
                return routes_result.dataframe()
        case "get-info":
            return cga.account_info().json()
        case _:
            raise CasaGeoError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    _util.cli_main(_consts.get_spatial_parser(), _main)
