import math
import typing


class Point2D(object):
    """2D point class"""

    def __init__(self, x: typing.Union[int, float], y: typing.Union[int, float]):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Size2D(object):
    """2D size class"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def __repr__(self):
        return f"({self.width}, {self.height})"


def rad2deg(rad: typing.Union[int, float]) -> typing.Union[int, float]:
    """Converts radians to degrees."""
    return rad * 180 / math.pi


def deg2rad(deg: typing.Union[int, float]) -> typing.Union[int, float]:
    """Converts degrees to radians."""
    return deg * math.pi / 180
