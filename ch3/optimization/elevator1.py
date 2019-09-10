def num_days(h, u, d):
    total_days = 1
    height_left = h

    while u < height_left:
        days = height_left // u
        total_days += days
        height_left -= days * (u - d)
    return total_days
