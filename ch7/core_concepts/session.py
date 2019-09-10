#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contains functions that depict steps to reconstruct different world parameters 
from observations using various noise levels.

@author: Ervin Varga
"""
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from data_generator import *
from observer import *

def set_session_seed(seed):
    np.random.seed(seed)    # Enables perfect reproduction of published results.

def demo_metrics_and_mse():
    set_session_seed(100)
    X = generate_base_features(1000)[['x_normal']]
    for noise_level in [0, 2, 15]:
        y = generate_response(X, noise_level, [-1.5, 4.1])
        model = LinearRegression()
        train_model(model, X, y)
        metrics = evaluate_model(model, X, y)

        print('\nIteration with noise level: %d' % noise_level)
        print_parameters(model, metrics)

        # Visualize the regression line and error terms.        
        if noise_level == 15:
            slope = model.coef_[0][0]
            intercept = model.intercept_
            explain_sse(slope, intercept, X[:15].values, y[:15])

def demo_overfitting():
    def visualize_overfitting():
        train_model(optimal_model, X, y)        
        train_model(complex_model, X, y)        
        
        _, ax = plt.subplots(figsize=(9, 7))
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.grid(False)

        X_test = np.linspace(0, 1.2, 100)
        plt.plot(X_test, np.sin(2 * np.pi * X_test), label='True function')
        plt.plot(
            X_test, 
            optimal_model.predict(X_test[:, np.newaxis]), 
            label='Optimal model',
            ls='-.')
        plt.plot(
            X_test, 
            complex_model.predict(X_test[:, np.newaxis]), 
            label='Complex model',
            ls='--',
            lw=2,
            color='red')
        plt.scatter(X, y, alpha=0.2, edgecolor='b', s=20, label='Training Samples')
        ax.fill_between(X_test, -2, 2, where=X_test > 1, hatch='/', alpha=0.05, color='black')
        plt.xlabel('x', fontsize=15)
        plt.ylabel('y', fontsize=15)
        plt.xlim((0, 1.2))
        plt.ylim((-2, 2))
        plt.legend(loc='upper left')
        plt.title('Visualization of How Overfitting Occurs', fontsize=19)
        plt.show()        
    
    set_session_seed(172)
    X = generate_base_features(120)[['x_uniform']]
    y = generate_response(X, 0.1, [0, 2 * np.pi], f=np.sin)
    
    optimal_model = make_poly_pipeline(LinearRegression(), 5)    
    plot_mse(optimal_model, X, y, 'Optimal Model', 0.1)
    complex_model = make_poly_pipeline(LinearRegression(), 35)
    plot_mse(complex_model, X, y, 'Complex Model', 0.1)
    
    visualize_overfitting()
    
def demo_underfitting():
    set_session_seed(15)
    X = generate_base_features(200)
    X_interacting = X[['x_interacting']]
    y = generate_response(X_interacting, 2, [1.7, -4.3])
    plot_mse(LinearRegression(), X_interacting, y, 'Optimal Model', 2)
    X_weak = X[['x_normal', 'x_uniform']]
    plot_mse(LinearRegression(), X_weak, y, 'Weak Model', 2)
    
def demo_collinearity():
    set_session_seed(10)
    X = generate_base_features(1000)
    X_world = X[['x_normal', 'x_combined']]
    y = generate_response(X_world, 2, [1.1, -2.3, 3.1])
    
    model = LinearRegression()
    # Showcase the first assumed model.
    train_model(model, X_world, y)
    metrics = evaluate_model(model, X_world, y)
    print('\nDumping stats for model 1')
    print_parameters(model, metrics)

    # Showcase the second assumed model.
    X_extended_world = X[['x_normal', 'x_combined', 'x_collinear']]
    train_model(model, X_extended_world, y)
    metrics = evaluate_model(model, X_extended_world, y)
    print('\nDumping stats for model 2')
    print_parameters(model, metrics)
    
    # Produce a scatter matrix plot.
    df = X
    df.columns = ['x' + str(i + 1) for i in range(len(df.columns))]
    df['y'] = y
    pd.plotting.scatter_matrix(df, alpha=0.2, figsize=(10, 10), diagonal='kde')
    
def demo_residuals():
    def plot_regression_line(x, y, case_num):
        _, ax = plt.subplots(figsize=(9, 9))
        ax.set_title('Regression Plot - Case ' + str(case_num), fontsize=19)
        ax.set_xlabel('x', fontsize=15)
        ax.set_ylabel('y', fontsize=15)
        sns.regplot(x.squeeze(), y.squeeze(),
                    ci=None,
                    ax=ax,
                    scatter_kws={'alpha': 0.3}, 
                    line_kws={'color': 'green', 'lw': 3})
    
    set_session_seed(100)
    X = generate_base_features(1000)
    X1 = X[['x_normal']]
    y1 = generate_response(X1, 0.04, [1.2, 0.00003])
    X2 = X1**2
    y2 = generate_response(X2, 0.04, [1.2, 0.00003])
    
    model = LinearRegression()
    # Showcase the first world with a linearly assumed model.
    plot_regression_line(X1, y1, 1)
    train_model(model, X1, y1)
    metrics = evaluate_model(model, X1, y1, True, 'Case 1')
    print('\nDumping stats for case 1')
    print_parameters(model, metrics)

    # Showcase the second world with a linearly assumed model.
    plot_regression_line(X1, y2, 2)
    train_model(model, X1, y2)
    metrics = evaluate_model(model, X1, y2, True, 'Case 2')
    print('\nDumping stats for case 2')
    print_parameters(model, metrics)

def demo_regularization():
    from sklearn.linear_model import RidgeCV
    
    set_session_seed(172)
    X = generate_base_features(120)[['x_uniform']]
    y = generate_response(X, 0.1, [0, 2 * np.pi], f=np.sin)
    
    regularized_model = make_poly_pipeline(
            RidgeCV(alphas=[1e-3, 1e-2, 1e-1, 1, 5, 10, 20], gcv_mode='auto'),
            35)
    plot_mse(regularized_model, X, y, 'Regularized Model', 0.1)