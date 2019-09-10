#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contains functions to recover parameters and demonstrate various effects 
pertaining to training, testing, and evaluation.

@author: Ervin Varga
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')

def train_model(model, X_train, y_train):
    model.fit(X_train, y_train)
    
def evaluate_model(model, X_test, y_test, plot_residuals=False, title=''):
    from sklearn.metrics import mean_squared_error, explained_variance_score

    y_pred = model.predict(X_test)

    if plot_residuals:
        _, ax = plt.subplots(figsize=(9, 9))
        ax.set_title('Residuals Plot - ' + title, fontsize=19)
        ax.set_xlabel('Predicted values', fontsize=15)
        ax.set_ylabel('Residuals', fontsize=15)
        sns.residplot(y_pred.squeeze(), y_test.squeeze(), 
                      lowess=True,
                      ax=ax,
                      scatter_kws={'alpha': 0.3}, 
                      line_kws={'color': 'black', 'lw': 2, 'ls': '--'})
    
    metrics = {
        'explained_variance': explained_variance_score(y_test, y_pred),
        'mse': mean_squared_error(y_test, y_pred) 
    }
    return metrics

def make_poly_pipeline(model, degree):
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import PolynomialFeatures
    
    return make_pipeline(PolynomialFeatures(degree=degree, include_bias=False), model)

def print_parameters(linear_model, metrics):
    print('Intercept: %.3f' % linear_model.intercept_)
    print('Coefficients: \n', linear_model.coef_)
    print('Explained variance score: %.3f' % metrics['explained_variance'])
    print("Mean squared error: %.3f" % metrics['mse'])

def plot_mse(model, X, y, title, error_spread):
    def collect_mse():
        from sklearn.model_selection import train_test_split
        from sklearn.model_selection import cross_val_score
    
        metrics_all = []
        for train_size_pct in range(10, 110, 10):
            X_train, X_test, y_train, y_test = \
                train_test_split(X, y, shuffle=False, train_size=train_size_pct / 100)
            metrics_current = dict()
            metrics_current['percent_train'] = train_size_pct
            train_model(model, X_train, y_train)
            metrics_train = evaluate_model(model, X_train, y_train)
            metrics_current['Training score'] = metrics_train['mse']
            metrics_cv = cross_val_score(
                model, 
                X_train, y_train, 
                scoring='neg_mean_squared_error', 
                cv=10)
            metrics_current['CV score'] = -metrics_cv.mean()
            if X_test.shape[0] > 0:
                metrics_test = evaluate_model(model, X_test, y_test)
                metrics_current['Testing score'] = metrics_test['mse']
            else:
                metrics_current['Testing score'] = np.NaN                
            metrics_all.append(metrics_current)
        return pd.DataFrame.from_records(metrics_all)        

    import matplotlib.ticker as mtick
    
    df = collect_mse()
    error_variance = error_spread**2
    ax = df.plot(
        x='percent_train',
        title=title,
        kind='line',
        xticks=range(10, 110, 10),
        sort_columns=True,
        style=['b+--', 'ro-', 'gx:'],
        markersize=10.0,
        grid=False,
        figsize=(8, 6),
        lw=2)
    ax.set_xlabel('Training set size', fontsize=15)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    y_min, y_max = ax.get_ylim()
    # FIX ME: See Exercise 3!
    ax.set_ylim(max(0, y_min), min(2 * error_variance, y_max))
    ax.set_ylabel('MSE', fontsize=15)
    ax.title.set_size(19)
    
    # Draw and annotate the minimum MSE.
    ax.axhline(error_variance, color='g', ls='--', lw=1)
    ax.annotate(
        'Inherent error level', 
        xy=(15, error_variance), 
        textcoords='offset pixels',
        xytext=(10, 80),
        arrowprops=dict(facecolor='black', width=1, shrink=0.05))

def explain_sse(slope, intercept, x, y):
    # Configure the diagram.
    _, ax = plt.subplots(figsize=(7, 9))
    ax.set_xlabel('x', fontsize=15)
    ax.set_ylabel('y', fontsize=15)
    ax.set_title(r'$SSE = \sum_{i=1}^n (y_i - \hat{y}_i)^2$', fontsize=19)
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction='out', length=6, width=2, colors='black')

    # Show x-y pairs.
    ax.scatter(x, y, alpha=0.5, marker='x')

    # Draw the regression line.
    xlims = np.array([np.min(x), np.max(x)])
    ax.plot(xlims, slope * xlims + intercept, lw=2, color='b')

    # Draw the error terms.
    for x_i, y_i in zip(x, y):
        ax.plot([x_i, x_i], [y_i, slope * x_i + intercept], color='r', lw=2, ls='--')