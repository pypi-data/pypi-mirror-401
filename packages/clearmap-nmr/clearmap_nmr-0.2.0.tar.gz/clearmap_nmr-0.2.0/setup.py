from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize

import os
import numpy as np
import multiprocessing as mp # import multiprocessing to determine CPU cores

# Define C and C++ flags to suppress warnings about unused variables
compile_args = ["-Wno-unused-variable", "-Wno-maybe-uninitialized", "-Wno-array-bounds"]

def make_ext(modname, pyxfilename):
    """
    Create a Cython extension module.
    """
    
    ext = Extension(
        name = modname,
        sources = [pyxfilename],
        language="c++",
        include_dirs = [
            np.get_include(), 
            os.path.dirname(os.path.abspath(__file__))
            ],
        extra_compile_args = ["-O3", "-march=native", "-fopenmp"] + compile_args,
        extra_link_args = ['-fopenmp'],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
        )
    
    return ext

# Define extensions to compile using make_ext
extensions = [
    make_ext("ClearMap.ImageProcessing.Binary.FillingCode", 
             "ClearMap/ImageProcessing/Binary/FillingCode.pyx"),
    make_ext("ClearMap.ImageProcessing.Clipping.ClippingCode", 
             "ClearMap/ImageProcessing/Clipping/ClippingCode.pyx"),
    make_ext("ClearMap.ImageProcessing.Differentiation.HessianCode", 
             "ClearMap/ImageProcessing/Differentiation/HessianCode.pyx"),
    make_ext("ClearMap.ImageProcessing.Filter.Rank.RankCode", 
             "ClearMap/ImageProcessing/Filter/Rank/RankCode.pyx"),
    make_ext("ClearMap.ImageProcessing.Filter.Rank.PercentileCode", 
             "ClearMap/ImageProcessing/Filter/Rank/PercentileCode.pyx"),
    make_ext("ClearMap.ImageProcessing.Filter.Rank.BilateralCode", 
             "ClearMap/ImageProcessing/Filter/Rank/BilateralCode.pyx"),
    make_ext("ClearMap.ImageProcessing.Filter.Rank.ParametricCode", 
             "ClearMap/ImageProcessing/Filter/Rank/ParametricCode.pyx"),
    make_ext("ClearMap.ImageProcessing.Thresholding.ThresholdingCode", 
             "ClearMap/ImageProcessing/Thresholding/ThresholdingCode.pyx"),
    make_ext("ClearMap.ImageProcessing.Tracing.TraceCode", 
             "ClearMap/ImageProcessing/Tracing/TraceCode.pyx"),
    make_ext("ClearMap.ParallelProcessing.DataProcessing.ArrayProcessingCode", 
             "ClearMap/ParallelProcessing/DataProcessing/ArrayProcessingCode.pyx"),
    make_ext("ClearMap.ParallelProcessing.DataProcessing.ConvolvePointListCode", 
             "ClearMap/ParallelProcessing/DataProcessing/ConvolvePointListCode.pyx"),
    make_ext("ClearMap.ParallelProcessing.DataProcessing.DevolvePointListCode", 
             "ClearMap/ParallelProcessing/DataProcessing/DevolvePointListCode.pyx"),
    make_ext("ClearMap.ParallelProcessing.DataProcessing.MeasurePointListCode", 
             "ClearMap/ParallelProcessing/DataProcessing/MeasurePointListCode.pyx"),
    make_ext("ClearMap.ParallelProcessing.DataProcessing.StatisticsPointListCode", 
             "ClearMap/ParallelProcessing/DataProcessing/StatisticsPointListCode.pyx"),
]

# Cythonize the extensions (limit to 8 threads max)
num_threads = min(8, mp.cpu_count())
cythonized_extensions = cythonize(
    extensions,
    language_level=3,
    nthreads=num_threads,
    compiler_directives={
        "embedsignature": True,
        "boundscheck": False,
        "wraparound": False,
        "cdivision": True,
        "initializedcheck": False,
        # "legacy_implicit_noexcept": True,  # available since Cython 3.0
    },
)

if __name__ == "__main__":
    setup(ext_modules=cythonized_extensions)