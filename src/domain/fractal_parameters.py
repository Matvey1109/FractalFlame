from dataclasses import dataclass
from src.domain.rect import Rect
from src.domain.resolution import Resolution
from src.transformations.base import ITransformation


@dataclass
class FractalParameters:
    resolution: Resolution
    num_iterations: int
    num_transforms: int
    rect: Rect
    transformations: list[type[ITransformation]]
