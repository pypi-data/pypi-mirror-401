#NOTE: Accelerating the cell_intensity function using dask-image
#      The function is called from run_ilastik.py
import os
import psutil # for memory usage

import numpy as np
import multiprocessing as mp
# this environment variable is used to set the number of threads used by numexpr (dask-image)
os.environ["NUMEXPR_MAX_THREADS"] = str(mp.cpu_count())

# h5py is used to read the ilastik output
import h5py

# dask-image is used to compute the center of mass and other cell measurements
import dask
import dask.array as da
import dask_image.ndmeasure as dndi
from dask.diagnostics import ProgressBar

# dask-image is not fully compatible with scikit-image, hence the following import is required
# REF: https://github.com/scikit-image/scikit-image/issues/3846
from skimage import morphology

# import computen node properties
# import compute_node_properties as cnp

import logging
import logstash

def setup_logging(logstash_host="localhost", logstash_port=5959, debug=False):
    
    if debug: # NOTE: useful to debug logging issues
        for logger_name in logging.Logger.manager.loggerDict.keys():
            print(f"[cell_intensity_dask] logger name: {logger_name} has handlers: {logging.getLogger(logger_name).hasHandlers()}")
    
    # if this method is run inside a node started via submitit, use that as the logger name
    if 'SUBMITIT_EXECUTOR' in os.environ:
        logger = logging.getLogger("submitit") # using the root logger
        logger.setLevel(logging.DEBUG)
    else :
        # using 'clearmap' as the logger name
        logger = logging.getLogger('clearmap')
        logger.setLevel(logging.DEBUG)

    # debugging the logger name, handlers and propagation
    if debug:
        print(f"[cell_intensity_dask] logger name: {logger.name} has handlers: {logger.hasHandlers()} propagates: {logger.propagate}")
        if logger.hasHandlers():
            for handler in logger.handlers:
                print(f"[cell_intensity_dask] handler name: {handler.name}, handler level: {handler.level}")
    
    # avoid duplicating any existing logger handlers
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

