"""The base class for implementing various path finders."""

import abc
from typing import List, Tuple, Set

import numpy as np

class BasePathFinder(metaclass=abc.ABCMeta):
    """
    Finds the path of a ball that descends in a terrain from some starting
    position.

    Args:
    terrain: the terrain's configuration comprised from (altitude, slope)
    integer pairs.
    """

    def __init__(self, terrain: np.ndarray):
        self._terrain = terrain

    @property
    def terrain(self):
        """Gets the current terrain data."""
        return self._terrain

    def wall(self, position: Tuple[int, int]) -> bool:
        """
        Checks whether the provided position is hitting the wall.

        Args:
        position: the pair of integers representing the ball's potential position.

        Output:
        True if the position is hitting the wall, or False otherwise.

        Examples:
        >>> BasePathFinder.__abstractmethods__ = set()
        >>> path_finder = BasePathFinder(np.array([[(-2, 0), (3, 0), (2, 0), (1, 0)]]))
        >>> path_finder.wall((0, 1))
        False
        >>> BasePathFinder.__abstractmethods__ = set()
        >>> path_finder = BasePathFinder(np.array([[(-2, 0), (3, 0), (2, 0), (1, 0)]]))
        >>> path_finder.wall((-1, 0))
        True
        """

        curr_x, curr_y = position
        length, width = self.terrain.shape[:2]
        return (curr_x < 0) or (curr_y < 0) or (curr_x >= length) or (curr_y >= width)

    @abc.abstractmethod
    def next_neighbor(self, position: Tuple[int, int],
                      visited: Set[Tuple[int, int]]) -> Tuple[int, int]:
        """
        Returns the position of the lowest neighbor or the current position.

        Args:
        position: the pair of integers representing the ball's current position.
        visited: the set of visited points.

        Output:
        The position (pair of coordinates) of the lowest neighbor.
        """

    @abc.abstractmethod
    def find_path(self, position: Tuple[int, int],
                  visited: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Finds the path that the ball would follow while descending in the terrain.

        Args:
        position: the pair of integers representing the ball's current position.
        visited: the set of visited points (may be preset to avoid certain points).

        Output:
        The list of coordinates of the path.
        """

    def find_paths(self, positions: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
        """
        Finds paths for all provided starting positions.

        Args:
        positions: the list of positions to for which to calculate path.

        Output:
        The list of paths in the same order as positions.
        """

        return [self.find_path(position, None) for position in positions]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
