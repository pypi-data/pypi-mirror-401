from dataclasses_json import DataClassJsonMixin
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Point(DataClassJsonMixin):
    def __post_init__(self) -> None:
        print(self, flush=True)

    x: float
    y: float


@dataclass
class Aoi(DataClassJsonMixin):
    def __post_init__(self) -> None:
        print(self, flush=True)

    name: str
    """Name of the AOI"""

    points: List[Point]
    z: float
    id: Optional[str] = None
