# Author : Ali Snedden
# Date   : 11/1/22
# License: MIT
"""Module that reads in Illustrius-3 TNG-50 simulations
"""
import sys
import argparse
import numpy as np
import illustris_python as il
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('tkagg')


def main():
    """
    Prints to stdout whether two files are identical within the tolerance

    Args:
        None.

    Returns:
        None
    """
    ### Get Command Line Options
    parser = argparse.ArgumentParser(description="Reader for Illustrius-3 Snapshots")
    parser.add_argument('path',   metavar='path/dir_above_snapshot_dir',   type=str,
                        help='Path to directory ABOVE dir containing snapshot data')
    parser.add_argument('snap',   metavar='snapshot_number',   type=int,
                        help='Snapshot number')
    parser.add_argument('nvox',   metavar='N_voxels_per_edge',   type=int,
                        help='Number of voxels per cubic edge')
    # Can't seem to extract header info from h5py.File("output/snapdir_135/snap_135.1.hdf5")
    parser.add_argument('size_in_kpc', metavar='Boxsize_in_comoving_kpc/h',
                        type=float, help='Boxsize in comoving kpc/h')
    args = parser.parse_args()

    ### Get arguments
    path = args.path
    snap = args.snap
    nvox = args.nvox
    bsize= args.size_in_kpc
    gas = il.snapshot.loadSubset(path,snap,'gas')
    dm  = il.snapshot.loadSubset(path,snap,'dm')
    gridM = np.zeros([nvox, nvox, nvox])
    dmMass=0.0282173775591101

    # Gas first
    iV = np.int32(np.floor(gas['Coordinates'][:,0] * nvox / bsize))
    jV = np.int32(np.floor(gas['Coordinates'][:,1] * nvox / bsize))
    kV = np.int32(np.floor(gas['Coordinates'][:,2] * nvox / bsize))
    # is empty
    for idx in range(len(iV)):
        i = iV[idx]
        j = jV[idx]
        k = kV[idx]
        gridM[i,j,k] += gas['Masses'][idx]

    # DM next
    iV = np.int32(np.floor(dm['Coordinates'][:,0] * nvox / bsize))
    jV = np.int32(np.floor(dm['Coordinates'][:,1] * nvox / bsize))
    kV = np.int32(np.floor(dm['Coordinates'][:,2] * nvox / bsize))
    # is empty
    for idx in range(len(iV)):
        i = iV[idx]
        j = jV[idx]
        k = kV[idx]
        gridM[i,j,k] += dmMass

    # Test heatmap plot 
    fig, ax = plt.subplots()
    # This reproduces image similar to heatmap.py
    im = ax.imshow(np.log(np.sum(gridM, axis=2)).T, origin='lower')
    plt.show()
    
         
      
    # DM next

    sys.exit(0)


if __name__ == "__main__":
    main()
