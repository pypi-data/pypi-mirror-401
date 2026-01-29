#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 16:32:27 2023

stats codes for clearmap2 data

@author: Georgina
"""

import ClearMap.Analysis.Statistics.GroupStatistics as st
import ClearMap.IO.IO as io
import numpy as np
from scipy import stats
import tifffile as tf




def read_data(groupa, groupb):

    groupa_data = st.read_group(groupa, combine=True).transpose(3,2,1,0);
    groupb_data = st.read_group(groupb, combine=True).transpose(3,2,1,0);
    
    return groupa_data, groupb_data;



def t_test_vox(groupa_data, groupb_data, p_cutoff, remove_nan):

    tvals = np.zeros(groupa_data.shape[:3])
    pvals = np.zeros(groupa_data.shape[:3])
    psign = np.zeros(groupa_data.shape[:3])
    pvalscol = np.zeros((groupa_data.shape[0],groupa_data.shape[1],groupa_data.shape[2],3))
    
    
    for i in range(len(groupa_data)):
        for l in range(len(groupa_data[i])):
            tvals[i][l], pvals[i][l] = stats.ttest_ind(groupa_data[i][l], groupb_data[i][l], axis=1, equal_var=True);
            psign[i][l] = np.sign(tvals[i][l])
            if remove_nan == True: 
               pi = np.isnan(pvals[i][l]);
               pvals[i][l][pi] = 1.0;
               tvals[i][l][pi] = 0; 
            pvals[i][l][pvals[i][l] > p_cutoff]  = p_cutoff;
            pvalscol[i][l] = st.color_p_values(pvals[i][l], psign[i][l], positive = [255,0,0], negative = [0,255,0])
    
    return pvals, pvalscol, psign



def mult_comp(pvals, psign, method):
    pvals1 = np.reshape(np.asarray(pvals), pvals.size);
    
    if method.lower() in ['bh', 'fdr']:
      pvals_sorted_ids = np.argsort(pvals1);
      pvals_sorted = pvals1[pvals_sorted_ids]
      sorted_ids_inv = pvals_sorted_ids.argsort()
    
      n = len(pvals1);
      bhfactor = np.arange(1,n+1)/float(n);
    
      pvals_corrected_raw = pvals_sorted / bhfactor;
      pvals_corrected = np.minimum.accumulate(pvals_corrected_raw[::-1])[::-1]
      pvals_corrected[pvals_corrected>1] = 1;
    
      pvals_corrected[sorted_ids_inv];
    
    elif method.lower() in ['b', 'fwer']:
      n = len(pvals1);        
      
      pvals_corrected = n * pvals1;
      pvals_corrected[pvals_corrected>1] = 1;\
      
      pvals_corrected;
      
    pvalscol_correctd = st.color_p_values(pvals_corrected, np.reshape(psign, pvals.size), positive = [255,0,0], negative = [0,255,0])
    
    pvalscol_correctd  = np.reshape(pvalscol_correctd , [pvals.shape[0],pvals.shape[1],pvals.shape[2],3]);

    return pvalscol_correctd




def save_pval_col(pvalcol, result_type, directory):
    
    if result_type =='counts':
        save_file = io.join(directory,'coloured_pval_stack_counts.tif')
    else:
        save_file = io.join(directory,'coloured_pval_stack_intensities.tif')
    
    
    pval_col = pvalcol.astype('uint16')
    
    with tf.TiffWriter(save_file) as tif:
        options = dict(
            photometric='rgb'
            )
        tif.write(pval_col,**options)
            
            
    return
        



            
def run_stats(analysis_on, groupa, groupb, remove_nan, p_cutoff, directory, multiple_corrections, multiple_corrections_method ):

    if 'counts' in analysis_on:
        groupa_counts = [io.join(i, 'density_counts.tif') for i in groupa]
        groupb_counts = [io.join(i, 'density_counts.tif') for i in groupb]
        
        groupa_counts_data, groupb_counts_data = read_data(groupa_counts, groupb_counts)
        
        pval, pval_col, psign = t_test_vox(groupa_counts_data, groupb_counts_data, p_cutoff, remove_nan)
        
        if multiple_corrections == True:
            pval_col = mult_comp(pval, psign, multiple_corrections_method)
        
        save_pval_col(pval_col, 'counts', directory)

    if 'intensities' in analysis_on:
        groupa_intensities = [io.join(i, 'density_intensities.tif') for i in groupa]
        groupb_intensities = [io.join(i, 'density_intensities.tif') for i in groupb]

        groupa_intensities_data, groupb_intensities_data = read_data(groupa_intensities, groupb_intensities)
        
        pval, pval_col, psign = t_test_vox(groupa_intensities_data, groupb_intensities_data, p_cutoff, remove_nan)        

        if multiple_corrections == True:
            pval_col = mult_comp(pval, psign, multiple_corrections_method)
        
        save_pval_col(pval_col, 'intensities', directory)
        
    return print('completed')
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    