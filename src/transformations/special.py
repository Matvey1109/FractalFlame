import math

from src.domain.point import Point
from src.transformations.base import ITransformation


class SphericalTransformation(ITransformation):
    """Spherical transformation (#2)"""

    def apply(self, x: float, y: float) -> Point:
        transformed_x: float = x / (x**2 + y**2)
        transformed_y: float = y / (x**2 + y**2)
        return Point(transformed_x, transformed_y)


class PolarTransformation(ITransformation):
    """Polar transformation (#5)"""

    def apply(self, x: float, y: float) -> Point:
        radius: float = math.sqrt(x**2 + y**2)
        theta: float = math.atan2(y, x)

        transformed_x: float = theta / math.pi
        transformed_y: float = radius - 1
        return Point(transformed_x, transformed_y)


class HandkerchiefTransformation(ITransformation):
    """Handkerchief transformation (#6)"""

    def apply(self, x: float, y: float) -> Point:
        radius: float = math.sqrt(x**2 + y**2)
        theta: float = math.atan2(y, x)

        transformed_x: float = radius * math.sin(theta + radius)
        transformed_y: float = radius * math.cos(theta - radius)
        return Point(transformed_x, transformed_y)


class HeartTransformation(ITransformation):
    """Heart transformation (#7)"""

    def apply(self, x: float, y: float) -> Point:
        radius: float = math.sqrt(x**2 + y**2)
        theta: float = math.atan2(y, x)

        transformed_x: float = radius * math.sin(theta * radius)
        transformed_y: float = -radius * math.cos(theta * radius)
        return Point(transformed_x, transformed_y)


class DiskTransformation(ITransformation):
    """Disk transformation (#8)"""

    def apply(self, x: float, y: float) -> Point:
        radius: float = math.sqrt(x**2 + y**2)
        theta: float = math.atan2(y, x)

        transformed_x: float = theta / math.pi * math.sin(radius * math.pi)
        transformed_y: float = theta / math.pi * math.cos(radius * math.pi)
        return Point(transformed_x, transformed_y)


class DiamondTransformation(ITransformation):
    """Diamond transformation (#11)"""

    def apply(self, x: float, y: float) -> Point:
        radius: float = math.sqrt(x**2 + y**2)
        theta: float = math.atan2(y, x)

        transformed_x: float = math.sin(theta) * math.cos(radius)
        transformed_y: float = math.cos(theta) * math.sin(radius)
        return Point(transformed_x, transformed_y)


class CrossTransformation(ITransformation):
    """Cross transformation (#48)"""

    def apply(self, x: float, y: float) -> Point:
        radius_denominator: float = (x**2 - y**2) ** 2

        if math.isclose(radius_denominator, 0.0):
            raise ZeroDivisionError("Division by zero in radius denominator")

        radius: float = math.sqrt(1 / radius_denominator)

        transformed_x: float = radius * x
        transformed_y: float = radius * y
        return Point(transformed_x, transformed_y)
