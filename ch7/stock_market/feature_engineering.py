#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to help perform feature engineering.

@author: Ervin Varga
"""
from data_visualization import *

def report_auto_correlation(ts, periods=5):
    for column in filter(lambda str: str.endswith('_ret'), ts.columns):
        future_column = 'future_' + column
        ts[future_column] = ts[column].shift(-periods).rolling(periods).sum()
        current_column = 'current_' + column
        ts[current_column] = ts[column].rolling(periods).sum()
        
        print(ts[[current_column, future_column]].corr())
        scatter_time_series(ts, current_column, future_column)
        
def create_features(ts):
    from talib import SMA, RSI, OBV
    
    target = 'future_close_ret'
    features = ['current_close_ret', 'current_volume_ret']

    for n in [14, 25, 50, 100]:
        ts['sma_' + str(n)] = SMA(ts['close'].values, timeperiod=n) / ts['close']
        ts['rsi_' + str(n)] = RSI(ts['close'].values, timeperiod=n)
    ts['obv'] = OBV(ts['close'].values, ts['volume'].values.astype('float64'))
    
    ts.drop(['close', 'volume', 'close_ret', 'volume_ret', 'future_volume_ret'],
            axis='columns',
            inplace=True)
    ts.dropna(inplace=True)
    return ts.corr()