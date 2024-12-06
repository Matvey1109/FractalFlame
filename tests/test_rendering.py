import pytest

from src.core.fractal_flame import FractalFlame
from src.core.symmetry_type import SymmetryType
from src.domain.affine_coefficient import AffineCoefficient
from src.domain.fractal_parameters import FractalParameters
from src.domain.rect import Rect
from src.domain.resolution import Resolution
from src.transformations.special import CrossTransformation
from src.utils.coefficient_generator import CoefficientGenerator
from src.utils.record_rendering_time import record_rendering_time


@pytest.fixture(scope="module")
def rendering_times() -> dict[int, float]:
    times = {}

    for input_num_threads in [1, 4]:
        resolution: Resolution = Resolution(1920, 1080)
        rect: Rect = Rect(-1.777, 1.777, -1.0, 1.0)
        symmetry_type: SymmetryType = SymmetryType.NONE
        num_iterations: int = 3000
        num_transforms: int = 8
        transformations: list = [CrossTransformation]

        fractal_flame: FractalFlame = FractalFlame(resolution, rect, symmetry_type)

        coeffs: list[AffineCoefficient] = CoefficientGenerator.generate(
            num_transforms=num_transforms,
            transformations=transformations,
        )

        fractal_parameters: FractalParameters = FractalParameters(
            resolution=resolution,
            num_iterations=num_iterations,
            num_transforms=num_transforms,
            rect=rect,
            transformations=transformations,
            symmetry_type=symmetry_type,
            number_of_threads=input_num_threads,
        )

        runtime: float = record_rendering_time(
            fractal_parameters, coeffs, fractal_flame
        )
        times[input_num_threads] = runtime

    return times


def test_rendering_time(rendering_times):
    assert rendering_times[1] > 0
    assert rendering_times[4] > 0
    # assert rendering_times[4] < rendering_times[1]
    # best case (GIL moment)
