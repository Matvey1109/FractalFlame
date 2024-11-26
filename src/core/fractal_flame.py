import random
import threading

from src.domain.affine_coefficient import AffineCoefficient
from src.domain.pixel import Pixel
from src.domain.point import Point
from src.domain.rect import Rect
from src.domain.resolution import Resolution
from src.transformations.affine import affine_transform


class FractalFlame:
    """Class holds the pixel grid and manages rendering"""

    def __init__(self, resolution: Resolution, rect: Rect):
        self.resolution: Resolution = resolution
        self.rect: Rect = rect
        self.pixels: list[list[Pixel]] = [
            [Pixel() for _ in range(resolution.width)] for _ in range(resolution.height)
        ]
        self.hit_count: list[list[int]] = [
            [0 for _ in range(resolution.width)] for _ in range(resolution.height)
        ]

    @staticmethod
    def create(resolution: Resolution, rect: Rect):
        return FractalFlame(resolution, rect)

    def render_thread(
        self,
        iterations: int,
        coeffs: list[AffineCoefficient],
        thread_id: int,
        thread_results,
    ):
        """Threaded rendering logic"""
        XMIN, XMAX = self.rect.xmin, self.rect.xmax
        YMIN, YMAX = self.rect.ymin, self.rect.ymax
        x_res: float = self.resolution.width
        y_res: float = self.resolution.height

        # Initialize separate results for this thread
        local_pixels: list[list[Pixel]] = [
            [Pixel() for _ in range(x_res)] for _ in range(y_res)
        ]
        local_hit_count: list[list[int]] = [
            [0 for _ in range(x_res)] for _ in range(y_res)
        ]

        for _ in range(iterations):
            x: float = random.uniform(XMIN, XMAX)
            y: float = random.uniform(YMIN, YMAX)
            point: Point = Point(x, y)

            for _ in range(20):  # Burn-in iterations
                coeff: AffineCoefficient = random.choice(coeffs)
                point: Point = affine_transform(point.x, point.y, coeff)
                point: Point = coeff.transformation.apply(point.x, point.y)

            for _ in range(iterations):  # Main rendering iterations
                coeff: AffineCoefficient = random.choice(coeffs)
                point: Point = affine_transform(point.x, point.y, coeff)
                point: Point = coeff.transformation.apply(point.x, point.y)

                if XMIN <= point.x <= XMAX and YMIN <= point.y <= YMAX:
                    resolution: Resolution = self.rect.scale(
                        point.x, point.y, self.resolution
                    )
                    local_pixels[resolution.height][resolution.width].add_color(
                        coeff.red, coeff.green, coeff.blue
                    )
                    local_hit_count[resolution.height][resolution.width] += 1

        # Store local results in the thread_results dictionary
        thread_results[thread_id] = (local_pixels, local_hit_count)

    def render(self, iterations: int, coeffs: list[AffineCoefficient], num_threads=1):
        """Main rendering function"""
        threads = []
        thread_results = {}
        iterations_per_thread: int = iterations // num_threads

        # Launch threads
        for thread_id in range(num_threads):
            thread: threading.Thread = threading.Thread(
                target=self.render_thread,
                args=(iterations_per_thread, coeffs, thread_id, thread_results),
            )
            threads.append(thread)
            thread.start()

        # Wait for threads to finish
        for thread in threads:
            thread.join()

        # Combine results from all threads
        for thread_id, (local_pixels, local_hit_count) in thread_results.items():
            for py in range(self.resolution.height):
                for px in range(self.resolution.width):
                    self.pixels[py][px].r += local_pixels[py][px].r
                    self.pixels[py][px].g += local_pixels[py][px].g
                    self.pixels[py][px].b += local_pixels[py][px].b
                    self.hit_count[py][px] += local_hit_count[py][px]

        # Normalize pixels and apply gamma correction
        max_hits: int = max(max(row) for row in self.hit_count)
        for py in range(self.resolution.height):
            for px in range(self.resolution.width):
                self.pixels[py][px].normalize(max_hits)
