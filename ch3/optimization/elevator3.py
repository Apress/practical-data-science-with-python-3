def num_days(h, u, d):
    import math
    
    height_left_until_last_day = h - u
    daily_progress = u - d
    return 1 + math.ceil(height_left_until_last_day / daily_progress)