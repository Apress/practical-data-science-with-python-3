"""Simple recursive path finder implementation."""

from typing import List, Tuple, Set
from pathfinder.base_pathfinder import BasePathFinder

class SimplePathFinder(BasePathFinder):
    """Concrete path finder that uses recursion and is sequential."""

    def next_neighbor(self, position: Tuple[int, int],
                      visited: Set[Tuple[int, int]]) -> Tuple[int, int]:
        """
        Uses a simple clockwise search of neighbors starting at south-west.

        Example:
        >>> path_finder = SimplePathFinder(np.array([[(-2, 0), (3, 0), (2, 0), (1, 0)]]))
        >>> path_finder.next_neighbor((0, 1), set((0, 1)))
        (0, 0)
        """

        curr_x, curr_y = position
        current_slope = self.terrain[position][1]
        min_altitude = self.terrain[position][0]
        min_position = position
        for delta_x in range(-1, 2):
            for delta_y in range(-1, 2):
                new_position = (curr_x + delta_x, curr_y + delta_y)
                if not self.wall(new_position) and not new_position in visited:
                    new_altitude = self.terrain[new_position][0]
                    if new_altitude < min_altitude or (new_altitude == min_altitude and
                                                       current_slope > 0):
                        min_altitude = new_altitude
                        min_position = new_position
        return min_position

    def find_path(self, position: Tuple[int, int],
                  visited: Set[Tuple[int, int]] = None) -> List[Tuple[int, int]]:
        """
        Recursively finds the path.

        Example:
        >>> path_finder = SimplePathFinder(np.array([[(-1, 2), (-2, 1), (-2, 2), (1, 0)]]))
        >>> path_finder.find_path((0, 2))
        [(0, 2), (0, 1)]
        """

        if visited is None:
            visited = set()
        visited.add(position)
        next_position = self.next_neighbor(position, visited)
        if position == next_position:
            return [position]
        return [position] + self.find_path(next_position, visited)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
