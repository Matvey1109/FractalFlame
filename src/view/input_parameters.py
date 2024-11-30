from src.core.symmetry_type import SymmetryType
from src.domain.fractal_parameters import FractalParameters
from src.domain.rect import Rect
from src.domain.resolution import Resolution
from src.transformations.base import ITransformation
from src.transformations.special import (CrossTransformation,
                                         DiamondTransformation,
                                         DiskTransformation,
                                         HandkerchiefTransformation,
                                         HeartTransformation,
                                         PolarTransformation)
from src.view.parameter_validator import ParameterValidator


class InputParameters:
    """Handles user interaction for setting fractal parameters."""

    DEFAULT_PARAMETERS: FractalParameters = FractalParameters(
        resolution=Resolution(1920, 1080),
        num_iterations=2000,
        num_transforms=8,
        rect=Rect(-1.777, 1.777, -1, 1),
        transformations=[
            CrossTransformation,
            PolarTransformation,
        ],  # Default single transformation
        symmetry_type=SymmetryType.NONE,
        number_of_threads=4,
    )

    AVAILABLE_TRANSFORMATIONS: list[type[ITransformation]] = [
        PolarTransformation,
        HandkerchiefTransformation,
        HeartTransformation,
        DiskTransformation,
        DiamondTransformation,
        CrossTransformation,
    ]

    @staticmethod
    def get_parameters() -> FractalParameters:
        """Prompt user to choose between default and custom parameters."""
        print("Do you want to use default parameters or set custom ones?")
        print("1: Use default parameters")
        print("2: Set custom parameters")

        choice: int = ParameterValidator.get_positive_int(
            "Enter your choice (1 or 2): ", "Choice must be 1 or 2."
        )
        while choice not in [1, 2]:
            print("Invalid choice. Please enter 1 or 2.")
            choice = ParameterValidator.get_positive_int(
                "Enter your choice (1 or 2): ", "Choice must be 1 or 2."
            )

        match choice:
            case 1:
                return InputParameters.DEFAULT_PARAMETERS
            case 2:
                return InputParameters._get_custom_parameters()
            case _:
                raise ValueError("Invalid choice")

    @staticmethod
    def _get_custom_parameters() -> FractalParameters:
        """Prompt the user for custom fractal parameters."""
        print("Enter custom parameters for fractal generation:")

        resolution: Resolution = InputParameters._get_resolution()

        num_iterations: int = ParameterValidator.get_positive_int(
            "Enter the number of iterations (e.g., 500): ",
            "Iterations must be a positive integer.",
        )

        num_transforms: int = ParameterValidator.get_positive_int(
            "Enter the number of affine transformations (e.g., 8): ",
            "Number of transformations must be a positive integer.",
        )

        rect: Rect = InputParameters._get_rendering_area()

        transformations: list[type[ITransformation]] = (
            InputParameters._get_transformations()
        )

        symmetry_type = InputParameters._get_symmetry_type()

        number_of_threads = InputParameters._get_number_of_threads()

        return FractalParameters(
            resolution=resolution,
            num_iterations=num_iterations,
            num_transforms=num_transforms,
            rect=rect,
            transformations=transformations,
            symmetry_type=symmetry_type,
            number_of_threads=number_of_threads,
        )

    @staticmethod
    def _get_resolution() -> Resolution:
        """Prompt user for image width and height, ensuring they are positive integers."""
        width: int = ParameterValidator.get_positive_int(
            "Enter the image width (e.g., 1920): ", "Width must be a positive integer."
        )
        height: int = ParameterValidator.get_positive_int(
            "Enter the image height (e.g., 1080): ",
            "Height must be a positive integer.",
        )
        return Resolution(width, height)

    @staticmethod
    def _get_rendering_area() -> Rect:
        """Prompt user for rendering area bounds, ensuring valid relationships."""
        print("Enter rendering area (left, right, bottom, top):")
        left: float = ParameterValidator.get_float("Left: ")
        right: float = ParameterValidator.get_float("Right: ")
        while right <= left:
            print("Right must be greater than Left.")
            right = ParameterValidator.get_float("Right: ")

        bottom: float = ParameterValidator.get_float("Bottom: ")
        top: float = ParameterValidator.get_float("Top: ")
        while top <= bottom:
            print("Top must be greater than Bottom.")
            top = ParameterValidator.get_float("Top: ")

        return Rect(left, right, bottom, top)

    @staticmethod
    def _get_transformations() -> list[type[ITransformation]]:
        """Prompt user to select transformations from the available list."""
        print("Available transformations:")
        for idx, transformation in enumerate(
            InputParameters.AVAILABLE_TRANSFORMATIONS, start=1
        ):
            print(f"{idx}: {transformation.__name__}")

        print(
            "Enter the numbers of the transformations you want to use, separated by commas (e.g., 1,3,5):"
        )
        while True:
            try:
                selections: list[str] = input("Your selection: ").split(",")
                selected_indices: list[int] = [int(s.strip()) for s in selections]

                if not all(
                    1 <= idx <= len(InputParameters.AVAILABLE_TRANSFORMATIONS)
                    for idx in selected_indices
                ):
                    raise ValueError("Selections out of range.")

                selected_transformations: list[type[ITransformation]] = [
                    InputParameters.AVAILABLE_TRANSFORMATIONS[idx - 1]
                    for idx in selected_indices
                ]

                return selected_transformations
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    @staticmethod
    def _get_symmetry_type() -> SymmetryType:
        """Prompt user to select symmetry type."""
        print("Select symmetry type:")
        for sym_type in SymmetryType:
            print(f"{sym_type.value}: {sym_type.name}")

        choice: str = input("Enter your choice: ")

        while choice not in [sym.value for sym in SymmetryType]:
            print("Invalid choice. Please enter a valid symmetry type.")
            choice: str = input("Enter your choice: ")

        return SymmetryType(choice)

    @staticmethod
    def _get_number_of_threads() -> int:
        """Prompt user to select the number of threads."""
        print("Select the number of threads:")
        print("1: Singlethreading")
        print("4: Multithreading")

        choice: int = ParameterValidator.get_positive_int(
            "Enter your choice: ", "Choice must be 1 or 4."
        )

        while choice not in [1, 4]:
            print("Invalid choice. Please enter 1 or 4.")
            choice = ParameterValidator.get_positive_int(
                "Enter your choice: ", "Choice must be 1 or 4."
            )

        return choice
