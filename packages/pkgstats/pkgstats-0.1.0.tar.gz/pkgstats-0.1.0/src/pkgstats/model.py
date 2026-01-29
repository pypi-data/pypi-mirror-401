from dataclasses import dataclass, field
from typing import Set


@dataclass
class PackageSummary:
    name: str = ""
    version: str = ""
    maintainer: str = ""
    rank: int = 0
    inst: int = 0
    votes: int = 0
    old: int = 0
    recent_installs: int = 0
    no_files: int = 0
    architectures: Set[str] = field(default_factory=set)