# using a CustomProgressBar that shows progress in 5% increments
class CustomProgressBar(ProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_percentage = 0
        
    def _draw_bar(self, frac, elapsed):
        percentage = int(frac * 100)
        if percentage % 5 == 0 and percentage != self._last_percentage:
            self._last_percentage = percentage
            super()._draw_bar(frac, elapsed)

def cell_maxima(sub_res, data, ilastik_parameter, min_cell_size=5, use_dtype=np.uint16):
    
    # setup the logging
    logstash_host = "somalogin01"
    logstash_port = 5959
    logger = setup_logging(logstash_host, logstash_port, debug=True)

    # Logging the process memory usage after each operation
    ps = psutil.Process(os.getpid())
    
    # Log the number of CPU cores that Dask is using
    num_cores = dask.config.get('num_workers', default=os.cpu_count())
    logger.info(f'Number of CPU cores Dask is using: {num_cores}')
    
    # If the DASK_SCHEDULER_ADDRESS is set in the environment use that as the scheduler
    dask_scheduler_address = os.getenv('DASK_SCHEDULER_ADDRESS')
    if dask_scheduler_address is None:
        scheduler = 'threads'
        logger.warning(f'DASK_SCHEDULER_ADDRESS is not set. Using {scheduler} scheduler.')
    else:
        logger.info(f'DASK_SCHEDULER_ADDRESS is set to: {dask_scheduler_address}')
        scheduler = dask.distributed.Client(dask_scheduler_address)
        logger.info(f'Dask client: {scheduler}')
    
    # Logging the shape and dtype of data
    logger.debug(f'data type: {type(data)}')
    logger.debug(f'data shape: {data.shape}, data dtype: {data.dtype}')
    
    # Logging the shape and dtype of sub_res
    logger.debug(f'sub_res type: {type(sub_res)}')
    logger.debug(f'sub_res shape: {sub_res.shape}, sub_res dtype: {sub_res.dtype}')
    
    # ORIGINAL TRANSPOSE
    # Transpose data and sub_res
    # NOTE: the image is transposed to match the ilastik output
    # comparing the first three dimensions of data and sub_res if they are not equal swap the axes
    if data.shape[:3] != sub_res.shape[:3]:
        logger.info('Transposing the image and sub_res')
        img = data.transpose(2,1,0)
        sub_res = sub_res.transpose(2,1,0,3)
    else:
        logger.info('No need to transpose the image and sub_res')
        img = data
        sub_res = sub_res
    
    
    #img = data.transpose(2,1,0)
    #sub_res = sub_res.transpose(2,1,0,3)
    
    # Using (1,2,0,3) as the transpose axes for sub_res
    # Using (1,2,0) as the transpose axes for img
    # NOTE: the image is transposed to match the ilastik output
    # img = data.transpose(1,2,0)
    # sub_res = sub_res.transpose(1,2,0,3)
    
    
    # logging the shape and dtype of img
    logger.debug(f'img type: {type(img)}')
    logger.debug(f'img shape: {img.shape}, img dtype: {img.dtype}')
    
    # logging the shape and dtype of sub_res
    logger.debug(f'sub_res type: {type(sub_res)}')
    logger.debug(f'sub_res shape: {sub_res.shape}, sub_res dtype: {sub_res.dtype}')
    
    # convert sub_res to a dask array
    if isinstance(sub_res, np.ndarray):
        sub_res = da.from_array(sub_res, chunks='auto')
        logger.debug(f'sub_res type: {type(sub_res)} shape: {sub_res.shape} dtype: {sub_res.dtype}')

    # convert img to a dask array
    if isinstance(img, np.ndarray):
        img = da.from_array(img, chunks='auto')
        
    # we look into sub_res which are the non-background classes
    # we want to know every possible class in the sub_res
    unique_classes = da.unique(sub_res)
    unique_classes, = dask.compute(unique_classes, scheduler=scheduler)
    
    # logging the unique classes
    logger.debug(f'unique classes: {unique_classes}')

    # compute the imgmax using dask
    classindex = ilastik_parameter["classindex"]
    #imgmax = da.argmax(da.transpose(sub_res, axes=(2,1,0,3)), axis=-1)
    imgmax = da.argmax(sub_res, axis=-1)
    imgmax = da.equal(imgmax, classindex)
    logger.debug(f'[after argmax] Memory usage (GB): {ps.memory_info().rss / 1024**3}')

    # Determine the type and dtype of imgmax
    logger.debug(f'imgmax type: {type(imgmax)}')
    logger.debug(f'imgmax shape: {imgmax.shape}, imgmax dtype: {imgmax.dtype}')

    # Compute the labels using dask-image
    with CustomProgressBar(dt=0.5):
        logger.info('Computing labels using dask-image')
        imglab, nlabels = dndi.label(imgmax)
        imglab, nlabels = dask.compute(imglab, nlabels, scheduler=scheduler)
    logger.debug(f'[before removing small objects] nlabels: {nlabels}')
    logger.debug(f'[after label] Memory usage (GB): {ps.memory_info().rss / 1024**3}')

    # Convert imglab dtype to use_dtype (default: np.uint16)
    if imglab.dtype != use_dtype and nlabels < np.iinfo(use_dtype).max:
        logger.info(f'Converting imglab dtype from {imglab.dtype} to {use_dtype}')
        imglab = imglab.astype(use_dtype)
        logger.debug(f'[after converting dtype] Memory usage (GB): {ps.memory_info().rss / 1024**3}')
    else :
        logger.info(f'imglab dtype is already {use_dtype} or nlabels is greater than {np.iinfo(use_dtype).max}')

    # Removing cells with size less than cells_min_size
    logger.info(f'Removing cells with size less than {min_cell_size}')
    imglab = morphology.remove_small_objects(imglab, min_size=min_cell_size)
    logger.debug(f'imglab type: {type(imglab)} shape: {imglab.shape} dtype: {imglab.dtype}')
    logger.debug(f'[after remove_small_objects] Memory usage (GB): {ps.memory_info().rss / 1024**3}')
    
    # Convert imglab to a dask array
    if isinstance(imglab, np.ndarray):
        imglab = da.from_array(imglab, chunks='auto')

    # config dask to avoid slicing large chunks
    dask.config.set(**{"array.slicing.split_large_chunks": False})
        
    # Recompute the number of unique labels after filtering
    # Using dask.array's unique function for large datasets
    with CustomProgressBar(dt=0.5):
        logger.info('Computing unique labels using dask')
        unique_labels = da.unique(imglab)
        unique_labels, = dask.compute(unique_labels, scheduler=scheduler)  # Compute the unique labels explicitly
    logger.debug(f'[after unique] Memory usage (GB): {ps.memory_info().rss / 1024**3}')
    logger.debug(f'unique labels (including the background label 0): {unique_labels}')
    # NOTE: unique_labels includes the background label (0)
    # removing the background label (0) from unique_labels
    unique_labels = unique_labels[1:]
    nlabels = len(unique_labels)
    logger.debug(f'[after removing small objects] nlabels: {nlabels}')
    
    if nlabels == 0:
        logger.warning('No cells found in the image chunk. Returning empty arrays.')
        return [np.zeros((0, 3), dtype=np.float32), np.zeros((0, 2), dtype=np.float32)]
    
    ## test that img and imglab shapes are compatible (so that they can be broadcast together)
    logger.debug(f'img type: {type(img)}')
    logger.debug(f'img shape: {img.shape}, img dtype: {img.dtype}')
    logger.debug(f'imglab type: {type(imglab)}')
    logger.debug(f'imglab shape: {imglab.shape}, imglab dtype: {imglab.dtype}')

    # Compute cell sizes using dask-image area
    # NOTE: The area is computed as the sum of the mask
    #       The mask is the binary image of the cell
    #       The mask is obtained by comparing the label image with the index
    with CustomProgressBar(dt=0.5):
        logger.info(f'computing cell sizes using area')
        csize = dndi.area(img, imglab, index=unique_labels)
        csize, = dask.compute(csize, scheduler=scheduler)
    logger.info(f'csize shape: {csize.shape} type: {type(csize)} dtype: {csize.dtype}')

    # Display a sample of cell sizes
    sample_size = min(10, nlabels)
    logger.debug(f'csize[:{sample_size}]: {csize[:sample_size]}')
    
    # Compute centers of mass
    def compute_center_of_mass(index):
        return dndi.center_of_mass(img, imglab, index=index)

    # Compute centers of mass with progress bar
    # NOTE: Splitting compute in batches of 100 labels to avoid memory issues
    # NOTE: max batch_size is 100, if batch_size > 100, it is set to 100
    # NOTE: in soma nodes with 350GB memory, batch_size of 100 is safe
    # batch_size = 100
    if imglab.dtype == np.uint16:
        batch_size = 200
    else:
        batch_size = 100
    logger.info(f'computing centers of mass in batches of {batch_size} labels')
    from more_itertools import batched
    with CustomProgressBar(dt=0.5):
        centers = []
        # iterating unique_labels in batches of labels
        for i, batch in enumerate(batched(unique_labels, batch_size)):
            first_label = i*batch_size + 1
            last_label = min((i+1)*batch_size, nlabels)
            logger.info(f'computing centers of mass {first_label}-{last_label} of {nlabels}')
            centers_partial = compute_center_of_mass(batch)
            centers_partial = dask.compute(centers_partial, scheduler=scheduler)
            centers.extend(centers_partial)
    logger.debug(f'[after compute center_of_mass] Memory usage (GB): {ps.memory_info().rss / 1024**3}')

    # Convert centers to a single dask array
    centers = da.concatenate(centers, axis=0)
    logger.info(f'centers shape: {centers.shape} type: {type(centers)} dtype: {centers.dtype}')

    # Convert centers into a numpy array
    # NOTE: compute() is used to convert dask array to numpy array
    #       compute() returns a tuple, hence [0] is used to get the numpy array
    centers, = dask.compute(centers, scheduler=scheduler)
    centers = centers.astype(np.float32)
    logger.info(f'centers shape: {centers.shape} type: {type(centers)} dtype: {centers.dtype}')

    # Set numpy print options
    np.set_printoptions(precision=2, suppress=True)

    # Display a sample of centers
    sample_size = min(10, nlabels)
    logger.debug(f'centers[:{sample_size}]: {centers[:sample_size]}')

    # compute cell intensities
    def find_cell_intensity(index, cell_intensity_method):
        if cell_intensity_method == 'sum' or cell_intensity_method == 'sum_labels':
            return dndi.sum_labels(img, label_image=imglab, index=index)
        elif cell_intensity_method == 'mean':
            return dndi.mean(img, label_image=imglab, index=index)
        elif cell_intensity_method == 'max':
            return dndi.maximum(img, label_image=imglab, index=index)
        elif cell_intensity_method == 'min':
            return dndi.minimum(img, label_image=imglab, index=index)
        elif cell_intensity_method == 'median':
            return dndi.median(img, label_image=imglab, index=index)
        else:
            raise RuntimeError('cellIntensity: unknown method %s!' % cell_intensity_method)

    cell_intensity_method = ilastik_parameter["method"].lower()
    logger.info(f'computing cell intensities using method: {cell_intensity_method}')
    with CustomProgressBar(dt=0.5):
        cell_intensity = find_cell_intensity(unique_labels, cell_intensity_method)
        cell_intensity, = dask.compute(cell_intensity, scheduler=scheduler)
    logger.info(f'cell_intensity shape: {cell_intensity.shape} type: {type(cell_intensity)} dtype: {cell_intensity.dtype}')

    # Display a sample of cell intensities
    sample_size = min(10, nlabels)
    logger.debug(f'cell_intensity[:{sample_size}]: {cell_intensity[:sample_size]}')
    
    # If the scheduler is a dask client, close the client
    if scheduler != 'threads' and scheduler != 'processes':
        logger.info('Closing dask client')
        scheduler.close()

    # Return centers, cell sizes and intensities
    return [centers, np.vstack((cell_intensity, csize)).transpose()]

import pickle

# Define a method for testing the cell_maxima function
def test_cell_maxima_read_numpy(input_dir, chunk_id=0):
    
    # load the data, sub_res and ilastik_parameter from the pickle files
    sub_res_file = os.path.join(input_dir, f'chunk{chunk_id}_sub_res.pkl')
    data_file = os.path.join(input_dir, f'chunk{chunk_id}_data.pkl')
    ilastik_parameter_file = os.path.join(input_dir, f'chunk{chunk_id}_ilastik_parameter.pkl')
    
    sub_res = pickle.load(open(sub_res_file, 'rb'))
    data = pickle.load(open(data_file, 'rb'))
    ilastik_parameter = pickle.load(open(ilastik_parameter_file, 'rb'))
    
    #img = data.transpose(2,1,0)
    img = data
    
    # call the cell_maxima function
    centers, cell_measurements = cell_maxima(sub_res, img, ilastik_parameter)
    # print the centers and cell_measurements
    print(f'centers:\n{centers[:10]}')
    print(f'cell_measurements:\n{cell_measurements[:10]}')
    # return centers and cell_measurements
    return centers, cell_measurements

# Define a method for testing the cell_maxima function
def test_cell_maxima_read_hdf5(input_dir, chunk_id=0):
    
    data_file = os.path.join(input_dir, f'chunk{chunk_id}.h5')
    prob_file = os.path.join(input_dir, f'chunk{chunk_id}_Probabilities.h5')
    # create ilastik_parameter
    ilastik_parameter = {"classindex": 1, "method": "max"}
    
    with h5py.File(data_file, 'r') as fdata, h5py.File(prob_file, 'r') as fprob:
        # create a dask array from the HDF5 dataset
        data = da.from_array(fdata['exported_data'], chunks='auto')
        # create a dask array from the HDF5 dataset
        sub_res = da.from_array(fprob['exported_data'], chunks='auto')
        
        # load the data, sub_res to numpy arrays
        #data = fdata['exported_data'][:]
        #sub_res = fprob['exported_data'][:]

        #img = data.transpose(2,1,0)
        img = data
    
        # call the cell_maxima function
        centers, cell_measurements = cell_maxima(sub_res, img, ilastik_parameter)

    # print the centers and cell_measurements
    print(f'centers:\n{centers[:10]}')
    print(f'cell_measurements:\n{cell_measurements[:10]}')
    # return centers and cell_measurements
    return centers, cell_measurements



# Test the cell_maxima function in the main method
if __name__ == '__main__':

    # #Create a dask cluster
    # import multiprocessing
    # from dask.distributed import LocalCluster
    # #NOTE: number of workers is set to 8, which is a common denominator of 40 and 48 cores (soma nodes)
    # num_workers = 48 # number of workers
    # num_threads = multiprocessing.cpu_count()/num_workers
    # worker_memory_limit = int(cnp.get_available_memory()/num_workers)
    # logger.info(f'worker_memory_limit: {worker_memory_limit} bytes')
    # cluster = LocalCluster(n_workers=num_workers, 
    #                        threads_per_worker=num_threads,
    #                        processes=True,
    #                        dashboard_address=':8787',
    #                        memory_limit=worker_memory_limit)
    # logger.info(f'dask scheduler address: {cluster.scheduler_address}')
    # os.environ['DASK_SCHEDULER_ADDRESS'] = cluster.scheduler_address    
    
    input_dir = '/gpfs/soma_fs/scratch/valerio/nmr/li-data/results_partial'
    chunk_id = 32

    #test_cell_maxima_read_numpy(input_dir, chunk_id)
    test_cell_maxima_read_hdf5(input_dir, chunk_id)
    # cluster.close()
