from functools import lru_cache

@lru_cache(maxsize=32)
def _partial_num_days(height_left, u, d):
    total_days = 1

    while u < height_left:
        days = height_left // u
        total_days += days
        height_left -= days * (u - d)
    return total_days

H_LIMIT = 1000000

def num_days(h, u, d):
    if h > H_LIMIT:
        days = 2 * (num_days(h // 2, u, d) - 1)
        height_left = h - days * (u - d)
        return days + _partial_num_days(height_left, u, d)
    else:
        return _partial_num_days(h, u, d)