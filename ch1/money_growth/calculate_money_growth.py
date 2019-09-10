# -*- coding: utf-8 -*-
import math

def calculate_money_growth(p0, r, t):
    # List of final amounts.
    p = []
    for i in range(len(p0)):
        p.append(p0[i] * math.exp(r * t[i]))
    return p