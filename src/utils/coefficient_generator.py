import random

from src.domain.affine_coefficient import AffineCoefficient
from src.transformations.base import ITransformation


class CoefficientGenerator:
    """Utility class for generating random coefficients for affine transformations"""

    @staticmethod
    def generate(
        num_transforms: int, transformation: ITransformation
    ) -> list[AffineCoefficient]:
        """Generates random coefficients for affine transformations"""
        coefficients: list[AffineCoefficient] = []
        for _ in range(num_transforms):
            coefficients.append(
                AffineCoefficient(
                    a=random.uniform(-1, 1),
                    b=random.uniform(-1, 1),
                    c=random.uniform(-1, 1),
                    d=random.uniform(-1, 1),
                    e=random.uniform(-1, 1),
                    f=random.uniform(-1, 1),
                    red=random.random(),
                    green=random.random(),
                    blue=random.random(),
                    transformation=transformation,
                )
            )
        return coefficients
