from io import TextIOWrapper
from urllib.request import urlopen
from .model import PackageSummary


DEBIAN_MIRROR = "http://ftp.uk.debian.org/debian/dists/stable/main"
POPCON_URL = "https://popcon.debian.org/by_inst"


def fetch_popcon(package: str) -> PackageSummary:
    data: PackageSummary = PackageSummary()

    with urlopen(POPCON_URL) as response:
        for line in TextIOWrapper(response, encoding="utf-8", errors="ignore"):
            if not line or line.startswith("#") or line.startswith("---"):
                continue

            info = line.split()
            pkg = info[1]
            if package == pkg:
                data = PackageSummary(
                    name=pkg,
                    rank=int(info[0]),
                    inst=int(info[2]),
                    votes=int(info[3]),
                    old=int(info[4]),
                    recent_installs=int(info[5]),
                    no_files=int(info[6]),
                    maintainer=" ".join(info[7:])[1:-1],  # remove parentheses
                    architectures=set(),
                    version="",
                )
                break
    return data
