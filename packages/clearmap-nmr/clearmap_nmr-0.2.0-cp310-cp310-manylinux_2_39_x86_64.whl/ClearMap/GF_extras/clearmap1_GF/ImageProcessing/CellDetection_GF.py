#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cell Detection Module addapted by Georgy

"""

from ClearMap.Utils.Timer import Timer
import ClearMap.GF_extras.clearmap1_GF.ImageProcessing.SpotDetection as spotd

from ClearMap.GF_extras.clearmap1_GF.ImageProcessing.spot_detection_processing_GF import spot_detection

def detectCells(source, sink, StackProcessingParameter, SpotDetectionParameter, cFosFileRange,FilteringParameter):
    verbose = StackProcessingParameter['verbose']
    processMethod = StackProcessingParameter['processMethod'].lower()
    
    timer = Timer();


    if processMethod == 'sequential' or processMethod == 'parallel':
         result = spot_detection(source, sink,
                                            StackProcessingParameter, SpotDetectionParameter, 
                                            cFosFileRange,FilteringParameter);  
                                               
    else:
        raise RuntimeError("detectCells: invalid processMethod %s" % str(processMethod));
    
    if verbose:
        timer.print_elapsed_time("Total Cell Detection");
    
    return #result;


