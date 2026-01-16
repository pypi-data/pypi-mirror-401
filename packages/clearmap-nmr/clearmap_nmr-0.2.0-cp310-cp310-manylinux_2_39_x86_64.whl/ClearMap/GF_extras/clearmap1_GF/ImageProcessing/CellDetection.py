# -*- coding: utf-8 -*-
"""
Cell Detection Module

This is the main routine to run the individual routines to detect cells om
volumetric image data.

ClearMap supports two predefined image processing pipelines which will extend
in the future:

================ ============================================================ ========================
Method           Description                                                  Reference
================ ============================================================ ========================
"SpotDetection"  uses predefined spot detection pipline                       :func:`~ClearMap.ImageProcessing.CellDetection.detectCells`
"Ilastik"        uses predefined pipline with cell classification via Ilastik :func:`~ClearMap.ImageProcessing.CellDetection.classifyCells`
function         a user defined function                                      NA
================ ============================================================ ========================

Example:

    >>> import ClearMap.IO as io  
    >>> import ClearMap.Settings as settings
    >>> from ClearMap.ImageProcessing.CellDetection import detectCells;
    >>> fn = os.path.join(settings.ClearMapPath, 'Test/Data/Synthetic/test_iDISCO_\d{3}.tif');
    >>> parameter = {"filterDoGParameter" : {"size": (5,5,5)}, "findExtendedMaximaParameter" : {"threshold" : 5}};
    >>> img = io.readData(fn);
    >>> img = img.astype('int16'); # converting data to smaller integer types can be more memory efficient!
    >>> res = detectCells(img, parameter);
    >>> print res[0].shape

See Also:
    :mod:`~ClearMap.ImageProcessing`

"""
#:copyright: Copyright 2015 by Christoph Kirst, The Rockefeller University, New York City
#:license: GNU, see LICENSE.txt for details.

import ClearMap.ImageProcessing.SpotDetection
import ClearMap.ImageProcessing.IlastikClassification

from ClearMap.ImageProcessing.StackProcessing import parallelProcessStack, sequentiallyProcessStack

from ClearMap.Utils.Timer import Timer
    

def detectCells(source, sink = None, processMethod = all, verbose = False, **parameter):
    """Detect cells in data using spotdetection methods
    
    This is a main script to start running the cell detection using clearmap1' spot detection.    
    
    Arguments:
        source (str or array): Image source
        sink (str or None): destination for the results

        processMethod (str or all): 'sequential' or 'parallel'. if all its choosen 
                                     automatically
        verbose (bool): print info
        **parameter (dict): parameter for the image procesing sub-routines
    
    Returns:
        
    """
    print(source)
    print(sink)
    print(processMethod)
    print(**parameter)
    
    
    timer = Timer();
        
    # run segmentation
#    detectCells = ClearMap.ImageProcessing.SpotDetection.detectSpots;



#    if processMethod == 'sequential':
#        result = sequentiallyProcessStack(source, sink = sink, function = detectCells, verbose = verbose, #**parameter);  
#    elif processMethod is all or processMethod == 'parallel':
#        result = parallelProcessStack(source, sink = sink, function = detectCells, verbose = verbose, #**parameter);  
#    else:
#        raise RuntimeError("detectCells: invalid processMethod %s" % str(processMethod));
#    
#    if verbose:
#        timer.printElapsedTime("Total Cell Detection");
    
    return #result;


