"""Fast implementation of the closest pair algorithm."""

from typing import List, Tuple, Callable
from closest_pair.base_closest_pair import Coordinates, BaseClosestPair

class FastClosestPair(BaseClosestPair):
    _y_prime: List[int]

    def _argsort_y(self) -> List[int]:
        """Finds the permutation of indices that arranges points by y coordinate."""

        return [t[0] for t in sorted(enumerate(self.y), key = lambda t: t[1])]

    def _get_x(self, i: int, s: List[int]) -> int:
        return self.x[self._y_prime[s[i]]]
    
    def _get_y(self, i: int, s: List[int]) -> int:
        return self.y[self._y_prime[s[i]]]
        
    def __init__(self, x: Coordinates, y: Coordinates):
        super().__init__(x, y)
        self._y_prime = self._argsort_y()
        
    def _selection(self, s: List[int], k: int) -> int:
        """Returns the x value of kth smallest point by x coordinate contained in s."""

        def split(v: int) -> Tuple[List[int], List[int], List[int]]:
            """Indirectly splits points in-place around value v into 2 sets (left and right)."""

            store = 0
            sl_idx = 0
            for i in range(len(s)):
                if self._get_x(i, s) < v:
                    s[i], s[store] = s[store], s[i]
                    store += 1
                    sl_idx = store
            for i in range(store, len(s)):
                if self._get_x(i, s) == v:
                    s[i], s[store] = s[store], s[i]
                    store += 1
            return (s[:sl_idx], s[sl_idx:store], s[store:])
          
        import random
        
        v_idx = random.randrange(len(s))
        v = self._get_x(v_idx, s)
        sl, sv, sr = split(v)
        sl_size = len(sl)
        sv_size = len(sv)
        
        if k <= sl_size:
            return self._selection(sl, k)
        if k > sl_size and k <= sl_size + sv_size:
            return self._get_x(-1, sv)
        return self._selection(sr, k - sl_size - sv_size)

    @staticmethod
    def _merge(sl: List[int], sr: List[int]) -> List[int]:
        """
        Merges the two sorted sublists into a new sorted list. The temporary
        storage may be allocated upfront as a further optimization.
        """

        sl_size = len(sl)
        sr_size = len(sr)
        s = [0] * (sl_size + sr_size) 
        k = 0
        i = 0
        j = 0
    
        while i < sl_size and j < sr_size:
            if sl[i] <= sr[j]:
                s[k] = sl[i]
                k += 1
                i += 1
            else:
                s[k] = sr[j]
                k += 1
                j += 1                       
        while i < sl_size:
            s[k] = sl[i]
            k += 1
            i += 1
        while j < sr_size:
            s[k] = sr[j]
            k += 1
            j += 1
                    
        return s
            
    def closest_pair(self, 
                     distance: Callable[[int, int, int, int], float] = BaseClosestPair.distance
                    ) -> Tuple[int, int, float]:
        """
        Computes the minimum distance in O(n*log n) time.
        
        Examples:
        >>> x = [0, 3, 100]
        >>> y = [0, 4, 110]
        >>> fcp = FastClosestPair(x, y)
        >>> fcp.closest_pair()
        (0, 1, 5.0)
        """
        
        from math import inf
        
        def filter_points(s: List[int], d: float, x: int) -> List[int]:
            """Returns the list of point indexes that fall inside the [x-d, x+d] interval."""

            return [s[i] for i in range(len(s)) if abs(self._get_x(i, s) - x) <= d]

        def find_nearest_neighbor(i: int, s: List[int]) -> Tuple[float, int, int]:
            """
            Finds the minimum distance between the current point i and next 7 seven
            subsequent points by y coordinate.
            """

            curr_x = self._get_x(i, s)
            curr_y = self._get_y(i, s)
            d = inf
            min_idx = i

            for j in range(i + 1, min(len(s), i + 7 + 1)):
                curr_d = distance(curr_x, self._get_x(j, s), curr_y, self._get_y(j, s))
                if curr_d < d:
                    d = curr_d
                    min_idx = j
            return d, s[i], s[min_idx]

        def find_minimum_distance(s: List[int]) -> Tuple[int, int, float]:
            """Main driver function to find the closest pair."""

            if len(s) == 1:
                # We will treat the distance from a single point as infinite.
                return s[0], -1, inf
            if len(s) == 2:
                return s[0], s[1], distance(self._get_x(0, s), 
                                      self._get_x(1, s), 
                                      self._get_y(0, s), 
                                      self._get_y(1, s))
        
            # This is the median value of input array x in regard of s.
            median_x = self._selection(s.copy(), len(s) // 2)

            # Separate points around median.
            sl = []
            sr = []
            for i in range(len(s)):
                if self._get_x(i, s) <= median_x:
                    sl.append(s[i])
                else:
                    sr.append(s[i])
     
            # Find minimum distances in left and right groups.
            p_l, q_l, d_l = find_minimum_distance(sl)
            p_r, q_r, d_r = find_minimum_distance(sr)
            if d_l < d_r:
                p_min, q_min = p_l, q_l
                d = d_l
            else:
                p_min, q_min = p_r, q_r
                d = d_r
        
            # Merge left and right indices keeping their sorted order.
            sm = FastClosestPair._merge(sl, sr)
            
            # Find the minimum distance inside the middle strip.
            sf = filter_points(sm, d, median_x)
        
            # Find the final minimum distance amond three groups (left, middle, and right).
            d_m, p_m, q_m = min([find_nearest_neighbor(i, sf) for i in range(len(sf))])        
            if d_m < d:
                return p_m, q_m, d_m
            else:
                return p_min, q_min, d

        p, q, d = find_minimum_distance(list(range(len(self._y_prime))))
        # We need to map back the point indices into their original base.
        return self._y_prime[p], self._y_prime[q], d

if __name__ == "__main__":
    import doctest
    doctest.testmod()

