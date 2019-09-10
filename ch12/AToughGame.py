#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution for the AToughGame Topcoder problem."""
class AToughGame:
    def expectedGain(self, prob, value):
        """
        Examples:
        >>> EPS = 10 ** -6
        >>> game = AToughGame()
        >>> abs(game.expectedGain((1000,500), (3,4)) - 10.0) < EPS
        True
        >>> abs(game.expectedGain((1000,1), (3,4)) - 3003.9999999999977) < EPS
        True
        >>> abs(game.expectedGain((500,500,500,500,500), (1,2,3,4,5)) - 16.626830517153095)  < EPS
        True
        >>> abs(game.expectedGain((250,750), (1000,1)) - 1067.6666666666667) < EPS
        True
        >>> abs(game.expectedGain((916,932,927,988,958,996,944,968,917,939,960,965,960,998,920,990,915,972,995,916,902, 968,970,962,922,959,994,915,996,996,994,986,945,947,912,946,972,951,973,965,921,910, 938,975,942,950,900,983,960,998,982,980,902,974,952,938,900,962,920,931,964,974,953, 995,946,946,903,921,923,985,919,996,930,915,991,967,996,911,999,936,1000,962,970,929, 966,960,930,920,958,926,983), (583,428,396,17,163,815,31,536,175,165,532,781,29,963,331,987,599,497,380,180,780,25, 931,607,784,613,468,140,488,604,401,912,204,785,697,173,451,849,714,914,650,652,338, 336,177,147,22,652,901,548,370,9,118,487,779,567,818,440,10,868,316,666,690,714,623, 269,501,649,324,773,173,54,391,745,504,578,81,627,319,301,16,899,658,586,604,83,520, 81,181,943,157)) - 54204.93356505282) < EPS
        True
        """

        # Combines two levels into a single aggregate. This implements the safe move
        # of this greedy algorithm.
        def combine(level0, level1):
            p0, v0, p1, v1 = level0[0], level0[1], level1[0], level1[1]
            q0, q1 = 1 - p0, 1 - p1
            return p0 * p1, v1 + v0 * p1 * (p0 + q0 / p1) * (1 - p0 * q1) ** -2

        from functools import reduce
        return reduce(combine, zip(map(lambda p: p / 1000, prob), value))[1]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
