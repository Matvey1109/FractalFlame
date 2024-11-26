from PIL import Image
from PIL.Image import Image as PILImage

from src.core.fractal_flame import FractalFlame


class FractalImageView:
    @staticmethod
    def to_image(fractal_flame: FractalFlame) -> PILImage:
        # Create a Pillow image from the pixels
        img_array: list[list[tuple[int, int, int]]] = [
            [
                fractal_flame.pixels[py][px].to_tuple()
                for px in range(fractal_flame.resolution.width)
            ]
            for py in range(fractal_flame.resolution.height)
        ]

        # Flatten the list of lists into a single list of tuples (RGB values)
        flattened_img_array: list[tuple[int, int, int]] = [
            color for row in img_array for color in row
        ]

        # Create a Pillow image using the flattened list
        img: PILImage = Image.new(
            "RGB", (fractal_flame.resolution.width, fractal_flame.resolution.height)
        )

        # Put the flattened pixel data into the image
        img.putdata(flattened_img_array)

        return img
