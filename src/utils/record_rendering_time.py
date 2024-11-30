import time

from src.core.fractal_flame import FractalFlame
from src.domain.affine_coefficient import AffineCoefficient
from src.domain.fractal_parameters import FractalParameters


def record_rendering_time(
    fractal_parameters: FractalParameters,
    coeffs: list[AffineCoefficient],
    fractal_flame: FractalFlame,
) -> float:
    """Function for recording rendering time"""
    start_time: float = time.time()
    fractal_flame.render(
        iterations=fractal_parameters.num_iterations,
        coeffs=coeffs,
        num_threads=fractal_parameters.number_of_threads,
    )
    end_time: float = time.time()

    runtime: float = end_time - start_time

    return runtime
