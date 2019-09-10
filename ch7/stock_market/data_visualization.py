#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contains various utility visualization routines.

@author: Ervin Varga
"""
import matplotlib.pyplot as plt

def plot_time_series(ts, title_prefix, style='b-'):
    ax = ts.plot(figsize=(9, 8), lw=2, fontsize=12, style=style)
    ax.set_title('%s Over Time' % title_prefix, fontsize=19)
    ax.set_xlabel('Year', fontsize=15)
    plt.show()

def hist_time_series(ts, xlabel, bins):
    ax = ts.hist(figsize=(9, 8), xlabelsize=12, ylabelsize=12, bins=bins, grid=False)
    ax.set_title('Distribution of %s' % xlabel, fontsize=19)
    ax.set_xlabel(xlabel, fontsize=15)
    plt.show()
    
def scatter_time_series(ts, x, y):
    ax = ts.plot(x=x, y=y, figsize=(9, 8), kind='scatter', fontsize=12)
    ax.set_title('Auto-correlation Graph', fontsize=19)
    ax.set_xlabel(x, fontsize=15)
    ax.set_ylabel(y, fontsize=15)
    plt.show()
    
def heat_corr_plot(corr_matrix):
    import numpy as np
    import seaborn as sns
    
    mask = np.zeros_like(corr_matrix)
    mask[np.triu_indices_from(mask)] = True
    _, ax = plt.subplots(figsize=(9, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='gist_gray', fmt=".2f", lw=.5, mask=mask, ax=ax)
    plt.tight_layout()
    plt.show()