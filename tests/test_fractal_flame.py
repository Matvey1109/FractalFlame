import pytest

from src.core.fractal_flame import FractalFlame
from src.core.symmetry_type import SymmetryType
from src.domain.affine_coefficient import AffineCoefficient
from src.domain.rect import Rect
from src.domain.resolution import Resolution
from src.transformations.special import (DiskTransformation,
                                         SphericalTransformation)
from src.utils.coefficient_generator import CoefficientGenerator


class TestFractalFlame:
    @pytest.fixture
    def fractal_flame(self) -> FractalFlame:
        """Fixture to create a new FractalFlame instance for each test"""
        resolution = Resolution(width=100, height=100)
        rect = Rect(xmin=-1.0, xmax=1.0, ymin=-1.0, ymax=1.0)
        symmetry_type = SymmetryType.NONE
        fractal_flame = FractalFlame.create(resolution, rect, symmetry_type)
        return fractal_flame

    @pytest.fixture
    def coeffs(self) -> list[AffineCoefficient]:
        """Fixture to create a list of AffineCoefficient instances"""
        coeffs: list[AffineCoefficient] = CoefficientGenerator.generate(
            num_transforms=8,
            transformations=[DiskTransformation, SphericalTransformation],
        )
        return coeffs

    def test_create_fractal_flame(self, fractal_flame: FractalFlame):
        assert isinstance(fractal_flame, FractalFlame)
        assert fractal_flame._resolution == Resolution(width=100, height=100)
        assert fractal_flame._symmetry_type == SymmetryType.NONE

    def test_generate_coeffs(self, coeffs: list[AffineCoefficient]):
        assert coeffs is not None
        assert len(coeffs) == 8
        assert all(isinstance(c, AffineCoefficient) for c in coeffs)
