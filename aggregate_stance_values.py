#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 15:47:58 2021

@author: arushi
"""

import numpy as np
import pandas as pd
import sys
import math
import glob 
import re 
from tqdm import tqdm

# Read stance file here
#start_row = int(sys.argv[1]) #(included) 
#end_row = int(sys.argv[2]) #(included)

# start_row = 19500001
# end_row = 19550000

# start_sheet_name = 50000*(start_row//50000)+1 #for csv_file variable
# end_sheet_name = 50000*(math.ceil(end_row/50000)) #for csv_file variable

#fileName = 'processed_data_stance_'+str(start_sheet_name)+'_'+str(end_sheet_name)+'.csv'

# PUT PATH HERE
#all_files = glob.glob("C:\\Users\\Akshay Jadiya\\Documents\\GT\\6. Courses\\Sem 1\\CSE 6242\\new\\*.csv")

if(len(sys.argv)<1):
    print("usage: python aggregate_stance_values.py")
    exit()

directory = './data/processed_data_stance' #sys.argv[1] #(included) 

all_files = glob.glob(directory+"/*.csv")

for fileName in tqdm(all_files):
    
    print("Processing file:", fileName)

    file_name_list = re.split('[_.]+',fileName)
    op_file_name = '_'.join([file_name_list[i] for i in [-2,-3]])
    
    df = pd.read_csv(fileName, header = None , sep=',' , names=[num for num in range(0,33)], engine='c')
    
    try:
        df = pd.read_csv(fileName, header = None , sep=',' , names=[num for num in range(0,33)], engine='c')
    except:
        print("Error with", str(fileName), "- skipping file")
        continue
    
    #df = pd.read_csv(fileName, header = None , sep=',' , names=[num for num in range(0,33)],engine='c',on_bad_lines = 'skip')
    
    # Select relevant columns and rename
    data_sel_col = df.iloc[:,[1,6,27,28,29,30,31,32]]
    colnames = ['Date','Party','Biden Favor',	'Biden Against','Biden Neutral','Trump Favor','Trump Against','Trump Neutral']
    data_sel_col.columns = colnames

    # OPTIONAL - To check missing values
    data_sel_col = data_sel_col.dropna(how='any',axis=0) 
    data_sel_col.shape

    df = data_sel_col.copy()

    # Separate columns for Biden and Trump
    biden_col = [col for col in df.columns if col.startswith('Biden')]
    biden_col_aug = ['Date','Party'] + biden_col

    trump_col = [col for col in df.columns if col.startswith('Trump')]
    trump_col_aug = ['Date','Party'] + trump_col

    # Find all rows where the max tweet is neutral
    df_republicans = df[(df['Party'] == 'Republicans') | (df['Party'] == 'BothParty')][trump_col_aug].copy()
    df_democrats = df[(df['Party'] == 'Democrats') | (df['Party'] == 'BothParty')][biden_col_aug].copy()

    def mod_max_trump(row):
        if(row['Trump Favor'] > -1*row['Trump Against']):
            return row['Trump Favor']
        else:
            return row['Trump Against']

    def mod_max_biden(row):
        if(row['Biden Favor'] > -1*row['Biden Against']):
            return row['Biden Favor']
        else:
            return row['Biden Against']


    # For Republicans
    df_republicans['max_val'] = df_republicans[trump_col].apply(max,axis=1)
    df_republicans_filt = df_republicans[df_republicans['max_val'] != df_republicans['Trump Neutral']].copy()
    df_republicans_filt['Trump Against'] = -1*df_republicans_filt['Trump Against']
    df_republicans_filt['stance'] = df_republicans_filt[trump_col].apply(mod_max_trump , axis = 1)
    df_republicans_filt['Date'] = pd.to_datetime(df_republicans_filt['Date']).dt.date
    
    # df_republicans_filt[['Date', 'Time', 'AM/PM']] = df_republicans_filt['Date'].str.split(' ', expand=True)
    df_republicans_filt[['Date','stance']].groupby('Date',as_index=False).mean()

    rep_output = df_republicans_filt[['Date','stance']].groupby('Date',as_index=False).agg(['sum','count'])
    output_rep = './data/processed_data_stance_aggregated/stance_republican_'+op_file_name+'.csv'
    rep_output.to_csv(output_rep, header = False)

    # For Democrats
    df_democrats['max_val'] = df_democrats[biden_col].apply(max,axis=1)
    df_democrats_filt = df_democrats[df_democrats['max_val'] != df_democrats['Biden Neutral']].copy()
    df_democrats_filt['Biden Against'] = -1*df_democrats_filt['Biden Against']
    df_democrats_filt['stance'] = df_democrats_filt[biden_col].apply(mod_max_biden , axis = 1)
    df_democrats_filt['Date'] = pd.to_datetime(df_democrats_filt['Date']).dt.date
    # df_democrats_filt[['Date', 'Time', 'AM/PM']] = df_democrats_filt['Date'].str.split(' ', expand=True)
    df_democrats_filt[['Date','stance']].groupby('Date',as_index=False).agg(['sum','count'])

    dem_output = df_democrats_filt[['Date','stance']].groupby('Date',as_index=False).agg(['sum','count'])
    output_dem = './data/processed_data_stance_aggregated/stance_democrat_'+op_file_name+'.csv'
    dem_output.to_csv(output_dem, header = False)