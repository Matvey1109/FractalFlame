from dataclasses import dataclass

from src.core.symmetry_type import SymmetryType
from src.domain.rect import Rect
from src.domain.resolution import Resolution
from src.transformations.base import ITransformation


@dataclass
class FractalParameters:
    """Stores parameters for fractal flame"""

    resolution: Resolution
    num_iterations: int
    num_transforms: int
    rect: Rect
    transformations: list[type[ITransformation]]
    symmetry_type: SymmetryType
    number_of_threads: int
    runtime: float = 0.0
