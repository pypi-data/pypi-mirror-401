ClearMap (NMR - G. Fenton customized version)
========


To learn about ClearMap read the [Documentation](README_CLEARMAP.md).

To use ClearMap in SOMA cluster follow these steps:


## Setup

**1.** Clone this repository in soma login nodes (using your soma account):

```
git clone https://github.com/mpinb/clearmap-nmr.git
```

**2.** Change into the cloned repository folder and create the container using the ilastik-nmr definition file (`ilastik-nmr.def`)

```
cd ~/clearmap-nmr
module load apptainer
apptainer build ilastik-nmr.sif ilastik-nmr.def
```

**3.** Create conda environment using the environment definition file in this repository

```
module load anaconda3/2022.10
source activate
cd ~/clearmap-nmr
CONDA_OVERRIDE_CUDA="11.8" conda env create -n clearmap-nmr -f clearmap-nmr-env.yml
```

**4.** Activate the environment, add scripts that setup the environment variables and create an `ipython kernel` to use the environment inside Jupyter Notebook.

```
conda activate clearmap-nmr
cp env_vars.sh $CONDA_PREFIX/etc/conda/activate.d
cp reset_env_vars.sh $CONDA_PREFIX/etc/conda/deactivate.d
python -m ipykernel install --user --name clearmap-nmr --display-name 'clearmap-nmr'
```

## pip install clearmap-nmr  (NEW: 26.08.2025)

We now recommend to pip install the package to avoid recompilation of the Cython extensions in `soma` cluster. 

```bash
python -m pip install clearmap-nmr
```

## Running clearmap-nmr

Allocate a compute node from soma GPU partition (large memory nodes).

```
srun -p GPU -t 8:00:00 --mem 720G --cpus-per-task=48 --nodes=1 --pty bash
```

If there are no GPU nodes available, allocate a node from the CPU partition instead.

```
srun -p GPU -t 8:00:00 --mem 350G --cpus-per-task=48 --nodes=1 --pty bash
```


Start a shell using the apptainer container image and then inside the container load anaconda3 and launch jupyter lab

**Note:** The environment modules script is used to load anaconda.
```
module load apptainer
apptainer shell --bind /gpfs:/gpfs ilastik-nmr.sif
# another alternative is using the ilastik-nmr.sif image in /gpfs/soma_fs/scratch/containers
# apptainer shell --bind /gpfs:/gpfs /gpfs/soma_fs/scratch/containers/ilastik-nmr.sif
source /gpfs/soma_fs/soft/CentOS_7/packages/x86_64/environment-modules/5.1.1/init/bash
module load anaconda3/2022.10
source activate
conda activate clearmap-nmr

# OPTION 1: Use jupyter-lab 
cd ** CLEARMAP-NMR REPOSITORY CLONE DIRECTORY **
jupyter-lab --port 2020 --no-browser

# OPTION 2: Run a python script
python PYTHON-SCRIPT.py
```
From your workstation open an *ssh-tunnel* connection to the compute node where the jupyter server instance is running.

```
ssh -fN -L 2020:localhost:2020 somacpu0XX
```

Open your browser and enter the jupyter-lab link from the previous step to start a Jupyter Lab session and run the ClearMap NMR notebooks. Remember to switch the ipython kernel to use the one created above.
