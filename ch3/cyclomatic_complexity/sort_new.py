#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def sort(data):
    for i in range(len(data)):
        for j in range(len(data)):
            avg = (data[i] + data[j]) / 2.0
            diff = abs(data[i] - avg)
            data[i] = avg - diff
            data[j] = avg + diff
    return data
