"""Naive implementation of the closest pair algorithm."""

from typing import Tuple, Callable
from closest_pair.base_closest_pair import BaseClosestPair

class NaiveClosestPair(BaseClosestPair):  
    def closest_pair(self, distance: Callable[[int, int, int, int], float] = BaseClosestPair.distance
                    ) -> Tuple[int, int, float]:
        """
        Iterates over all pairs and computes their distances.
        
        Examples:
        >>> x = [0, 3, 100]
        >>> y = [0, 4, 110]
        >>> ncp = NaiveClosestPair(x, y)
        >>> ncp.closest_pair()
        (0, 1, 5.0)
        """
        
        from math import inf

        n = len(self.x)
        min_distance = inf
        for i in range(n - 1):
            for j in range(i + 1, n):
                d = distance(self.x[i], self.x[j], self.y[i], self.y[j])
                if d < min_distance:
                    min_distance = d
                    p_i = i
                    p_j = j
                    
        return p_i, p_j, min_distance

if __name__ == "__main__":
    import doctest
    doctest.testmod()
