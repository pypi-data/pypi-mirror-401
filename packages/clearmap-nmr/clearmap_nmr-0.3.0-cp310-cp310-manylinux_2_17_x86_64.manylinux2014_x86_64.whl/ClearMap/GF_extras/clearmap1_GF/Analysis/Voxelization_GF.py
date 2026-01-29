#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 2023

Converts point data into voxel image data for visulaization and analysis

@author: 
"""

import numpy
import math
import tifffile as tiff

# NOTE: Please comment this lines before packaging. It leads to race conditions if enabled in HPC
# NOTE: pyximport is unnecessary when package is properly installed via setup.py
# import pyximport;
# pyximport.install(setup_args={"include_dirs":numpy.get_include()}, reload_support=True)

import ClearMap.IO.IO as io
import ClearMap.GF_extras.clearmap1_GF.Analysis.VoxelizationCode as vox

def writeData(filename, data):
    """Write image data to tif file
    
    Arguments:
        filename (str): file name 
        data (array): image data
    
    Returns:
        str: tif file name
    """
    
    d = len(data.shape);
    
    if d == 2:
        #tiff.imsave(filename, data);
        tiff.imsave(filename, data.transpose([1,0]));
    elif d == 3:   
        #tiff.imsave(filename, data.transpose([2,0,1]));
        tiff.imsave(filename, data.transpose([2,1,0]));
    elif d == 4:        
        #tiffile (z,y,x,c)
        #t = tiff.TiffWriter(filename, bigtiff = True);
        #t.save(data.transpose([2,0,1,3]), photometric = 'minisblack',  planarconfig = 'contig');
        #t.save(data.transpose([2,1,0,3]), photometric = 'minisblack',  planarconfig = 'contig')
        #t.close();    
        tiff.imsave(filename, data.transpose([2,1,0,3]), photometric = 'minisblack',  planarconfig = 'contig', bigtiff = True);
    else:
        raise RuntimeError('writing multiple channel data to tif not supported!');
    
    return filename;




def voxelize(source, sink = None, shape = None, weights = None,  method = 'Spherical', radius = (5,5,5)):
    """Converts a list of points into an volumetric image array
    
    Arguments:
        points (array): point data array
        dataSize (tuple): size of final image
        sink (str, array or None): the location to write or return the resulting voxelization image, if None return array
        voxelizeParameter (dict):
            ========== ==================== ===========================================================
            Name       Type                 Descritption
            ========== ==================== ===========================================================
            *method*   (str or None)        method for voxelization: 'Spherical', 'Rectangular' or 'Pixel'
            *size*     (tuple)              size parameter for the voxelization
            *weights*  (array or None)      weights for each point, None is uniform weights                          
            ========== ==================== ===========================================================      
    Returns:
        (array): volumetric data of smeared out points
    """
    #points = io.read(source);
    points = source;

    dataSize = shape;
    
    # if dataSize is None:
    #     dataSize = tuple(int(math.ceil(points[:,i].max())) for i in range(points.shape[1]));
    # elif isinstance(dataSize, str):
    #     dataSize = io.dataSize(dataSize);
    
    #points = io.readPoints(points);

    print(radius)
    print(dataSize)        
    if method.lower() == 'spherical':
        if weights is None:
            data = vox.voxelizeSphere(points.astype('float'), dataSize[0], dataSize[1], dataSize[2], radius[0], radius[1], radius[2]);
        else:
            data = vox.voxelizeSphereWithWeights(points.astype('float'), dataSize[0], dataSize[1], dataSize[2], radius[0], radius[1], radius[2], weights);
           
    elif method.lower() == 'rectangular':
        if weights is None:
            data = vox.voxelizeRectangle(points.astype('float'), dataSize[0], dataSize[1], dataSize[2], radius[0], radius[1], radius[2]);
        else:
            data = vox.voxelizeRectangleWithWeights(points.astype('float'), dataSize[0], dataSize[1], dataSize[2], radius[0], radius[1], radius[2], weights);
    
    elif method.lower() == 'pixel':
        data = voxelizePixel(points.astype('int'), dataSize, weights);
        
    else:
        raise RuntimeError('voxelize: mode: %s not supported!' % method);
    
    return writeData(sink, data);


def voxelizePixel(points,  dataSize = None, weights = None):
    """Mark pixels/voxels of each point in an image array
    
    Arguments:
        points (array): point data array
        dataSize (tuple or None): size of the final output data, if None size is determined by maximal point coordinates
        weights (array or None): weights for each points, if None weights are all 1s.
    
    Returns:
        (array): volumetric data with with points marked in voxels
    """
    
    # if dataSize is None:
    #     dataSize = tuple(int(math.ceil(points[:,i].max())) for i in range(points.shape[1]));
    # elif isinstance(dataSize, str):
    #     dataSize = io.dataSize(dataSize);
    
    if weights is None:
        vox = numpy.zeros(dataSize, dtype=numpy.int16);
        for i in range(points.shape[0]):
            if points[i,0] > 0 and points[i,0] < dataSize[0] and points[i,1] > 0 and points[i,1] < dataSize[1] and points[i,2] > 0 and points[i,2] < dataSize[2]:
                vox[points[i,0], points[i,1], points[i,2]] += 1;
    else:
        vox = numpy.zeros(dataSize, dtype=weights.dtype);
        for i in range(points.shape[0]):
            if points[i,0] > 0 and points[i,0] < dataSize[0] and points[i,1] > 0 and points[i,1] < dataSize[1] and points[i,2] > 0 and points[i,2] < dataSize[2]:
                vox[points[i,0], points[i,1], points[i,2]] += weights[i];
    
    return  vox;


    