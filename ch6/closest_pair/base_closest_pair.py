"""The base class for implementing various variants to find the closest pair."""

import abc
from typing import Tuple, Callable, TypeVar, Sequence, Generic
import numpy as np

Coordinates = TypeVar('Coordinates', Sequence[int], np.ndarray)

class BaseClosestPair(Generic[Coordinates], metaclass=abc.ABCMeta):
    """
    Finds the closest pair among 2D points given by their x and y coordinates. The
    distance is by default defined as a standard Euclidian distance.

    Args:
    x: the list of x coordinates of all points.
    y: the list of y coordinates of all points. The ordering of elements matches
    the list of x coordinates, i.e., the ith point is specified as (x[i], y[i]).
    """

    _x: Coordinates
    _y: Coordinates

    def __init__(self, x: Coordinates, y: Coordinates):
        assert len(x) >= 2 and len(x) == len(y)
        self._x = x
        self._y = y

    @property
    def x(self) -> Coordinates:
        """Gets the x coordinates of points."""
        return self._x

    @property
    def y(self) -> Coordinates:
        """Gets the y coordinates of points."""
        return self._y

    @staticmethod
    def load_from_stdin() -> Tuple[Coordinates, Coordinates]:
        """
        Loads points from standard input by enumarating x and y coordinates in succession.
        Each datum must be separated with space.

        Output:
        The tuple of x and y coordinates.
        """

        import sys

        data = sys.stdin.read()
        points = list(map(int, data.split()))
        x = points[1::2]
        y = points[2::2]
        return x, y

    @staticmethod
    def generate_points(n: int, seed: int) -> Tuple[Coordinates, Coordinates]:
        """
        Generates random points for stress testing.

        Output:
        The tuple of x and y coordinates.

        Examples:
        >>> BaseClosestPair.generate_points(3, 10)
        ([227077737, -930024104, -78967768], [36293302, 241441628, -968147565])
        """

        import random

        assert n >= 2
        random.seed(seed)
        x = [random.randint(-10**9, 10**9) for _ in range(n)]
        y = [random.randint(-10**9, 10**9) for _ in range(n)]

        return x, y

    @staticmethod
    def distance(x1: int, x2: int, y1: int, y2: int) -> float:
        """
        Returns the Euclidian distance between two points.

        Args:
        x1: the x coordinate of the first point.
        x1: the x coordinate of the second point.
        y1: the y coordinate of the first point.
        y2: the y coordinate of the second point.

        Output:
        The distance between points defined as the square root of the sum of squared
        differences of the matching coordinates.

        Examples:
        >>> BaseClosestPair.distance(1, 2, 1, 2)
        1.4142135623730951
        >>> BaseClosestPair.distance(1, 1, 1, 1)
        0.0
        """

        from math import sqrt

        return sqrt((x1 - x2)**2 + (y1 - y2)**2)

    @abc.abstractmethod
    def closest_pair(self, distance: Callable[[int, int, int, int], float]) -> Tuple[int, int, float]:
        """
        Returns back the tuple with indexes of closest points as well as
        their distance.

        Args:
        distance: the function that receives four parameters (x1, x2, y1, y2) and
        returns back the distance between these points.
        """

if __name__ == "__main__":
    import doctest
    doctest.testmod()
