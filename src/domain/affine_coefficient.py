from dataclasses import dataclass

from src.transformations.base import ITransformation


@dataclass
class AffineCoefficient:
    """Stores coefficients for an affine transformation"""

    a: float
    b: float
    c: float
    d: float
    e: float
    f: float
    red: float
    green: float
    blue: float
    transformations: list[type[ITransformation]]
