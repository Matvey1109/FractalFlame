import pytest

from src.domain.pixel import Pixel


class TestPixel:
    @pytest.fixture
    def pixel(self) -> Pixel:
        """Fixture to create a new Pixel instance for each test"""
        return Pixel()

    def test_add_color(self, pixel: Pixel):
        pixel.add_color(0.5, 0.3, 0.1)

        assert pixel.r == 0.5
        assert pixel.g == 0.3
        assert pixel.b == 0.1
        assert pixel.hit_count == 1

    def test_normalize(self, pixel: Pixel):
        pixel.add_color(0.5, 0.3, 0.1)
        pixel.normalize(10)

        assert pixel.r <= 1.0
        assert pixel.g <= 1.0
        assert pixel.b <= 1.0

    def test_to_tuple(self, pixel: Pixel):
        pixel.add_color(0.5, 0.3, 0.1)
        pixel.normalize(10)
        rgb_tuple = pixel.to_tuple()

        assert isinstance(rgb_tuple, tuple)
        assert len(rgb_tuple) == 3
        assert all(isinstance(value, int) for value in rgb_tuple)
        assert all(0 <= value <= 255 for value in rgb_tuple)
