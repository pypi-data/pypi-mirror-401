#NOTE: First attempt of accelerating the cell_intensity function using cupy for parallel processing and measurements
import tifffile as tff

import os
import psutil # for memory usage

import multiprocessing as mp

# the cpu version uses scipy for measurements and concurrent futures for parallel processing
import numpy as np
import scipy.ndimage as sndi
from concurrent.futures import ThreadPoolExecutor

# the gpu version uses cupy for measurements and cupyx.scipy.ndimage for measurements
import cupy as cp
import cupyx.scipy.ndimage as cndi

import logging

logger = logging.getLogger()

def test_cuda():
    try:
        # Attempt to create a CuPy array on a CUDA device
        cp.array([1], dtype=cp.float32).device
        cuda_available = True
        meminfo = cp.cuda.runtime.memGetInfo()
        total_memory = meminfo.total
    except cp.cuda.runtime.CUDARuntimeError:
        cuda_available = False
        total_memory = 0
        
    return cuda_available, total_memory


def cell_maxima_shape(sub_res, substack, image_sequence, ilastik_parameter):
    
    # persisting the cell_maxima_shape arguments as state for the function using pickle
    # this is necessary because the function will be executed on a remote server
    # and the arguments will not be available in the remote server's memory
    # the function will be executed on the remote server by SLURM
    
    # sub_res is a numpy array
    # substack is a dictionary
    # image_sequence is a tifffile.TiffSequence object
    # ilastik_parameter is a dictionary
    
    # import pickle
    # pickle.dump(sub_res, open('sub_res.pkl', 'wb'), protocol=4)
    # pickle.dump(substack, open('substack.pkl', 'wb'), protocol=4)
    # pickle.dump(image_sequence, open('image_sequence.pkl', 'wb'), protocol=4)
    # pickle.dump(ilastik_parameter, open('ilastik_parameter.pkl', 'wb'), protocol=4)

    # reading image data from tiff files (image_sequence) using substack['z'] (z range of the substack)
    data = tff.imread(image_sequence.files[substack['z'][0]:substack['z'][1]])
    
    return cell_maxima(sub_res, data, ilastik_parameter)

def cell_maxima(sub_res, data, ilastik_parameter):
    
    # count the number of files that exist ending with the name 'sub_res.pkl'
    count = len([f for f in os.listdir('.') if f.endswith('sub_res.pkl')])
    
    # persisting the cell_maxima arguments as state for the function using pickle  (DEBUG)
    import pickle
    pickle.dump(sub_res, open(f'{count+1}_sub_res.pkl', 'wb'), protocol=4)
    pickle.dump(data, open(f'{count+1}_data.pkl', 'wb'), protocol=4)
    pickle.dump(ilastik_parameter, open(f'{count+1}_ilastik_parameter.pkl', 'wb'), protocol=4)
   
    # NOTE: the image without transpose is already available in the calling method (run_ilastik) 
    image = data.transpose(2,1,0)

    ps = psutil.Process(os.getpid())
    memory = ps.memory_info().rss
    logger.debug(f'[after transpose] Memory usage (GB): {memory / 1024**3}')

    ## determine if cuda is available
    cuda_available, device_mem = test_cuda()
    logger.info(f'cuda_available: {cuda_available}')
    logger.info(f'device memory: {device_mem}')
    
    # if cuda is available and the device memory is greater than 2 times the size of the image and sub_resi
    if cuda_available and device_mem > 2 * (image.nbytes + sub_res.nbytes):
        logger.info('__cell_maxima: running on GPU')
        return __cell_maxima_gpu(sub_res, image, ilastik_parameter)
    else:
        logger.info('__cell_maxima: running on CPU')
        return __cell_maxima_cpu(sub_res, image, ilastik_parameter)


# __cell_maxima_cpu function
def __cell_maxima_cpu(sub_res, img, ilastik_parameter):
    imgmax = np.argmax(sub_res.transpose(2,1,0,3), axis=-1)
    imgmax = imgmax == ilastik_parameter["classindex"]
    imglab, nlab = sndi.label(imgmax)
    logger.info(f'nlab: {nlab}')

    ## test that img and imglab shapes are compatible (so that they can be broadcast together)
    logger.info(f'img shape: {img.shape}')
    logger.info(f'imglab shape: {imglab.shape}')

    ## obtain the number of multiprocessing cores
    ncores = mp.cpu_count()

    # use concurrent processing to speed up the computation (concurrent futures)
    centers = np.zeros((0,3))

    def compute_center_of_mass(index):
        return sndi.center_of_mass(img, imglab, index=index)

    with ThreadPoolExecutor(max_workers=ncores) as executor:
        centers = np.array(list(executor.map(compute_center_of_mass, np.arange(1, nlab+1))))

    #find cell sizes
    def compute_cell_size(index):
        return sndi.sum(imglab == index)

    with ThreadPoolExecutor(max_workers=ncores) as executor:
        csize = np.array(list(executor.map(compute_cell_size, np.arange(1, nlab+1))))

    #find cell intensities
    cell_intensity_method = ilastik_parameter["method"].lower()

    def find_cell_intensity(index):
        if cell_intensity_method == 'sum':
            return sndi.sum(img, labels=imglab, index=index)
        elif cell_intensity_method == 'mean':
            return sndi.mean(img, labels=imglab, index=index)
        elif cell_intensity_method == 'max':
            return sndi.maximum(img, labels=imglab, index=index)
        elif cell_intensity_method == 'min':
            return sndi.minimum(img, labels=imglab, index=index)
        else:
            raise RuntimeError(f'[cellIntensity] unknown method: {cell_intensity_method} !')

    with ThreadPoolExecutor(max_workers=ncores) as executor:
        cintensity = np.array(list(executor.map(find_cell_intensity, np.arange(1, nlab+1))))

    idz = csize > 0  #remove cells of size 0

    return [centers[idz], np.vstack((cintensity[idz], csize[idz])).transpose()]

# gpu accelerated cell_maxima shape function
def __cell_maxima_gpu(sub_res, img, ilastik_parameter):
    imgmax = cp.argmax(cp.transpose(sub_res, axes=(2,1,0,3)), axis=-1) # transpose from [z,y,x, class] to [x,y,z,class]
    imgmax = imgmax == ilastik_parameter["classindex"]
    imglab, nlab = cndi.label(imgmax)

    ## test that img and imglab shapes are compatible (so that they can be broadcast together)
    logger.info(f'img shape: {img.shape}')
    logger.info(f'imglab shape: {imglab.shape}')

    # compute cells center of mass
    centers = cndi.center_of_mass(img, imglab, index=cp.arange(1, nlab))

    #find cell sizes
    csize = cndi.sum_labels(imglab, index=cp.arange(1, nlab))

    #find cell intensities
    cell_intensity_method = ilastik_parameter["method"].lower()
    
    if cell_intensity_method == 'sum':
        cintensity = cndi.sum(img, labels=imglab, index=cp.arange(1, nlab))
    elif cell_intensity_method == 'mean':
        cintensity = cndi.mean(img, labels=imglab, index=cp.arange(1, nlab))
    elif cell_intensity_method == 'max':
        cintensity = cndi.maximum(img, labels=imglab, index=cp.arange(1, nlab))
    elif cell_intensity_method == 'min':
        cintensity = cndi.minimum(img, labels=imglab, index=cp.arange(1, nlab))
    else:
        raise RuntimeError(f'[cellIntensity] unknown method: {cell_intensity_method}!')

    idz = csize > 0  #remove cells of size 0

    return [centers[idz], np.vstack((cintensity[idz], csize[idz])).transpose()]
