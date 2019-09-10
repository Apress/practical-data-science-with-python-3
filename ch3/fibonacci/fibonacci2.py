#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def fibonacci(n, f0=0, f1=1): 
    sequence = []
    current, next = f0, f1 
    for _ in range(n):
        current, next = next, current + next
        sequence.append(current) 
    return sequence