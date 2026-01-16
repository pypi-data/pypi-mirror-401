#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 2023

clearmap1 sequentially process spot detection

@author: Georgy
"""
import os
import math
import numpy as np
import h5py
import scipy.ndimage.measurements as sm;
import tifffile as tff  
from ClearMap.Utils.Timer import Timer


from ClearMap.Environment import *  
import ClearMap.GF_extras.clearmap1_GF.ImageProcessing.SpotDetection as spotd

from ClearMap.GF_extras.clearmap1_GF.ImageProcessing.IlluminationCorrection import correctIllumination
from ClearMap.GF_extras.clearmap1_GF.ImageProcessing.BackgroundRemoval import removeBackground
from ClearMap.GF_extras.clearmap1_GF.ImageProcessing.Filter.DoGFilter import filterDoG
from ClearMap.GF_extras.clearmap1_GF.ImageProcessing.MaximaDetection import findExtendedMaxima
from ClearMap.GF_extras.clearmap1_GF.ImageProcessing.MaximaDetection import findPixelCoordinates
from ClearMap.GF_extras.clearmap1_GF.ImageProcessing.MaximaDetection import findIntensity
from ClearMap.GF_extras.clearmap1_GF.ImageProcessing.MaximaDetection import findCenterOfMaxima
from ClearMap.GF_extras.clearmap1_GF.ImageProcessing.CellSizeDetection import detectCellShape, findCellSize, findCellIntensity

from multiprocessing import Pool

#------------------------------------------------------------------------------
def file_size(source):
    fs = io.as_source(source).shape;
    ns = fs[2];
    zr = (0, ns);
    nz = ns;
    return (fs, nz, zr)



#------------------------------------------------------------------------------

#calculate optimal chunk sizes
def calculateChunkSize(nz, zr, processing_parameter):
    
    pre = "ChunkSize: ";
      
    #calcualte chunk sizes
    chunksize = processing_parameter['size_max'];
    chunkSizeMin = processing_parameter['size_min'];
    size = nz
    chunkOverlap = processing_parameter['overlap']
    chunkOptimization = processing_parameter['optimization']
    processes = processing_parameter['processes']
    chunkOptimizationSize = processing_parameter['optimization_fix']
    verbose = processing_parameter['verbose']
    
    
    
    nchunks = int(math.ceil((size - chunksize) / (1. * (chunksize - chunkOverlap)) + 1)); 
    if nchunks <= 0:
        nchunks = 1;   
    chunksize = (size + (nchunks-1) * chunkOverlap) / nchunks;
    
    if verbose:
        print( "ChunkSize: Estimated chunk size " + str(chunksize) + " in " + str(nchunks) + " chunks!");
    
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
                print( "ChunkSize: Optimizing chunk size to fit number of processes!")
                
            if not chunkOptimizationSize:
                #try to deccrease chunksize / increase chunk number to fit distribution on processors
                nchunks = nchunks - np + processes;
                chunksize = (size + (nchunks-1) * chunkOverlap) / nchunks;
                
                if verbose:
                    print( "ChunkSize: Optimized chunk size decreased to " + str(chunksize) + " in " + str(nchunks) + " chunks!");
                    
            else:
                if nchunks != np:
                    #try to decrease chunk number to fit  processors
                    nchunks = nchunks - np;
                    chunksize = (size + (nchunks-1) * chunkOverlap) / nchunks;
                                  
                    if verbose:
                        print( "ChunkSize: Optimized chunk size increased to " + str(chunksize) + " in " + str(nchunks) + " chunks!");
                
                else:
                    if verbose:
                        print( "ChunkSize: Optimized chunk size unchanged " + str(chunksize) + " in " + str(nchunks) + " chunks!");
        
        else:
            if verbose:
                print( "ChunkSize: Optimized chunk size unchanged " + str(chunksize) + " in " + str(nchunks) + " chunks!");
    
    
    #increase overlap if chunks too small
    chunkSizeMin = min(chunkSizeMin, chunkOverlap);
    if chunksize < chunkSizeMin:
        if verbose: 
            print( "ChunkSize: Warning: optimal chunk size " + str(chunksize) + " smaller than minimum chunk size " + str(chunkSizeMin) + "!"); 
        chunksize = chunkSizeMin;
        chunkOverlap = math.ceil(chunksize - (size - chunksize) / (nchunks -1));
        
        if verbose:        
            print( "ChunkSize: Warning: setting chunk overlap to " + str(chunkOverlap) + "!");
           
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
        print ("ChunkSize: final chunks : " + str(zranges));
        print ("ChunkSize: final centers: " + str(zcenters));
    
    #adjust for the zrange
    zcenters = [c + zr[0] for c in zcenters];
    zranges = [(zc[0] + zr[0], zc[1] + zr[0]) for zc in zranges];
    
    return nchunks, zranges, zcenters;

#------------------------------------------------------------------------------
def create_substacks(nchunks, zcenters, zranges, source, zr, x, y):     
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


#------------------------------------------------------------------------------

def getParameter(parameter, key, default = None):

    if not isinstance(parameter, dict):
        return default;
    
    if key in parameter.keys():
        return parameter[key];
    else:
        return default;
    
    
#------------------------------------------------------------------------------

def run_spotdetection(substacki, image_sequence, SpotDetectionParameter, verbose):
    timer = Timer();  
    
    correctIlluminationParameter = SpotDetectionParameter["correctIlluminationParameter"];
    removeBackgroundParameter = SpotDetectionParameter["removeBackgroundParameter"];
    filterDoGParameter = SpotDetectionParameter["filterDoGParameter"];
    findExtendedMaximaParameter = SpotDetectionParameter["findExtendedMaximaParameter"];
    hMax = findExtendedMaximaParameter["hMax"];
    detectCellShapeParameter = SpotDetectionParameter["detectCellShapeParameter"];
    cellShapeThreshold = detectCellShapeParameter["threshold"];
    findIntensityParameter = SpotDetectionParameter["findIntensityParameter"];
    
    #img = io.readData(sub["source"], x = sub["x"], y = sub["y"], z = sub["z"]);
    data = tff.imread(image_sequence.files[substacki['z'][0]:substacki['z'][1]])

    timer.reset();

    # correct illumination
    img1 = data.copy();
    img1 = correctIllumination(img1, correctIlluminationParameter = correctIlluminationParameter, 
                               verbose = verbose, out = None)   


    # background subtraction in each slice
    img2 = removeBackground(img1, removeBackgroundParameter = removeBackgroundParameter, 
                            verbose = verbose, out = None)   
    
    #DoG filter
    dogSize = getParameter(filterDoGParameter, "size", None);
    img3 = filterDoG(img2, filterDoGParameter = filterDoGParameter, 
                     verbose = verbose, out = None);
    
    # extended maxima
    imgmax = findExtendedMaxima(img3, findExtendedMaximaParameter = findExtendedMaximaParameter, 
                                verbose = verbose, out = None);
    
    #center of maxima
    if not hMax is None:
        centers = findCenterOfMaxima(img, imgmax, verbose = verbose, out = None);
    else:
        centers = findPixelCoordinates(imgmax, verbose = verbose, out = None);
    
    #cell size detection
    if not cellShapeThreshold is None:
        
        # cell shape via watershed
        imgshape = detectCellShape(img2, centers, detectCellShapeParameter = detectCellShapeParameter, verbose = verbose, out = None);
        
        #size of cells        
        csize = findCellSize(imgshape, maxLabel = centers.shape[0], out = None);
        
        #intensity of cells
        cintensity = findCellIntensity(data, imgshape,  findCellIntensityParameter = findIntensityParameter, 
                                       maxLabel = centers.shape[0], verbose = verbose, out = None);

        #intensity of cells in background image
        cintensity2 = findCellIntensity(img2, imgshape,  findCellIntensityParameter = findIntensityParameter,
                                        maxLabel = centers.shape[0], verbose = verbose, out = None);
    
        #intensity of cells in dog filtered image
        if dogSize is None:
            cintensity3 = cintensity2;
        else:
            cintensity3 = findCellIntensity(img3, imgshape,  maxLabel = centers.shape[0], verbose = verbose, out = None);
        
        if verbose:
            timer.print_elapsed_time(head = 'Spot Detection' + '\n');
        
        #remove cell;s of size 0
        idz = csize > 0;
                       
        return ( [centers[idz], np.vstack((cintensity[idz], cintensity3[idz], cintensity2[idz], csize[idz])).transpose()]);        
        
    
    else:
        findIntensityParameter = detectSpotsParameter['findIntensityParameter']
        #intensity of cells
        cintensity = findIntensity(data, centers, findIntensityParameter, verbose = verbose, out = None);

        #intensity of cells in background image
        cintensity2 = findIntensity(img2, centers, findIntensityParameter, verbose = verbose, out = None);
    
        #intensity of cells in dog filtered image
        if dogSize is None:
            cintensity3 = cintensity2;
        else:
            cintensity3 = findIntensity(img3, centers, verbose = verbose, out = None);

        if verbose:
            timer.print_elapsed_time(head = 'Spot Detection' + '\n');
    
        return ( [centers, np.vstack((cintensity, cintensity3, cintensity2)).transpose()]);
        
    
#------------------------------------------------------------------------------

def cents_separate(cents):
    nchunks = len(cents);
    pointlist = [cents[i][0] for i in range(nchunks)];
    intensities = [cents[i][1] for i in range(nchunks)]; 
    return pointlist, intensities; 


#------------------------------------------------------------------------------

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


#------------------------------------------------------------------------------


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


#------------------------------------------------------------------------------

def combine_substacks(pointlist, intensities, subStacks, fs, shiftPoints = True):
    results = [];
    resultsi = [];
    for i in range(len(subStacks)):
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
    
    return results_fin;



#-----------------------------------------------------------------------------

def save_clearmap1_format(res_dir, results_fin):

    if isinstance(results_fin, tuple):
        np.savetxt(io.join(res_dir,'cell_maxima.csv'), results_fin[0], 
                   delimiter=',', newline='\n', fmt='%.5e')
        np.savetxt(io.join(res_dir,'cell_intensities.csv'), results_fin[1], 
                   delimiter=',', newline='\n', fmt='%.5e')
    
    else:
        np.savetxt(io.join(res_dir,'cell_maxima.csv'), results_fin, 
                   delimiter=',', newline='\n', fmt='%.5e')
        
    return print('csv files saved in clearmap1 format')   
        
#------------------------------------------------------------------------------

def save_clearmap2_format(results_fin, sink):
    results = np.hstack(results_fin)
    header = ['x','y','z','size','source'];
    dtypes = [int, int, int, int, float];
    
    dt = {'names' : header, 'formats' : dtypes};
    cells = np.zeros(len(results), dtype=dt);
    for i,h in enumerate(header):
      cells[h] = results[:,i];
    

    io.write(io.join(sink,'cells_filtered.npy') , cells);
    
    return print('npy file saved in clearmap2 format')  



#-------------------------------------------------------------------------------

def sequential_spot_detection(source, sink, StackProcessingParameter, SpotDetectionParameter, cFosFileRange):

    verbose = StackProcessingParameter['verbose']
    
    fs, nz, zr = file_size(source) #fs = brain shape, nz = number of z slices

    nchunks, zranges, zcenters = calculateChunkSize(nz, zr, StackProcessingParameter)
    
    subStacks, zs = create_substacks(nchunks, 
                                     zcenters, zranges, 
                                     source, 
                                     zr, x=all, y=all) 
    
    #chunk_list = create_chunk_list(subStacks, ilastik_parameter)
    
    
    source_oldstyle = source.split('<')[0] + '*' + source.split('>')[1] 
    image_sequence = tff.TiffSequence(source_oldstyle , pattern=r'_(\d+)')


    # process in parallel
    pool = Pool(processes = StackProcessingParameter['processes']);    

    argdata = [];
    for i in range(len(SubStacks)):
        argdata.append((subStacks[i], sink, image_sequence));    

    results = pool.map(run_spotdetection, argdata);

 

    
    results = [];
    for i in range(len(subStacks)):
        print('Running spot detection on substack: ' + str(i) + '/' + str(len(subStacks)))
        
        results.append(run_spotdetection(subStacks[i],
                                      image_sequence,
                                      SpotDetectionParameter,
                                      verbose))


    

    pointlist, intensities = cents_separate(results)
    
    results_fin = combine_substacks(pointlist, intensities, subStacks, fs)

  
    # write results in clearmap 1 format
    save_clearmap1_format(sink, results_fin)
  
    # write results in clearmap 2 format of filtered cells
    save_clearmap2_format(results_fin, sink)
    
    return print('clearmap1 cell detection completed')
    









