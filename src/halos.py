# Author : Ali Snedden
# Date   : 11/24/22
# License: MIT
# NOTES  : 
#
#   https://www.tng-project.org/data/docs/specifications/#sec2
#
#

"""Module that reads in Illustrius-3 TNG-50 simulations
"""
import sys
import argparse
import numpy as np
import illustris_python as il
import matplotlib.pyplot as plt
import matplotlib
import pickle
#matplotlib.use('tkagg')


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
    #parser.add_argument('nvox',   metavar='N_voxels_per_edge',   type=int,
    #                    help='Number of voxels per cubic edge')
    # Can't seem to extract header info from h5py.File("output/snapdir_135/snap_135.1.hdf5")
    #parser.add_argument('size_in_kpc', metavar='Boxsize_in_comoving_kpc/h',
    #                    type=float, help='Boxsize in comoving kpc/h')
    args = parser.parse_args()

    ### Get arguments
    path = args.path
    snap = args.snap
    halos = il.groupcat.load(path,snap)
    # Plot for diagnostic purposes
    thresh = 100
    haloBool = halos['halos']['GroupMass'] > thresh
    print("np.sum(haloBool) = {}".format(np.sum(haloBool)))
    haloPos = halos['halos']['GroupPos'][haloBool]
    plt.scatter(haloPos[:,0], haloPos[:,1])
    plt.show()
    #dmMass=0.0282173775591101
    np.savetxt("halo_pos_snap_{}_thresh_{}.txt".format(snap,thresh), haloPos)


    sys.exit(0)


if __name__ == "__main__":
    main()
