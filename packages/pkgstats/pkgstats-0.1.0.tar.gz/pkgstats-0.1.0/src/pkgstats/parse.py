import gzip
from pathlib import Path
from collections import Counter
from urllib.error import HTTPError
from urllib.request import urlopen


ARCHS = [
    "alpha",
    "amd64",
    "arm64",
    "armhf",
    "armel",
    "i386",
    "loong64",
    "mipsel",
    "mips64el",
    "ppc64el",
    "riscv64",
    "s390x",
    "powerpc",
    "ppc64",
    "sparc64",
    "alpha",
    "hppa",
    "hurd-amd64",
    "hurd-i386",
    "ia64",
    "kfreebsd-amd64",
    "kfreebsd-i386",
    "m68k",
    "mips",
    "sh4",
    "x32",
]


def get_package_architectures(
    pkg_name: str, verbose: bool, mirror: str, suite="stable", component="main"
):
    pkg_archs = set()

    for arch in ARCHS:
        url = f"{mirror}/dists/{suite}/{component}/binary-{arch}/Packages.gz"
        if verbose:
            print(f"Scanning {arch}…")
        try:
            with urlopen(url):
                pkg_archs.add(arch)
        except HTTPError:
            if verbose:
                print(f"  Could not fetch package file for arch {arch}")
    return pkg_archs


def parse_contents(contents_file: Path) -> Counter:
    counter: Counter = Counter()

    with contents_file.open(encoding="utf-8", errors="ignore") as f:
        for line in f:
            if not line.strip():
                continue

            _, pkgs = line.rsplit(" ", 1)
            for pkg in pkgs.split(","):
                if pkg != "EMPTY_PACKAGE":
                    counter[pkg] += 1

    return counter


def parse_packages(packages_gz: Path) -> dict:
    packages: dict = dict()
    current: dict = dict()

    with gzip.open(packages_gz, "rt", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.rstrip()

            if not line:
                if "Package" in current:
                    packages[current["Package"]] = current
                current = dict()
                continue

            if ":" in line:
                key, value = line.split(":", 1)
                current[key.strip()] = value.strip()

    return packages
