import time

from PIL.Image import Image as PILImage

from src.core.fractal_flame import FractalFlame
from src.core.symmetry_type import SymmetryType
from src.domain.affine_coefficient import AffineCoefficient
from src.domain.rect import Rect
from src.domain.resolution import Resolution
from src.transformations.base import ITransformation
from src.transformations.special import DiskTransformation
from src.utils.coefficient_generator import CoefficientGenerator
from src.view.fractal_image_view import FractalImageView


def workflow():
    width, height = 1920, 1080
    resolution: Resolution = Resolution(width, height)  # Image resolution
    iterations: int = 500  # Number of points to plot (1000000)
    num_transforms: int = 8  # Number of affine transformations
    rect: Rect = Rect(-1.777, 1.777, -1, 1)  # Define the rendering area

    transformation: ITransformation = DiskTransformation()

    coeffs: list[AffineCoefficient] = CoefficientGenerator.generate(
        num_transforms, transformation
    )

    symmetry_type: SymmetryType = SymmetryType.NONE
    fractal_flame: FractalFlame = FractalFlame.create(resolution, rect, symmetry_type)

    start_time = time.time()
    fractal_flame.render(iterations, coeffs, num_threads=1)
    runtime = time.time() - start_time

    fractal_image: PILImage = FractalImageView.to_image(fractal_flame)

    output_filename: str = "fractal_flame.png"
    fractal_image.save(output_filename, "PNG")
    print(f"Output saved to {output_filename}")
    print(f"Image dimensions: {width}x{height}")
    print(
        f"Number of points to plot: {iterations}, Number of affine transformations: {num_transforms}"
    )
    print(f"Runtime: {runtime:.2f} seconds")
