# Author : Ali Snedden
# Date   : 22-january-2024
# 
#
#
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TKAgg')      # For interactive plotting

def plot_segmentation_results(haloV : np.ndarray, densM : np.ndarray, matrixL : list,
                              z : int) -> None:
    """Takes halos (loaded from npz) and matrix and plots a slice of it

    Args:
        haloV   : np.array, halos created by Guobao 
        densM   : np.array, density halo created by Guobao
        matrixL : list, list of numpy matrixes
        z       : in, slice in z to plot

    Returns:
        n/a, this plots

    Raises:
    """
    ### Sanity check
    for i in range(len(matrixL)):
        matrix = matrixL[i]
        if i == 0:
            mshape = matrix.shape           # Shape of matrixL[0]
            if len(mshape) != 3:
                raise ValueError("ERROR!!! Expected to be matrix with 3 spatial dims "
                                 "not {} dims".format(len(matrix.shape)))
            # Assume square
            if mshape[0] != mshape[1] or mshape[1] != mshape[2] or mshape[0] != mshape[2]:
                raise ValueError("ERROR!!! Expected to be matrix to be cubic with dims "
                                 "{} == {} == {}".format(mshape[0], mshape[1], mshape[2]))
        else:
            # All matrices should be the same
            if mshape != matrix.shape :
                raise ValueError("ERROR!!! shape {} != matrixL[{}].shape".format(mshape,
                                 i, matrix.shape))
    # Let's bin and only select relevant halos
    minz = np.min(haloV['z'])
    dz = (np.max(haloV['z']) - np.min(haloV['z']))/mshape[0]
    lowerz = minz + z*dz
    upperz = minz + (z+1)*dz
    tmpV = haloV[haloV['z'] > lowerz]
    hsliceV = tmpV[tmpV['z'] <= upperz]

    fig = plt.figure()
    # Be flexible to plot multiple data sets
    if len(matrixL) == 1:
        nrow = 1
        ncol = 2
    else:
        nrow = 2
        ncol = 2
    gs = fig.add_gridspec(nrow,ncol)
    # halos
    haloax = fig.add_subplot(gs[0,0])
    haloax.scatter(hsliceV['x'], hsliceV['y'], s=np.log10(hsliceV['mass']+2))

    # Vessels
    matrix = matrixL[0]
    ax = fig.add_subplot(gs[0,1])
    ax.imshow(np.log10(matrix[:,:,z]))        # This is doesn't look good.

    # Matrix plot
    if len(matrixL) > 1:
        # Clusters
        matrix = matrixL[1]
        ax = fig.add_subplot(gs[1,0])
        ax.imshow(np.log10(matrix[:,:,z]))        # This is doesn't look good.
        # Voids
        matrix = matrixL[2]
        ax = fig.add_subplot(gs[1,1])
        ax.imshow(np.log10(matrix[:,:,z]))        # This is doesn't look good.
        
    #ax.scatter(subDF['x'], subDF['y'], s=np.log10(np.max(subDF['mass'])+2)/10000)
    #ax.set_title("{:<.2f}kpc/h slab in z-axis".format(zthresh))

    #print('Subset = {}'.format(subDF.shape))
    plt.show()

    #fout = open("{}.NDfield_ascii".format(args.output), "w+")
    # Header
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
