#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 11:56:04 2023

ilastik code v7

@author: Georgina
@modified by: Omar Valerio (2024)
"""
import os
import math
import numpy as np
import h5py
import tifffile as tff
import pprint as pp

import sys # used to get the python executable inside the ilastik-nmr container
import subprocess # used to run ilastik command on the host machine
import submitit # using submitit to parallelize ilastik pixel classification jobs using slurm
import ClearMap.GF_extras.cell_intensity_dask as ci # using the cell_intensity.py file from the ClearMap/GF_extras folder

#NOTE: only using the io module from ClearMap
#from ClearMap.Environment import *  
from ClearMap.IO import IO as io

import logging
import logstash

def setup_logging(logstash_host="localhost", logstash_port=5959, debug=False):
    
    if debug: # NOTE: useful to debug logging issues
        for logger_name in logging.Logger.manager.loggerDict.keys():
            print(f"logger name: {logger_name} has handlers: {logging.getLogger(logger_name).hasHandlers()}")
    
    # if this method is run inside a node started via submitit, use that as the logger name
    if 'SUBMITIT_EXECUTOR' in os.environ:
        logger = logging.getLogger("submitit") # using the root logger
    else :
        # using 'clearmap' as the logger name
        logger = logging.getLogger('clearmap')
        #logger.setLevel(logging.DEBUG)
    
    # avoid duplicating logger handlers
    if logger.hasHandlers() and logger.name != "submitit":
        return logger
    
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("{levelname} [{name}]: {asctime} - {message}", style="{")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # create logstash handler and set level to debug
    lh = logstash.LogstashHandler(logstash_host, logstash_port, version=1, message_type='logstash', tags={'application': 'ilastik-nmr'})
    lh.setLevel(logging.DEBUG)
    logger.addHandler(lh)
    
    return logger

# setup the logging
logstash_host = "somalogin01"
logstash_port = 5959
logger = setup_logging(logstash_host, logstash_port, debug=False)

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
    
    logger.info(pre + "Calculating chunk size for " + str(size) + " slices in range " + str(zr) + "!")
    logger.info(pre + " Processing Parameters: ")
    logger.info(pp.pformat(processing_parameter))
    
    # assert that chunkOverlap is less or equal than half the chunksize
    if chunkOverlap > chunksize / 2:
        logger.error("ChunkSize: chunkOverlap must be less or equal than half the chunksize!")
        raise RuntimeError("ChunkSize: chunkOverlap must be less or equal than half the chunksize!")
    
    nchunks = int(math.ceil((size - chunksize) / (1. * (chunksize - chunkOverlap)) + 1)); 
    if nchunks <= 0:
        nchunks = 1;   
    chunksize = (size + (nchunks-1) * chunkOverlap) / nchunks;
    
    if verbose:
        logger.debug( "ChunkSize: Estimated chunk size " + str(chunksize) + " in " + str(nchunks) + " chunks!");
    
    if nchunks == 1:
        return 1, [(0, chunksize)], [0, chunksize]
        
    #optimize number of chunks wrt to number of processors
    if chunkOptimization:
        np = nchunks % processes; #FIXME: this name shadows the numpy module import. 
        if np != 0:
            if chunkOptimizationSize == 'all': #FIXME: all is a special variable changed to 'all' to avoid confusion
                if np < processes / 2.0:
                    chunkOptimizationSize = True;
                else:
                    chunkOptimizationSize = False;
                    
            if verbose:
                logger.debug( "ChunkSize: Optimizing chunk size to fit number of processes!")
                
            if not chunkOptimizationSize:
                #try to deccrease chunksize / increase chunk number to fit distribution on processors
                nchunks = nchunks - np + processes;
                chunksize = (size + (nchunks-1) * chunkOverlap) / nchunks;
                
                if verbose:
                    logger.debug( "ChunkSize: Optimized chunk size decreased to " + str(chunksize) + " in " + str(nchunks) + " chunks!");
                    
            else:
                if nchunks != np:
                    #try to decrease chunk number to fit  processors
                    nchunks = nchunks - np;
                    chunksize = (size + (nchunks-1) * chunkOverlap) / nchunks;
                                  
                    if verbose:
                        logger.debug( "ChunkSize: Optimized chunk size increased to " + str(chunksize) + " in " + str(nchunks) + " chunks!");
                
                else:
                    if verbose:
                        logger.debug( "ChunkSize: Optimized chunk size unchanged " + str(chunksize) + " in " + str(nchunks) + " chunks!");
        
        else:
            if verbose:
                logger.debug( "ChunkSize: Optimized chunk size unchanged " + str(chunksize) + " in " + str(nchunks) + " chunks!");
    
    
    #increase overlap if chunks too small
    chunkSizeMin = min(chunkSizeMin, chunkOverlap);
    if chunksize < chunkSizeMin:
        if verbose: 
            logger.debug( "ChunkSize: Warning: optimal chunk size " + str(chunksize) + " smaller than minimum chunk size " + str(chunkSizeMin) + "!"); 
        chunksize = chunkSizeMin;
        chunkOverlap = math.ceil(chunksize - (size - chunksize) / (nchunks -1));
        
        if verbose:        
            logger.debug( "ChunkSize: Warning: setting chunk overlap to " + str(chunkOverlap) + "!");
           
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
        logger.debug("adjusted chunk size: " + str(chunksize) + " in " + str(nchunks) + " chunks!");
        logger.debug(f"zranges: {zranges}")
        logger.debug("ChunkSize: final chunks : " + str(zranges));
        logger.debug("ChunkSize: final centers: " + str(zcenters));
    
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
    

def run_command(cmd):
    cmd = ' '.join(cmd)
    logger.info(f'Ilastik running: {cmd}')

    # Use subprocess.Popen to execute the command and capture stdout and stderr in real-time
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Read and log the output as it is produced
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            logger.info(f'Ilastik command output: {output.strip()}')

    # Check if the process exited with an error
    if process.returncode != 0:
        # Read any errors from stderr
        error_output = process.stderr.read()
        logger.error(f'Error running ilastik command: {error_output}')
        raise subprocess.CalledProcessError(process.returncode, cmd, output=error_output)
    else:
        logger.info("Ilastik command completed successfully")

#------------------------------------------------------------------------------
def ilastik_initialise(ilastik_path):
    ilastikbin = os.path.join(ilastik_path, 'run_ilastik.sh');
    if os.path.exists(ilastikbin):
        logger.info( "Ilastik sucessfully initialized from path: %s" % ilastik_path);
        IlastikBinary = ilastikbin;
    return IlastikBinary;

#------------------------------------------------------------------------------
def run_ilastik(substack, i, res_dir, image_sequence, ilastik_parameter, processing_parameter):

    data = tff.imread(image_sequence.files[substack['z'][0]:substack['z'][1]])
    
    # DEBUG
    #import pickle
    #pickle.dump(data, open('data.pkl', 'wb'), protocol=4)
    #data = pickle.load(open('data.pkl', 'rb')) #FIXME: remove this line
    
    ## ilastik performance optimization: convert data into h5 file  ##
    chunk_name = 'chunk' + str(i) # name of the chunk file used also to name the output files of ilastik
    chunksize = substack['z'][1] - substack['z'][0]
    ilinp_h5 = io.join(res_dir,chunk_name +'.h5')
    with h5py.File(ilinp_h5, 'w') as f:
        f.create_dataset('exported_data', data=data, dtype='uint16', chunks=(min(64, chunksize), 64, 64))
    
    IlastikBinary = ilastik_initialise(ilastik_parameter["ilastikPath"])
    project = ilastik_parameter["classifier" ]
    
    # find number of cpu cores in the container
    import multiprocessing
    cpu_count = multiprocessing.cpu_count()
    logger.info(f'Number of CPU cores: {cpu_count}')
    
    # obtain available memory in the container
    available_memory = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024. ** 2)
    logger.info(f'Available memory: {available_memory} MB')
    
    # use 90% of the available node memory and round to the nearest integer
    available_memory = int(0.90 * available_memory)
    logger.info(f'Lazyflow memory (90% of available memory): {available_memory} MB')
    
    ilastik_cmd = [
        'LAZYFLOW_TOTAL_RAM_MB={available_memory}'.format(available_memory=available_memory),
        'LAZYFLOW_THREADS={cpu_count}'.format(cpu_count=cpu_count),
        IlastikBinary,
        '--headless',
        '--readonly',
        '--project=' + project,
        '--output_format=hdf5',
        '--output_filename_format={res_dir}/{chunk_name}_{{result_type}}.h5'.format(res_dir=res_dir, chunk_name=chunk_name),
        '{ilinp_h5}/exported_data'.format(ilinp_h5=ilinp_h5),
    ]
    
    # running the ilastik command using a subprocess
    run_command(ilastik_cmd)

    # once ilastik is done, used the output file to calculate cell centres and size
    ilastik_output_file = io.join(res_dir, chunk_name + '_Probabilities.h5')
    with h5py.File(ilastik_output_file, 'r') as f:
        import psutil
        # get the process from the PID
        ps = psutil.Process(os.getpid())
        logger.debug(f'[before loading sub_res] Memory usage (GB): {ps.memory_info().rss / 1024**3}')
        sub_res = np.array(f['exported_data'])
        logger.debug(f'[after loading sub_res] Memory usage (GB): {ps.memory_info().rss / 1024**3}')

        cents = ci.cell_maxima(sub_res, data, ilastik_parameter)
    
    return cents


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
            results_fin = (np.zeros((0,3)), np.zeros((0,2)));
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

def save_clearmap1_format(results_fin, sink):

    if isinstance(results_fin, tuple):
        np.savetxt(io.join(sink,'cell_maxima.csv'), results_fin[0], 
                   delimiter=',', newline='\n', fmt='%.5e')
        np.savetxt(io.join(sink,'cell_intensities.csv'), results_fin[1], 
                   delimiter=',', newline='\n', fmt='%.5e')
    
    else:
        np.savetxt(io.join(sink,'cell_maxima.csv'), results_fin, 
                   delimiter=',', newline='\n', fmt='%.5e')
        
    logger.info('csv files saved in clearmap1 format')   
        
#------------------------------------------------------------------------------

def save_clearmap2_format(results_fin, sink):
    # stack the centroids, size and maximal intensity
    results = np.hstack(results_fin)
    header = ['x','y','z','size','source']
    dtypes = [int, int, int, int, float]
    
    dt = {'names' : header, 'formats' : dtypes}
    # creating a data structure using the above data types
    cells = np.zeros(len(results), dtype=dt)
    for i,h in enumerate(header):
        cells[h] = results[:,i].astype(dtypes[i])
    
    io.write(io.join(sink,'cells_unfiltered.npy'), cells)
    
    logger.info('npy file saved in clearmap2 format')


#-----------------------------------------------------------------------------
def cell_detection(source, sink, ilastik_parameter, processing_parameter):
    
    fs, nz, zr = file_size(source) #fs = brain shape, nz = number of z slices
    logger.debug(f'fs (brain shape): {fs}, nz (num z slices): {nz}, zr: {zr}')

    nchunks, zranges, zcenters = calculateChunkSize(nz, zr, processing_parameter)
    
    subStacks, zs = create_substacks(nchunks, 
                                     zcenters, zranges, 
                                     source, 
                                     zr, x=all, y=all)
    
    source_oldstyle = source.split('<')[0] + '*' + source.split('>')[1] 
    image_sequence = tff.TiffSequence(source_oldstyle , pattern=r'_(\d+)|_Z(\d+)')

    #DEBUG: uncomment to process/run only the first substack
    #subStacks = subStacks[:1]
    
    processMethod = processing_parameter['processMethod']
    logger.info(f'processMethod: {processMethod}')
    
    if processMethod == 'sequential':
        cents = []
        for i in range(len(subStacks)):
            logger.info('Running ilastik on substack: ' + str(i) + '/' + str(len(subStacks)))
            cents.append(run_ilastik(subStacks[i], i, sink, image_sequence, ilastik_parameter, processing_parameter))
    else:
        
        # python executable inside ilastik-nmr container
        submitit_python = f"apptainer exec --env PYTHONPATH=~/clearmap-nmr --bind /gpfs:/gpfs /gpfs/soma_fs/scratch/containers/ilastik-nmr.sif {sys.executable}"
        logger.info(f'submitit python: {submitit_python}')

        logs_dir = io.join(sink, 'logs')
        logger.info(f'Logs dir: {logs_dir}')
        executor = submitit.SlurmExecutor(folder=logs_dir, python=submitit_python)

        executor.update_parameters(
            partition="CPU,GPU",
            time="4:00:00", # 4 hours (might be less time depending on the number of substacks and the number of cells in each substack)
            mem="350G",
            cpus_per_task=48,
            comment="ilastik-job",
            job_name="ilastik-job",
            array_parallelism=nchunks,
        )

        jobs = []
        with executor.batch():
            for i in range(len(subStacks)):
                logger.info('Submitting ilastik job on substack: ' + str(i) + '/' + str(len(subStacks)))
                job = executor.submit(run_ilastik, subStacks[i], i, sink, image_sequence, ilastik_parameter, processing_parameter)
                jobs.append(job)

        # Waiting for jobs to complete
        cents = [job.result() for job in jobs]
        logger.info("Jobs completed")

    logger.info('ilastik completed')

    # Separating the centroids from the intensities
    pointlist, intensities = cents_separate(cents)
    logger.info(f'pointlist: \n {pp.pformat(pointlist)}')
    logger.info(f'intensities: \n {pp.pformat(intensities)}')

    # save results of cells detection on the separate chunks
    np.save(io.join(sink,'chunked_pointlist.npy'), np.asarray(pointlist, dtype=object), allow_pickle=True)
    np.save(io.join(sink,'chunked_intensities.npy'), np.asarray(intensities, dtype=object), allow_pickle=True)
    np.save(io.join(sink,'substacks_info.npy'), np.asarray(subStacks, dtype=object), allow_pickle=True)
    
    results_fin = combine_substacks(pointlist, intensities, subStacks, fs)

    # write results in clearmap 1 format
    save_clearmap1_format(results_fin, sink)
  
    # write results in clearmap 2 format of filtered cells
    save_clearmap2_format(results_fin, sink)
    
    logger.info('ilastik cell detection completed')
    
    return results_fin



















            