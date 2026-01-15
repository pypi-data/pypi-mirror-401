import argparse

import pandas as pd

# noinspection PyProtectedMember
from casageo.tools import CasaGeoClient, CasaGeoError, _consts, _util

# noinspection PyProtectedMember
from casageo.tools._coder import AddressResult, CasaGeoCoder

__all__ = [
    "AddressResult",
    "CasaGeoCoder",
]


def _main(args: argparse.Namespace) -> dict | pd.DataFrame:
    cga = CasaGeoClient(args.key, preferred_language=args.lang)
    cgc = CasaGeoCoder(cga)

    if args.get_info:
        return cga.account_info().json()
    elif args.addrstr:
        result = cgc.address(args.addrstr)
        if args.json:
            return result.json()
        else:
            return result.dataframe()
    elif args.file:
        df = pd.read_csv(args.file, sep=";")
        if args.format:
            column_format = args.format.split(",")
            if len(column_format) != len(df.columns):
                raise CasaGeoError(
                    "The amount of columns in format and data must be equal",
                )

            if not set(column_format).issubset(_consts.ALLOWED_COLUMNS):
                raise CasaGeoError(
                    f"The format must only contain {', '.join(_consts.ALLOWED_COLUMNS)}.",
                )

            dupes = _util.duplicates(column_format)
            while "_" in dupes:
                dupes.remove("_")
            if dupes:
                raise CasaGeoError(
                    "There cannot be multiple columns of the same name except for _",
                )

            # if there is more than one _ rename them to _1, _2 etc
            for i, name in enumerate(column_format):
                if name == "_":
                    column_format[i] = f"_{i}"

            df.columns = column_format

        if "id" not in df.columns:
            raise CasaGeoError("DataFrame must contain an 'id' column")

        if df["id"].duplicated().any():
            raise CasaGeoError("'id' column contains duplicate values")

        if args.json:
            return cgc._bulk_address_json(df)
        else:
            raise CasaGeoError("Dataframe output is currently not supported")
    else:
        raise CasaGeoError("Please provide an argument")


if __name__ == "__main__":
    _util.cli_main(_consts.get_coder_parser(), _main)
