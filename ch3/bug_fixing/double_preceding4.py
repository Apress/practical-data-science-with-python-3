#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def double_preceding(x: np.ndarray) -> None:
    """Transforms the array by setting x[i] = 2 * x[i-1] and x[0] = 0.

    >>> x = np.array([5, 10, 15])
    >>> double_preceding(x)
    >>> x
    array([ 0, 10, 20])
    """

    if x.size != 0:
        x[:-x.size:-1] = 2 * x[-2::-1]
        x[0] = 0
