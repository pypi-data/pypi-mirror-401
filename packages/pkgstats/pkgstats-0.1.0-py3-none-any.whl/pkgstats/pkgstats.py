#!/usr/bin/env python3
"""
pkgstats.py

Command-line tool to analyze the amount of download for a specified package.
"""

import argparse

from .popcon import fetch_popcon
from .parse import get_package_architectures
from .model import PackageSummary

DEBIAN_MIRROR = "http://ftp.uk.debian.org/debian/"

# ---------------------------
# Command Line Interface
# ---------------------------


def print_summary(pkg: PackageSummary) -> None:
    print(f"\n📦 Package: {pkg.name}")
    print(f"Maintainer: {pkg.maintainer}")
    print(
        f"Rank position: {pkg.rank}"
    )  # is the rank of the package in the popularity contest
    print(f"Available Architectures: {', '.join(sorted(pkg.architectures))}")

    print("\nPopularity Data:")
    print(
        f"N. of users with regular usage: {pkg.votes}"
    )  # number of people who use this package regularly
    print(
        f"N. of old installs (no regular usage): {pkg.old}"
    )  # number of people who installed, but don't use this package regularly
    print(
        f"N. of recent upgrades: {pkg.recent_installs}"
    )  # number of people who upgraded this package recently
    print(
        f"Entry with no info (atime = ctime = 0): {pkg.no_files}"
    )  # entries which don't contain enough info (atime and ctime were 0)
    print(
        f"\n➡️  Total installs of {pkg.name}: {pkg.inst}"
    )  # number of people who installed this package
    print("-" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=("Analyze the amount of download for a specified package.")
    )
    parser.add_argument(
        "package",
        help="Debian package name to inspect",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Enable verbose output",
    )

    args = parser.parse_args()
    if args.package:
        data: PackageSummary = fetch_popcon(args.package)
        data.architectures = get_package_architectures(
            args.package,
            args.verbose, DEBIAN_MIRROR
        )
        print_summary(data)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
