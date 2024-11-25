from abc import ABC, abstractmethod

from src.domain.point import Point


class ITransformation(ABC):
    """Abstract base class for all transformations"""

    @abstractmethod
    def apply(self, x: float, y: float) -> Point:
        """Applies the transformation to a point (x, y)"""
        pass
