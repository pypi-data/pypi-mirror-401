#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 11:56:04 2023

ilastik code v6

@author: Georgina
"""
import os

import ClearMap.ImageProcessing.Ilastik_GF.IlastikClassification as I_GF
ilastik_function = I_GF.classifyCells
import ClearMap.IO.IO as io
import ClearMap.IO.TIF as tf
import os
import math
from ClearMap.Utils.Timer import Timer;
from ClearMap.Environment import *  

import ClearMap.ImageProcessing.Ilastik_GF.IO_GF as io_GF
from ClearMap.ImageProcessing.Ilastik_GF.ProcessWriter import ProcessWriter  
import ClearMap.ImageProcessing.Ilastik_GF.IlastikClassification as IC

import tifffile as tff  
import tempfile  
import numpy as np
import ClearMap.ImageProcessing.Ilastik_GF.IlastikClassification as IC
from ClearMap.ImageProcessing.Ilastik_GF.ParameterTools import getParameter, writeParameter
import h5py
import scipy.ndimage.measurements as sm;


def ilastik_initialise(ilastik_path):
    ilastikbin = os.path.join(ilastik_path, 'run_ilastik.sh');
    if os.path.exists(ilastikbin):
        print( "Ilastik sucessfully initialized from path: %s" % ilastik_path);
        IlastikBinary = ilastikbin;
        Initialized = True;
    return IlastikBinary





def file_size(source):
    fs = io.as_source(source).shape;
    ns = fs[2];
    zr = (0, ns);
    nz = ns;
    return (fs, nz, zr)










#calculate optimal chunk sizes
def calculateChunkSize(nz, zr, processing_parameter):
    verbose = True
    pre = "ChunkSize: ";
      
    #calcualte chunk sizes
    chunksize = processing_parameter['size_max'];
    chunkSizeMin = processing_parameter['size_min'];
    size = nz
    chunkOverlap = processing_parameter['overlap']
    chunkOptimization = processing_parameter['optimization']
    processes = processing_parameter['processes']
    chunkOptimizationSize = processing_parameter['optimization_fix']
    
    nchunks = int(math.ceil((size - chunksize) / (1. * (chunksize - chunkOverlap)) + 1)); 
    if nchunks <= 0:
        nchunks = 1;   
    chunksize = (size + (nchunks-1) * chunkOverlap) / nchunks;
    
    if verbose:
        print( pre + "Estimated chunk size " + str(chunksize) + " in " + str(nchunks) + " chunks!");
    
    if nchunks == 1:
        return 1, [(0, chunksize)], [0, chunksize]
        
    #optimize number of chunks wrt to number of processors
    if chunkOptimization:
        np = nchunks % processes;
        if np != 0:
            if chunkOptimizationSize == all:
                if np < processes / 2.0:
                    chunkOptimizationSize = True;
                else:
                    chunkOptimizationSize = False;
                    
            if verbose:
                print( pre + "Optimizing chunk size to fit number of processes!")
                
            if not chunkOptimizationSize:
                #try to deccrease chunksize / increase chunk number to fit distribution on processors
                nchunks = nchunks - np + processes;
                chunksize = (size + (nchunks-1) * chunkOverlap) / nchunks;
                
                if verbose:
                    print( pre + "Optimized chunk size decreased to " + str(chunksize) + " in " + str(nchunks) + " chunks!");
                    
            else:
                if nchunks != np:
                    #try to decrease chunk number to fit  processors
                    nchunks = nchunks - np;
                    chunksize = (size + (nchunks-1) * chunkOverlap) / nchunks;
                                  
                    if verbose:
                        print( pre + "Optimized chunk size increased to " + str(chunksize) + " in " + str(nchunks) + " chunks!");
                
                else:
                    if verbose:
                        print( pre + "Optimized chunk size unchanged " + str(chunksize) + " in " + str(nchunks) + " chunks!");
        
        else:
            if verbose:
                print( pre + "Optimized chunk size unchanged " + str(chunksize) + " in " + str(nchunks) + " chunks!");
    
    
    #increase overlap if chunks too small
    chunkSizeMin = min(chunkSizeMin, chunkOverlap);
    if chunksize < chunkSizeMin:
        if verbose: 
            print( pre + "Warning: optimal chunk size " + str(chunksize) + " smaller than minimum chunk size " + str(chunkSizeMin) + "!"); 
        chunksize = chunkSizeMin;
        chunkOverlap = math.ceil(chunksize - (size - chunksize) / (nchunks -1));
        
        if verbose:        
            print( pre + "Warning: setting chunk overlap to " + str(chunkOverlap) + "!");
           
    #calucalte actual chunk sizes
    chunksizerest = chunksize;
    chunksize = int(math.floor(chunksize));
    chunksizerest = chunksizerest - chunksize;
    
    zranges = [(0, chunksize)];
    zcenters = [0];
    n = 1;
    csr = chunksizerest;
    zhi = chunksize;
    
    while (n < nchunks):
        n += 1;
        
        zhiold = zhi;
        zlo = zhi - chunkOverlap;
        zhi = zlo + chunksize;
        
        csr += chunksizerest;
        if csr >= 1:
            csr = csr - 1;
            zhi += 1;
        
        if n == nchunks:        
            zhi = size;
        
        zranges.append((int(zlo), int(zhi)));
        zcenters.append((zhiold - zlo) / 2. + zlo); 
        
    zcenters.append(size);
    
    if verbose:    
        print (zranges)
        print (pre + "final chunks : " + str(zranges));
        print (pre + "final centers: " + str(zcenters));
    
    #adjust for the zrange
    zcenters = [c + zr[0] for c in zcenters];
    zranges = [(zc[0] + zr[0], zc[1] + zr[0]) for zc in zranges];
    
    return (nchunks, zranges, zcenters)




def create_substacks(nchunks, zcenters, zranges, source, x, y, zr):     
    subStacks = [];
    indexlo = zr[0];
    
    for i in range(nchunks):
        
        indexhi = int(round(zcenters[i+1]));
        if indexhi > zr[1] or i == nchunks - 1:
            indexhi = zr[1];
        
        zs = zranges[i][1] - zranges[i][0];
        
        subStacks.append({"stackId" : i, "nStacks" : nchunks, 
                          "source" : source, "x" : x, "y" : y, "z" : zranges[i], 
                          "zCenters" : (zcenters[i], zcenters[i+1]),
                          "zCenterIndices" : (indexlo, indexhi),
                          "zSubStackCenterIndices" : (indexlo - zranges[i][0], zs - (zranges[i][1] - indexhi))});
        
        indexlo = indexhi; # + 1;
        
    return subStacks, zs; 
    





def run_ilastik(substacki, i, parent_dir, image_sequence, ilastik_project_file ):

    data = tff.imread(image_sequence.files[substacki['z'][0]:substacki['z'][1]])
    tff.imwrite(io.join(parent_dir,'chunk' + str(i) +'.tif'),  data)
    
    ilinp = io.join(parent_dir,'chunk' + str(i) +'.tif')   ;   
    
    IlastikBinary = ilastik_initialise(ilastik_path)
    project = ilastik_project_file
    args = '--project=' + project + ' ' + ilinp;
    cmd = IlastikBinary + ' --headless ' + args;
    print( 'Ilastik: running: %s' % cmd);

    os.system(cmd);

    f = h5py.File(io.join(parent_dir, 'chunk' + str(i) +'_Probabilities.h5') , "r");
    
    dsname = "/exported_data";
    dset = f.get(dsname);
    sub_res = np.array(dset);
    f.close();
    os.remove(io.join(parent_dir,'chunk' + str(i) +'.tif') )
    
    return (sub_res)





def cell_maxima_shape(sub_resi, substacki, classindex, method):    
    imgmax = np.argmax(sub_resi.transpose(2,1,0,3), axis = -1);
  
    
    imgmax = imgmax == classindex; 
    imgshape, nlab = sm.label(imgmax);
    
    img = tff.imread(image_sequence.files[substacki['z'][0]:substacki['z'][1]]).transpose(2,1,0)
    
    imglab, nlab = sm.label(imgmax);  
    
         
    if nlab > 0:
        centers = np.array(sm.center_of_mass(img, imglab, index = np.arange(1, nlab)));    
        
    else:
        centers = np.zeros((0,3));
    
        
    #find cell sizes
    maxLabel = centers.shape[0]
    if maxLabel is None:
        maxLabel = int(imglab.max());
    
    csize = sm.sum(np.ones(imglab.shape, dtype = bool), labels = imglab, 
                  index = np.arange(1, maxLabel + 1));
    
    idz = csize > 0; #remove cells of size 0
        

    #find cell intensities    
    if method.lower() == 'sum':
        cintensity  = sm.sum(img, labels = imglab, index = np.arange(1, maxLabel + 1));
    elif method.lower() == 'mean':
        cintensity  = sm.mean(img, labels = imglab, index = np.arange(1, maxLabel + 1));
    elif method.lower() == 'max':
        cintensity  = sm.maximum(img, labels = imglab, index = np.arange(1, maxLabel + 1));
    elif method.lower() == 'min':
        cintensity  = sm.minimum(img, labels = imglab, index = np.arange(1, maxLabel + 1));
    else:
        raise RuntimeError('cellIntensity: unkown method %s!' % method);
    
    return ( [centers[idz], np.vstack((cintensity[idz], csize[idz])).transpose()] ); 


def cents_separate(cents):
    nchunks = len(cents);
    pointlist = [cents[i][0] for i in range(nchunks)];
    intensities = [cents[i][1] for i in range(nchunks)]; 
    return pointlist, intensities 




def toDataRange(size, r = all):


    if r is all:
        return (0,size);
    
    if isinstance(r, int) or isinstance(r, float):
        r = (r, r +1);
      
    if r[0] is all:
        r = (0, r[1]);
    if r[0] < 0:
        if -r[0] > size:
            r = (0, r[1]);
        else:
            r = (size + r[0], r[1]);
    if r[0] > size:
        r = (size, r[1]);
        
    if r[1] is all:
        r = (r[0], size);
    if r[1] < 0:
        if -r[1] > size:
            r = (r[0], 0);
        else:
            r = (r[0], size + r[1]);
    if r[1] > size:
        r = (r[0], size);
    
    if r[0] > r[1]:
        r = (r[0], r[0]);
    
    return r;

def pointShiftFromRange(dataSize, x = all, y = all, z = all, **args):   
    
    d = len(dataSize);
    rr = [];
    if d > 0:
        rr.append(toDataRange(dataSize[0], r = x));
    if d > 1:
        rr.append(toDataRange(dataSize[1], r = y));
    if d > 2:
        rr.append(toDataRange(dataSize[2], r = z));
    if d > 3 or d < 1:
        raise RuntimeError('shiftFromRange: dimension %d to big' % d);
    
    return [r[0] for r in rr];



def combine_substacks(pointlist, intensities, subStacks, fs):
    results = [];
    resultsi = [];
    for i in range(nchunks):
        cts = pointlist[i];
        cti = intensities[i];
    
        if cts.size > 0:
            cts[:,2] += subStacks[i]["z"][0];
            iid = np.logical_and(subStacks[i]["zCenters"][0] <= cts[:,2] , cts[:,2] < subStacks[i]["zCenters"][1]);
            cts = cts[iid,:];
            results.append(cts);
            if not cti is None:
                cti = cti[iid];
                resultsi.append(cti);
            
    if results == []:
        if not intensities is None:
            results_fin = (np.zeros((0,3)), np.zeros((0)));
        else:
            results_fin =  np.zeros((0,3))
    else:
        points = np.concatenate(results);
        
        if shiftPoints:
            points = points + pointShiftFromRange(fs, x = subStacks[0]["x"], y = subStacks[0]["y"], z = 0);
        else:
            points = points - pointShiftFromRange(fs, x = 0, y = 0, z = subStacks[0]["z"]); #absolute offset is added initially via zranges !
            
        if intensities is None:
            results_fin =  points;
        else:
            results_fin =  (points, np.flip(np.concatenate(resultsi), axis=1));
    
    return results_fin





def save_clearmap1_format(parent_dir, result_fin):

    if isinstance(results_fin, tuple):
        np.savetxt(io.join(directory1,'cell_maxima.csv'), results_fin[0], delimiter=',', newline='\n', fmt='%.5e')
        np.savetxt(io.join(directory1,'cell_intensities.csv'), results_fin[1], delimiter=',', newline='\n', fmt='%.5e')
    
    else:
        np.savetxt(io.join(directory1,'cell_maxima.csv'), results_fin, delimiter=',', newline='\n', fmt='%.5e')
        
    return print('csv files saved in clearmap1 format')   
        

def save_clearmap2_format(parent_dir, result_fin, sink):
    results = np.hstack(results_fin)
    header = ['x','y','z','size','source'];
    dtypes = [int, int, int, int, float];
    
    dt = {'names' : header, 'formats' : dtypes};
    cells = np.zeros(len(results), dtype=dt);
    for i,h in enumerate(header):
      cells[h] = results[:,i];
    
    sink = ws.filename('cells', postfix='filtered') 
    io.write(sink, cells);
    return print('npy file saved in clearmap1 format')  












            