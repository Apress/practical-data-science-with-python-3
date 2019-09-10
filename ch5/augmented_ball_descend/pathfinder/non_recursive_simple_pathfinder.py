"""Simple non-recursive path finder implementation."""

from typing import List, Tuple, Set
from pathfinder.simple_pathfinder import SimplePathFinder

class NonRecursiveSimplePathFinder(SimplePathFinder):
    """Concrete path finder that doesn't use recursion."""

    def find_path(self, position: Tuple[int, int],
                  visited: Set[Tuple[int, int]] = None) -> List[Tuple[int, int]]:
        """
        Iteratively finds the path (without using recursion).

        Example:
        >>> path_finder = NonRecursiveSimplePathFinder(np.array([[(-1, 2), (-2, 1), (-2, 2), (1, 0)]]))
        >>> path_finder.find_path((0, 2))
        [(0, 2), (0, 1)]
        """

        if visited is None:
            visited = set()
        visited.add(position)
        calculated_path = [position]
        next_position = self.next_neighbor(position, visited)

        while position != next_position:
            position = next_position
            visited.add(position)
            calculated_path.append(position)
            next_position = self.next_neighbor(position, visited)

        return calculated_path

if __name__ == "__main__":
    import doctest
    doctest.testmod()
