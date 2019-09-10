#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produces features and outputs based upon various criteria by simulating 
fake "real world" processes.

@author: Ervin Varga
"""
import numpy as np
import pandas as pd

def generate_base_features(sample_size):
    x_normal = np.random.normal(6, 9, sample_size)
    x_uniform = np.random.uniform(0, 1, sample_size)
    x_interacting = x_normal * x_uniform
    x_combined = 3.6 * x_normal + np.random.exponential(2/3, sample_size)
    x_collinear = 5.6 * x_combined
    
    features = {
        'x_normal': x_normal,
        'x_uniform': x_uniform,
        'x_interacting': x_interacting,
        'x_combined': x_combined,
        'x_collinear': x_collinear
    }
    return pd.DataFrame.from_dict(features)

def identity(x):
    return x

def generate_response(X, error_spread, beta, f=identity):
    error = np.random.normal(0, error_spread, (X.shape[0], 1))
    intercept = beta[0]
    coef = np.array(beta[1:]).reshape(X.shape[1], 1)
    return f(intercept + np.dot(X, coef)) + error