#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def puzzle2(bytes):
    f = [0] * 255
    s = k = 0
    
    for b in bytes:
        f[b] += 1
    
    s += f[k]
    k += 1
    while s < len(bytes) / 2:
        s += f[k]
        k += 1
    return k
