#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def simple_recurrent_sequence(n, first, second, combine_fun):
    sequence = []
    current, next = first, second 
    for _ in range(n):
        current, next = next, combine_fun(current, next)
        sequence.append(current) 
    return sequence    

def fibonacci(n):
    return simple_recurrent_sequence(n, 0, 1, lambda x, y: x + y)