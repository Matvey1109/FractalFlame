from src.domain.affine_coefficient import AffineCoefficient
from src.domain.point import Point


def affine_transform(x: float, y: float, coeff: AffineCoefficient) -> Point:
    """Applies an affine transformation to a point"""
    transformed_x: float = coeff.a * x + coeff.b * y + coeff.c
    transformed_y: float = coeff.d * x + coeff.e * y + coeff.f

    return Point(transformed_x, transformed_y)
