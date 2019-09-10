# -*- coding: utf-8 -*-
import numpy as np

def calculate_money_growth(p0, r, t):
    assert p0.size == t.size
    
    return p0 * np.exp(r * t)