#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def sort(data):
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i] > data[j]:
                data[i], data[j] = (data[j], data[i])
    return data