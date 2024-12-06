from enum import StrEnum, auto


class SymmetryType(StrEnum):
    """Enum class to store available types of symmetry"""

    NONE = auto()
    HORIZONTAL = auto()
    VERTICAL = auto()
    BOTH = auto()
