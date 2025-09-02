#!/usr/bin/env python3


"""
Read trajectory counts from text files and tabulate them based on their filenames.
"""


from argparse import ArgumentParser, FileType
import re

import pandas as pd
from su2pg_analysis.provenance import get_basic_metadata, text_metadata


def get_args():
    """
    Parse command-line arguments.
    """
    parser = ArgumentParser(description="Tabulate trajectory counts.")
    parser.add_argument(
        "count_filenames",
        metavar="FILENAME",
        nargs="+",
        help=(
            "Filename of a file containing a trajectory count, "
            "and named according to the beta value."
        ),
    )
    parser.add_argument(
        "--output_file",
        type=FileType("w"),
        help="Where to put the resulting LaTeX table.",
    )
    return parser.parse_args()


def get_data(filenames):
    """
    Collate the beta values in the given filenames,
    and the counts in the files referred to,
    and return them as a Pandas DataFrame.
    """
    data = []
    for filename in filenames:
        beta = float(*re.match(".*beta([0-9.]+)", filename).groups())
        with open(filename, "r", encoding="utf-8") as count_file:
            count = int(count_file.read().strip())
        data.append({"beta": beta, "count": count})
    return pd.DataFrame(data)


def main():
    """
    Turn the given files into a LaTeX table.
    """
    args = get_args()
    data = get_data(args.count_filenames)
    print(text_metadata(get_basic_metadata(), comment_char="%"), file=args.output_file)
    content = data.sort_values(by="beta").to_latex(
        header=[r"$\beta$", r"$N_{{\mathrm{{traj}}}}$"],
        index=False,
        formatters=["{:.02f}".format, "{:d}".format],
        column_format="cc",
    )
    print(content, file=args.output_file)


if __name__ == "__main__":
    main()
