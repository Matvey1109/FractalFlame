from dataclasses import dataclass


@dataclass
class Resolution:
    """Represents the resolution of an image or rendering"""

    width: int
    height: int
