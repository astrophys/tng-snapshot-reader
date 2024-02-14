# Author : Ali Snedden
# Date   : 22-january-2024
# 
#
#
"""Code to plot dark matter halos from TNG simulations with [optionally] gas density together
"""
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    """

    Args:

    Returns:

    Raises:
    """
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--halos', metavar='halo_pos_mass.npz', type=str,
                        help='Input npy file')
    parser.add_argument('--density', metavar='halo_pos_mass.npz', type=str, nargs='?',
                        help='Input npy file')
    #parser.add_argument('--output', metavar='output', type=str,
    #                    help='')
    args = parser.parse_args()
    halos = np.load(args.halos, allow_pickle=True)
    density = np.load(args.density, allow_pickle=True)

    ### Work on Halos
    haloV = halos['data']         # This is an ugly np.vector of tuples, let's rework this
    # Put the haloV into a data frame that I can more easily handle
    haloL = []
    for i in range(haloV.shape[0]):
        #lst = [haloV[i][0], haloV[i][1], haloV[i][2], haloV[i][3], haloV[i][4]]
        haloL.append(list(haloV[i]))
    haloDF = pd.DataFrame(haloL)
    # Strip out spaces, make lower case
    header = [string.split(' ')[0].lower() for string in halos['metadata'].item()['headers']]
    units = halos['metadata'].item()['units']
    
    haloDF.columns = header
    ### Work on density

    print("WARNING!! Ugly hardcoding going on below")
    fig = plt.figure()
    # Only plot halos
    if density is None:
        # Only plot from 0 -> zthresh
        zthresh = 1000     # kpc/h
        print("Subsetting halos from 0 -> {}kpc/h".format(zthresh))
        subDF = haloDF[haloDF['z'] < zthresh]
        #slab = 
        gs = fig.add_gridspec(1,1)
        ax = fig.add_subplot(gs[0,0])
        ax.scatter(subDF['x'], subDF['y'], s=np.log10(np.max(subDF['mass'])+2)/10000)
        ax.set_title("{:<.2f}kpc/h slab in z-axis".format(zthresh))
    else:
        # Let's plot z=0 -> 7500kpc/h, it may be the issue that the order of axis in
        # the gas file is off
        # Hard coded for now
        halothresh = 7500
        gasthresh  = 60
        subDF = haloDF[haloDF['z'] < halothresh]
        gs = fig.add_gridspec(1,2)
        # halos
        ax = fig.add_subplot(gs[0,0])
        #ax.scatter(haloDF['x'], haloDF['y'], s=np.log10(np.max(haloDF['mass'])+2)/1500000)
        ax.scatter(subDF['x'], subDF['y'], s=np.log10(np.max(subDF['mass'])+2)/10000)
        ax.set_title("{:<.2f}kpc/h slab in z-axis".format(halothresh))
        # density
        ax = fig.add_subplot(gs[0,1])
        # Summing over axis=2 really is over z-axis, to test
        # aa = np.asarray([[[1,2],[3,4],[5,6]], [[7,8],[9,10],[11,12]], [[13,14],[15,16],[17,18]], [[19,20],[21,22],[23,24]]])
        # (Pdb) aa.shape
        # (4, 3, 2)
        # (Pdb) np.sum(aa, axis=2).shape
        # (4, 3)
        #density2D = np.sum(density[:,:,0:gasthresh], axis=2)
        #density2D = np.sum(density[:,0:gasthresh,:], axis=1

        # This gets the correct spatial organization of Gas density w/r/t Halos)
        #   --> See halo_vs_gas_npsum_axis0.jpg
        density2D = np.sum(density[0:gasthresh,:,:], axis=0)
        im = ax.imshow(np.log10(density2D+1))
        fig.colorbar(im, ax=ax, anchor=(0, 0.3), shrink=0.7)
        ax.set_xlim(0,density.shape[0])
        ax.set_ylim(0,density.shape[1])
        ax.set_title("0-{} gas slab in z-axis".format(gasthresh))
        fig.suptitle('z=[0-{}kpc/h]'.format(halothresh))


    #print('Subset = {}'.format(subDF.shape))
    plt.show()

    ### Obsolete until (if ever) figure out Disperse
    #fout = open("{}.NDfield_ascii".format(args.output), "w+")
    ## Header
    #fout.write("ANDFIELD COORDS\n")
    #fout.write("3 {}\n".format(subDF.shape[0]))
    #for index, row in subDF.iterrows():
    #    fout.write("{} {} {}\n".format(row['x'], row['y'], row['z']))
    #fout.write("%i %i %i\n"%(nx,ny,nz))
    #for k in range(0, nz):
    #    for j in range(0, ny):
    #        for i in range(0, nx):
    #            fout.write("{:<.4e} ".format(data[i,j,k]))
    #        fout.write("\n")
    #print("Finished outputting : %s"%(args.output))
    #fout.close()
    sys.exit(0)


if __name__ == "__main__":
    main()
