def num_days(h, u, d):
    total_days = 1
    curr_height = 0
    
    while h - curr_height > u:
        curr_height += u - d
        total_days += 1
    return total_days