from src.domain.resolution import Resolution


class Rect:
    """Represents the boundaries of the fractal rendering area"""

    def __init__(self, xmin: float, xmax: float, ymin: float, ymax: float) -> None:
        self.xmin: float = xmin
        self.xmax: float = xmax
        self.ymin: float = ymin
        self.ymax: float = ymax

    def scale(self, x: float, y: float, resolution: Resolution) -> Resolution:
        """Scale a coordinate from fractal space into pixel space"""
        px = int((x - self.xmin) / (self.xmax - self.xmin) * (resolution.width - 1))
        py = int((y - self.ymin) / (self.ymax - self.ymin) * (resolution.height - 1))
        return Resolution(px, py)
