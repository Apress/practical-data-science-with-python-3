"""Contains various path related utility classes and methods."""

from typing import List, Tuple

import numpy as np

class PathUtils:
    """Encompasses static methods to handle paths."""

    @staticmethod
    def encode_path(terrain: np.ndarray, descend_path: List[Tuple[int, int]]) -> np.ndarray:
        """
        Encodes the path into the terrain by setting the points's 3rd (blue) component to 255.

        Args:
        terrain: the terrain's configuration comprised from (altitude, slope, [aspect])
        integer pairs/triples.

        Output:
        New terrain with an extra 3rd dimension to encode the path.

        Example:
        >>> terrain = np.array([[(-1, 2), (-2, 1), (-2, 2), (1, 0)]])
        >>> PathUtils.encode_path(terrain, [(0, 2), (0, 1)])
        array([[[ -1,   2,   0],
                [ -2,   1, 255],
                [ -2,   2, 255],
                [  1,   0,   0]]])
        """

        # Expand terrain with an extra dimension, as needed.
        if terrain.shape[2] == 2:
            new_shape = terrain.shape[:2] + (3,)
            new_terrain = np.zeros(new_shape, terrain.dtype)
            new_terrain[:terrain.shape[0], :terrain.shape[1], :2] = terrain
        else:
            new_terrain = np.copy(terrain)

        for point in descend_path:
            new_terrain[point][2] = 255
        return new_terrain

    @staticmethod
    def decode_path(terrain: np.ndarray) -> List[Tuple[int, int]]:
        """
        Decodes the path from the terrain by picking points's whose 3rd (blue) component is 255.
        The reconstructed path may not be unique, which depends upon the path finder logic.

        Args:
        terrain: the terrain's configuration encoded with a single path.

        Output:
        The decoded path that is guaranteed to contain all points of the encoded path.
        Ordering of points may differ from what was reported by the matching path finder.
        """

        # Extra exercise to implement this method according to the specification.
        raise NotImplementedError

if __name__ == "__main__":
    import doctest
    doctest.testmod()
