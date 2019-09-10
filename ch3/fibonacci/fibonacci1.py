#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def fibonacci(n): 
    sequence = []
    current, next = 0, 1 
    for _ in range(n):
        current, next = next, current + next
        sequence.append(current) 
    return sequence