#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to download all data, summarize a single data file chunk-by-chunk and 
traverse the data folder to process all files.

@author: Ervin Varga
"""

import requests, zipfile, io, shutil

unpackedFolder = '/dds_datasets/'
unpackedZipFile = 'dds_ch2_nyt.zip'

def retrieve(sourceFile, destinationFolder):
    def cleanup():
        try:
            shutil.rmtree(destinationFolder + unpackedFolder)
        except OSError as e:
            print("Folder: %s, Error: %s" % (e.filename, e.strerror))                

    r = requests.get(sourceFile)
    assert r.status_code == requests.codes.ok

    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(destinationFolder)
    
    # The top archive contains another ZIP file with our data.
    z = zipfile.ZipFile(destinationFolder + unpackedFolder + unpackedZipFile)
    z.extractall(destinationFolder)
    
    cleanup()

import pandas as pd
import numpy as np

def summarize(data_file, chunksize):
    def q25(x):
        return x.quantile(0.25)

    def q75(x):
        return x.quantile(0.75)

    # Read and parse the CSV data file chunk-by-chunk.
    nyt_data = pd.DataFrame()
    for chunk_df in pd.read_csv(
            data_file, 
            dtype={'Gender': 'category'},
            chunksize=chunksize):
    
        # Segment users into age groups.    
        chunk_df['Age_Group'] = pd.cut(
                chunk_df['Age'], 
                bins=[-1, 0, 17, 24, 34, 44, 54, 64, 120], 
                labels=["Unknown", 
                        "1-17", 
                        "18-24", 
                        "25-34", 
                        "35-44", 
                        "45-54", 
                        "55-64", 
                        "65+"])

        # Create the click through rate feature.    
        chunk_df['CTR'] = chunk_df['Clicks'] / chunk_df['Impressions']
        chunk_df.dropna(inplace=True)
        chunk_df.drop((chunk_df['Clicks'] > chunk_df['Impressions']).nonzero()[0], 
                      inplace=True)
        
        # Append chunk to the main data frame.
        nyt_data = nyt_data.append(
                chunk_df[['Age_Group', 'Gender', 'Clicks', 'CTR']], 
                ignore_index=True)

    # Make final description of data.
    compressed_nyt_data = \
        nyt_data.groupby(by=['Age_Group', 'Gender'])[['CTR', 'Clicks']] \
                .agg([np.mean, np.std, np.max, q25, np.median, q75, np.sum])
    return compressed_nyt_data

import pathlib

def traverse(sourceFolder, collect, chunksize=10000):
    def get_file_number(data_file):
        return int(data_file.name[3:-4]) - 1
        
    for data_file in pathlib.Path(sourceFolder).glob('nyt*.csv'):
        collect(summarize(data_file.absolute(), chunksize), 
                get_file_number(data_file))