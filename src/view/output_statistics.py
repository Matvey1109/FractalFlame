from src.domain.fractal_parameters import FractalParameters
from src.transformations.base import ITransformation


class OutputStatistics:
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path

    def append_to_file(self, fractal_parameters: FractalParameters):
        with open(self.file_path, "a") as file:
            if file.tell() == 0:  # Check if file is empty
                file.write(
                    "| Resolution | Num Iterations | Num Transforms | Transformations | Symmetry Type | Threads | Runtime |\n"
                )
                file.write(
                    "|------------|-----------------|-----------------|-----------------|---------------|---------|---------|\n"
                )

            file.write(
                f"| {fractal_parameters.resolution.width}x{fractal_parameters.resolution.height} | {fractal_parameters.num_iterations} | {fractal_parameters.num_transforms} | {self._format_transformations(fractal_parameters.transformations)} | {fractal_parameters.symmetry_type} | {fractal_parameters.number_of_threads} | {fractal_parameters.runtime:.2f}s |\n"
            )

    def _format_transformations(
        self, transformations: list[type[ITransformation]]
    ) -> str:
        return ", ".join(
            [transformation.__name__ for transformation in transformations]
        )
