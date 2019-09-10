#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main driver file that connects all pieces together.

@author: Ervin Varga
"""
from data_preprocessing import *
from data_visualization import *

# Data Acquisition stage.
stock_data = read_daily_equity_data('daily_AAPL.csv')

# Data Preprocessing stage.
stock_data = create_log_returns(stock_data, 23)

plot_time_series(stock_data['close'], 'AAPL Closing Levels')
plot_time_series(stock_data['close'].rolling('365D').mean(), 'AAPL Closing Trend')
plot_time_series(compose_trends(stock_data), 'AAPL Closing & Volume Trends', ['b-', 'g--'])

# To produce the non-normalized price log returns plot you must call 
# the create_log_returns function with normalize_close=False. Try this as an
# additional exercise.
plot_time_series(stock_data['close_ret'], 'AAPL Volatility-Norm. Price Log Returns')
plot_time_series(stock_data['volume_ret'], 'AAPL Volume Log Returns')

hist_time_series(stock_data['close_ret'], 'Daily Stock Log Returns', 50)
hist_time_series(stock_data['volume_ret'], 'Daily Volume Log Returns', 50)

# Feature Engineering stage.
from feature_engineering import *

report_auto_correlation(stock_data)
corr_matrix = create_features(stock_data)
heat_corr_plot(corr_matrix)

# Regression Implementation stage.
from pyspark.sql import SparkSession

from streaming_regression import *

sparkSession = SparkSession.builder \
                           .master("local[4]") \
                           .appName("Streaming Regression Case Study")\
                           .getOrCreate()
fit_and_predict(sparkSession, stock_data)