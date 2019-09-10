"""Efficient parallel version of the path finder system."""

from typing import Tuple, Set

import numpy as np
from numba import jit
from pathfinder.non_recursive_simple_pathfinder import NonRecursiveSimplePathFinder

class ParallelSimplePathFinder(NonRecursiveSimplePathFinder):
    """Concrete path finder that uses Numba to perform operations in parallel."""

    @staticmethod
    @jit(nopython=True, parallel=True, cache=True)
    def _best_neighbor(terrain: np.ndarray, position: Tuple[int, int]) -> Tuple[int, int]:
        curr_x, curr_y = position
        length, width = terrain.shape[:2]
        current_slope = terrain[position][1]
        min_altitude = terrain[position][0]
        min_position = position

        for delta_x in range(-1, 2):
            for delta_y in range(-1, 2):
                new_position = (curr_x + delta_x, curr_y + delta_y)
                new_x, new_y = new_position
                if not ((new_x < 0) or
                        (new_y < 0) or
                        (new_x >= length) or
                        (new_y >= width)) and not new_position == position:
                    new_altitude = terrain[new_position][0]
                    if new_altitude < min_altitude or (new_altitude == min_altitude and
                                                       current_slope > 0):
                        min_altitude = new_altitude
                        min_position = new_position
        return min_position

    def next_neighbor(self, position: Tuple[int, int],
                      visited: Set[Tuple[int, int]]) -> Tuple[int, int]:
        """
        Uses a vectorized clockwise search of neighbors starting at south-west.

        Example:
        >>> terrain = np.array([[(-2, 0), (2, 0), (2, 1), (3, 1)]])
        >>> path_finder = ParallelSimplePathFinder(terrain)
        >>> path_finder.next_neighbor((0, 2), set((0, 2)))
        (0, 1)
        """

        best_neighbor = ParallelSimplePathFinder._best_neighbor(self.terrain, position)
        if not best_neighbor in visited:
            return best_neighbor
        return position

if __name__ == "__main__":
    import doctest
    doctest.testmod()
