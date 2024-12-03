from dataclasses import dataclass

from src.domain.pixel import Pixel


@dataclass
class RenderData:
    """Class to store render data"""

    pixels: list[list[Pixel]]
    hit_count: list[list[int]]
