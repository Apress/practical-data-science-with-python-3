#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to preprocess financal data and prepare for further regression analysis.

@author: Ervin Varga
"""
import numpy as np
import pandas as pd

def read_daily_equity_data(file):
    stock_data = pd.read_csv(file, usecols=[0, 4, 5], skiprows=[1])
    stock_data['timestamp'] = pd.to_datetime(stock_data['timestamp'])
    stock_data.set_index('timestamp', inplace=True, verify_integrity=True)
    stock_data.sort_index(inplace=True)
    return stock_data

def compose_trends(ts):
    from sklearn.preprocessing import MinMaxScaler
    
    scaler = MinMaxScaler()
    scaled_ts = pd.DataFrame(scaler.fit_transform(ts), columns=ts.columns, index=ts.index)
    return pd.concat([scaled_ts['close'].rolling('365D').mean(), 
                      scaled_ts['volume'].rolling('365D').mean()], axis=1)

def create_log_returns(ts, halflife, normalize_close=True):
    ts['close_ret'] = np.log(ts['close']).diff()
    if normalize_close:
        ts['close_ret'] /= ts['close_ret'].ewm(halflife=halflife).std()
    ts['volume_ret'] = np.log(ts['volume']).diff()
    return ts.dropna()