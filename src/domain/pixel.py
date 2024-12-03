import math


class Pixel:
    """Represents an individual pixel with RGB color values and hit count"""

    def __init__(self) -> None:
        self.r: float = 0.0
        self.g: float = 0.0
        self.b: float = 0.0
        self.hit_count: int = 0

    def add_color(self, r: float, g: float, b: float) -> None:
        """Add RGB color values to the pixel and increment the hit count"""
        self.r += r
        self.g += g
        self.b += b
        self.hit_count += 1

    def normalize(self, max_hits: int) -> None:
        """Normalize the pixel's color values based on the maximum number of hits"""
        if self.hit_count > 0:
            # Logarithmic scaling based on hit count
            log_factor: float = math.log(self.hit_count + 1) / math.log(max_hits + 1)
            self.r *= log_factor
            self.g *= log_factor
            self.b *= log_factor

            # Apply gamma correction
            gamma: float = 2.2  # Common gamma value
            self.r = self._apply_gamma_correction(self.r, gamma)
            self.g = self._apply_gamma_correction(self.g, gamma)
            self.b = self._apply_gamma_correction(self.b, gamma)

    def to_tuple(self) -> tuple[int, int, int]:
        "Convert pixel to RGB tuple"
        return (
            int(min(self.r, 1.0) * 255),
            int(min(self.g, 1.0) * 255),
            int(min(self.b, 1.0) * 255),
        )

    def _apply_gamma_correction(self, value: float, gamma: float) -> float:
        """Apply gamma correction to a color value"""
        return value ** (1 / gamma)
