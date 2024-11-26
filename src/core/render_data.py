from dataclasses import dataclass

from src.domain.pixel import Pixel


@dataclass
class RenderData:
    pixels: list[list[Pixel]]
    hit_count: list[list[int]]
