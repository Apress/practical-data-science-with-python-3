#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def puzzle1(n):
    p = 0; w = 1; s = n
    
    while w <= n:
        w <<= 2

    while w != 1:
        w >>= 2
        f = p + w
        p >>= 1

        if s >= f:
            p += w
            s -= f
    return p
