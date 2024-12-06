import random
from threading import Thread

from src.core.render_data import RenderData
from src.core.symmetry_type import SymmetryType
from src.domain.affine_coefficient import AffineCoefficient
from src.domain.pixel import Pixel
from src.domain.point import Point
from src.domain.rect import Rect
from src.domain.resolution import Resolution
from src.transformations.affine import affine_transform

NUMBER_OF_SKIPPING_ITERATIONS: int = 20


class FractalFlame:
    """Class holds the pixel grid and manages rendering"""

    def __init__(
        self,
        resolution: Resolution,
        rect: Rect,
        symmetry_type: SymmetryType = SymmetryType.NONE,
    ):
        self._resolution: Resolution = resolution
        self._rect: Rect = rect
        self._pixels: list[list[Pixel]] = [
            [Pixel() for _ in range(resolution.width)] for _ in range(resolution.height)
        ]
        self._hit_count: list[list[int]] = [
            [0 for _ in range(resolution.width)] for _ in range(resolution.height)
        ]
        self._symmetry_type: SymmetryType = symmetry_type

    @staticmethod
    def create(
        resolution: Resolution, rect: Rect, symmetry_type: SymmetryType
    ) -> "FractalFlame":
        return FractalFlame(resolution, rect, symmetry_type)

    def render(
        self, iterations: int, coeffs: list[AffineCoefficient], num_threads=1
    ) -> None:
        """Main rendering function"""
        threads: list[Thread] = []
        thread_results: dict[int, RenderData] = {}
        iterations_per_thread: int = iterations // num_threads

        # Launch threads
        for thread_id in range(num_threads):
            thread: Thread = Thread(
                target=self._render_thread,
                args=(iterations_per_thread, coeffs, thread_id, thread_results),
            )
            threads.append(thread)
            thread.start()

        # Wait for threads to finish
        for thread in threads:
            thread.join()

        # Combine results from all threads
        for thread_id, render_data in thread_results.items():
            for py in range(self._resolution.height):
                for px in range(self._resolution.width):
                    self._pixels[py][px].r += render_data.pixels[py][px].r
                    self._pixels[py][px].g += render_data.pixels[py][px].g
                    self._pixels[py][px].b += render_data.pixels[py][px].b
                    self._hit_count[py][px] += render_data.hit_count[py][px]

        # Normalize pixels and apply gamma correction
        max_hits: int = max(max(row) for row in self._hit_count)
        for py in range(self._resolution.height):
            for px in range(self._resolution.width):
                self._pixels[py][px].normalize(max_hits)

    def _render_thread(
        self,
        iterations: int,
        coeffs: list[AffineCoefficient],
        thread_id: int,
        thread_results: dict[int, RenderData],
    ) -> None:
        """Threaded rendering logic"""
        XMIN, XMAX = self._rect.xmin, self._rect.xmax
        YMIN, YMAX = self._rect.ymin, self._rect.ymax
        x_res: float = self._resolution.width
        y_res: float = self._resolution.height

        # Initialize separate results for this thread
        render_data: RenderData = RenderData(
            pixels=[[Pixel() for _ in range(x_res)] for _ in range(y_res)],
            hit_count=[[0 for _ in range(x_res)] for _ in range(y_res)],
        )

        for _ in range(iterations):
            x: float = random.uniform(XMIN, XMAX)
            y: float = random.uniform(YMIN, YMAX)
            current_point: Point = Point(x, y)

            for _ in range(NUMBER_OF_SKIPPING_ITERATIONS):  # Burn-in iterations
                coeff: AffineCoefficient = random.choice(coeffs)
                current_point: Point = affine_transform(
                    current_point.x, current_point.y, coeff
                )

                for transformation in coeff.transformations:
                    current_point: Point = transformation().apply(
                        current_point.x, current_point.y
                    )

            for _ in range(iterations):  # Main rendering iterations
                coeff: AffineCoefficient = random.choice(coeffs)
                current_point: Point = affine_transform(
                    current_point.x, current_point.y, coeff
                )

                for transformation in coeff.transformations:
                    current_point: Point = transformation().apply(
                        current_point.x, current_point.y
                    )

                # Apply symmetry
                points: list[Point] = self._apply_symmetry(current_point)

                for sym_point in points:
                    if XMIN <= sym_point.x <= XMAX and YMIN <= sym_point.y <= YMAX:
                        resolution: Resolution = self._rect.scale(
                            sym_point.x, sym_point.y, self._resolution
                        )
                        render_data.pixels[resolution.height][
                            resolution.width
                        ].add_color(coeff.red, coeff.green, coeff.blue)
                        render_data.hit_count[resolution.height][resolution.width] += 1

        # Store local results in the thread_results dictionary
        thread_results[thread_id] = render_data

    def _apply_symmetry(self, point: Point) -> list[Point]:
        """Apply symmetry to a point based on the symmetry type"""
        points: list[Point] = [point]  # Original point
        match self._symmetry_type:
            case SymmetryType.HORIZONTAL:
                points.append(Point(point.x, -point.y))
            case SymmetryType.VERTICAL:
                points.append(Point(-point.x, point.y))
            case SymmetryType.BOTH:
                points.extend(
                    [
                        Point(-point.x, point.y),
                        Point(point.x, -point.y),
                        Point(-point.x, -point.y),
                    ]
                )
            case SymmetryType.NONE:
                pass  # No symmetry applied
        return points
