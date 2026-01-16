"""
Usage:

    ruffup


Runs ruff format + isort on the current path.

Thanks to https://stackoverflow.com/a/78156861/344286
"""

import argparse
import os
import sys


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("PATH", default=".", nargs="?")
    args = parser.parse_args()
    os.system(f"ruff check --select I --fix {args.PATH}")
    os.system(f"ruff format {args.PATH}")


if __name__ == "__main__":
    main()
