import numpy as np
from typing import List, Tuple

def wall(terrain:np.matrix, position:Tuple[int,int]) -> bool:
    """
    Checks whether the provided position is hitting the wall.
    
    Args:
    terrain: the terrain's configuration comprised from integer elevation levels.
    position: the pair of integers representing the ball's potential position.

    Output:
    True if the position is hitting the wall, or False otherwise.
    
    Examples:
    >>> wall(np.matrix([[-2, 3, 2, 1]]), (0, 1))
    False
    >>> wall(np.matrix([[-2, 3, 2, 1]]), (-1, 0))
    True
    """
    
    x, y = position
    length, width = terrain.shape
    return (x < 0) or (y < 0) or (x >= length) or (y >= width)

def next_neighbor(terrain:np.matrix, position:Tuple[int,int]) -> Tuple[int,int]:
    """
    Returns the position of the lowest neighbor.
    
    Args:
    terrain: the terrain's configuration comprised from integer elevation levels.
    position: the pair of integers representing the ball's current position.

    Output:
    The position (pair of coordinates) of the lowest neighbor.
    
    Example:
    >>> next_neighbor(np.matrix([[-2, 3, 2, 1]]), (0, 1))
    (0, 0)
    """
    
    x, y = position
    allowed_neighbors = []
    for delta_x in range(-1, 2):
        for delta_y in range(-1, 2):
            new_position = (x + delta_x, y + delta_y)
            if (not wall(terrain, new_position)):
                allowed_neighbors.append((terrain.item(new_position), new_position))
    return min(allowed_neighbors)[1]

def find_path(terrain:np.matrix, position:Tuple[int,int]) -> List[Tuple[int,int]]:
    """
    Finds the path that the ball would follow while descending in the terrain.
    
    Args:
    terrain: the terrain's configuration comprised from integer elevation levels.
    position: the pair of integers representing the ball's current position.
    
    Output:
    The list of coordinates of the path.
    
    Example:
    >>> find_path(np.matrix([[-2, 3, 2, 1]]), (0, 1))
    [(0, 1), (0, 0)]
    """
    
    next_position = next_neighbor(terrain, position)
    if (position == next_position):
        return [position]
    else:
        return [position] + find_path(terrain, next_position)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()