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
            self.r = self.r ** (1 / gamma)
            self.g = self.g ** (1 / gamma)
            self.b = self.b ** (1 / gamma)

            # Optional: Add brightness adjustment based on log scaling
            # brightness_factor = 1.2
            # self.r *= brightness_factor
            # self.g *= brightness_factor
            # self.b *= brightness_factor

    # def normalize(self, max_hits):
    #     if self.hit_count > 0:
    #         self.r /= self.hit_count
    #         self.g /= self.hit_count
    #         self.b /= self.hit_count

    #         brightness_factor = 2
    #         brightness = (
    #             math.log(self.hit_count + 1) / math.log(max_hits + 1)
    #         ) * brightness_factor
    #         self.r *= brightness
    #         self.g *= brightness
    #         self.b *= brightness

    def to_tuple(self) -> tuple[int, int, int]:
        "Convert pixel to RGB tuple"
        return (
            int(min(self.r, 1.0) * 255),
            int(min(self.g, 1.0) * 255),
            int(min(self.b, 1.0) * 255),
        )
