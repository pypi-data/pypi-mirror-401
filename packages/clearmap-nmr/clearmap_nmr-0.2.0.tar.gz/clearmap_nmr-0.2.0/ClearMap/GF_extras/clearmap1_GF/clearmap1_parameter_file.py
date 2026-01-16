#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 2023

Parameter file for clearmap 1 type analysis

@author: Georgine
"""
###############################################################################
### Default parameter
###############################################################################




default_cell_detection_parameter = dict( 
  #flatfield
  correctIlluminationParameter = dict(flatfield     = None,
                                      background    = None,
                                      scaling       = 'mean',
                                      save          = None),
                       
  #background removal
  removeBackgroundParameter = dict(size = None,
                                   save = None),
  
  
  #difference of gaussians filter
  filterDoGParameter = dict(size = None,
                            sigma = None,
                            sigma2 = None,
                            save = None),
  
  #extended maxima detection
  findExtendedMaximaParameter = dict(hMax = None,
                                     size = 5,
                                     threshold = 0,
                                     save = None),

  #cell shape detection                                  
  detectCellShapeParameter = dict(threshold = 700,
                                  save = None),
  
  #cell intenisty detection                   
  findIntensityParameter = dict(method = 'Max',
                                size = (3,3,3)), 
)


#------------------------------------------------------------------------------

#cells filtering values
default_filtering_parameter = dict(threshold = (20, 900), 
				     row = (3,3))




#------------------------------------------------------------------------------
default_StackProcessingParameter  = dict(
  size_max = 100,
  size_min = 50,
  overlap = 32,
  axes = [2],
  optimization = True,
  optimization_fix = 'all',
  processes = 6,
  processMethod = 'parallel',
  min_cell_size = 10,
  verbose = True
)




#------------------------------------------------------------------------------
default_ilastik_path = '/home/nmr/ilastik-1.4.0-Linux';

default_ilastik_parameter = {
    "ilastikPath" : default_ilastik_path,
    "classifier" : None,
    "classindex" : 0,
    "save"       : None,      
    "verbose"    : True,
    "method" : 'Max',      
    "verbose": True} 
