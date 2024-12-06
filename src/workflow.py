from PIL.Image import Image as PILImage

from src.core.fractal_flame import FractalFlame
from src.domain.affine_coefficient import AffineCoefficient
from src.domain.fractal_parameters import FractalParameters
from src.utils.coefficient_generator import CoefficientGenerator
from src.utils.record_rendering_time import record_rendering_time
from src.view.fractal_image import FractalImage
from src.view.input_parameters import InputParameters
from src.view.output_statistics import OutputStatistics

DATA_FOLDER: str = "data"
IMG_FILENAME: str = f"{DATA_FOLDER}/fractal_flame.png"
STATISTICS_FILENAME: str = f"{DATA_FOLDER}/statistics.md"


def workflow():
    fractal_parameters: FractalParameters = InputParameters.get_parameters()
    print("Program started!")

    coeffs: list[AffineCoefficient] = CoefficientGenerator.generate(
        num_transforms=fractal_parameters.num_transforms,
        transformations=fractal_parameters.transformations,
    )

    fractal_flame: FractalFlame = FractalFlame.create(
        resolution=fractal_parameters.resolution,
        rect=fractal_parameters.rect,
        symmetry_type=fractal_parameters.symmetry_type,
    )

    runtime: float = record_rendering_time(
        fractal_parameters=fractal_parameters,
        coeffs=coeffs,
        fractal_flame=fractal_flame,
    )

    fractal_parameters.runtime = runtime
    fractal_image: PILImage = FractalImage.to_image(fractal_flame)

    fractal_image.save(IMG_FILENAME, "PNG")

    writer: OutputStatistics = OutputStatistics(file_path=STATISTICS_FILENAME)
    writer.append_to_file(fractal_parameters=fractal_parameters)
    print(f"Program finished! Find results in folder *{DATA_FOLDER}*")
