import pytest

from src.domain.point import Point
from src.transformations.base import ITransformation
from src.transformations.special import (CrossTransformation,
                                         DiamondTransformation,
                                         DiskTransformation,
                                         HandkerchiefTransformation,
                                         HeartTransformation,
                                         PolarTransformation)


@pytest.mark.parametrize(
    "transformation_class, expected_output",
    [
        (PolarTransformation, Point(0.3128329581890012, 2.605551275463989)),
        (HandkerchiefTransformation, Point(-3.5778476801486687, -3.1310513738273134)),
        (HeartTransformation, Point(-1.4104430878355214, 3.318229994436341)),
        (DiskTransformation, Point(-0.29579074248587306, 0.10184447156786328)),
        (DiamondTransformation, Point(-0.7440926423462323, -0.24822376277499156)),
        (CrossTransformation, Point(0.4, 0.6000000000000001)),
    ],
)
def test_transformation_apply(
    transformation_class: type[ITransformation], expected_output: Point
):
    transformation: ITransformation = transformation_class()
    result: Point = transformation.apply(2.0, 3.0)

    assert isinstance(result, Point)
    assert isinstance(result.x, float)
    assert isinstance(result.y, float)
    assert result.x == expected_output.x
    assert result.y == expected_output.y
