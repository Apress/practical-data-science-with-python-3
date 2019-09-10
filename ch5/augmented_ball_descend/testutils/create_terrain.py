"""Creates a degenerate terrain for measuring various running times."""

import numpy as np

def create_test_terrain(n: int) -> np.ndarray:
    """Creates a square maze-like terrain with alleys of decreasing altitude.

    Args:
    n: number of rows and columns of a terrain

    Output:
    The test terrain of proper size.

    Example:
    >>> terrain = create_test_terrain(9)
    >>> terrain[:, :, 0]
    array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8],
           [81, 81, 81, 81, 81, 81, 81, 81, 17],
           [26, 25, 24, 23, 22, 21, 20, 19, 18],
           [27, 81, 81, 81, 81, 81, 81, 81, 81],
           [36, 37, 38, 39, 40, 41, 42, 43, 44],
           [81, 81, 81, 81, 81, 81, 81, 81, 53],
           [62, 61, 60, 59, 58, 57, 56, 55, 54],
           [63, 81, 81, 81, 81, 81, 81, 81, 81],
           [72, 73, 74, 75, 76, 77, 78, 79, 80]])
    """

    size = n * n
    terrain = np.zeros((n, n, 2), dtype=int)
    terrain[:, :, 0] = np.arange(0, size).reshape((n, n))
    
    # Reverse every 4th row to have proper ordering of elements.
    for i in range(2, n, 4):
        terrain[i, :, 0] = np.flip(terrain[i, :, 0])

    # Create "walls" inside the terrain.
    for i in range(1, n, 4):
        terrain[i, :-1, 0] = size
    for i in range(3, n, 4):
        terrain[i, 1:, 0] = size

    return terrain

if __name__ == "__main__":
    import doctest
    doctest.testmod()
