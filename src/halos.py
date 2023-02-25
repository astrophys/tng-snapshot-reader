# Author : Ali Snedden
# Date   : 11/24/22
# License: MIT
# NOTES  : 
#
#   https://www.tng-project.org/data/docs/specifications/#sec2
#
# Example : 
#   python -m pdb src/halos.py ~/Lab/phillips/data/TNG-50/Illustris-3/output/ 135 100
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
    parser.add_argument('thresh',   metavar='halo_threshold_in_10^10Msun',   type=float,
                        help='Halo threshold in 10^10Msun')
    # Can't seem to extract header info from h5py.File("output/snapdir_135/snap_135.1.hdf5")
    #parser.add_argument('size_in_kpc', metavar='Boxsize_in_comoving_kpc/h',
    #                    type=float, help='Boxsize in comoving kpc/h')
    args = parser.parse_args()

    ### Get arguments
    path = args.path
    snap = args.snap
    halos = il.groupcat.load(path,snap)
    # Plot for diagnostic purposes
    thresh = args.thresh
    haloBool = halos['halos']['GroupMass'] > thresh
    print("np.sum(haloBool) = {}".format(np.sum(haloBool)))
    haloPos = halos['halos']['GroupPos'][haloBool]
    haloMass= halos['halos']['GroupMass'][haloBool]
    plt.scatter(haloPos[:,0], haloPos[:,1])
    plt.show()
    #dmMass=0.0282173775591101
    # np.savetxt("halos_pos_snap_{}_thresh_{}_Msun.txt".format(snap,thresh), haloPos)

    # Write OFF 
    fout = open("halos_pos_snap_{}_thresh_{}_10pow10_Msun.xyzm".format(snap,thresh), "w+")
    fout.write("x y z m\n")
    #fout.write("{} {} {} {}\n".format(haloPos.shape[0], 0, 0))
    for i in range(haloPos.shape[0]):
        fout.write("{:<.12f} {:<.12f} {:<.12f} {:<.12f}\n".format(haloPos[i][0], haloPos[i][1],
                   haloPos[i][2], haloMass[i]))
    fout.close()


    sys.exit(0)


if __name__ == "__main__":
    main()
