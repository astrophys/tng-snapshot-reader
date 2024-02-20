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

def plot_segmentation_results(haloV : np.ndarray, densM : np.ndarray,
                              matrixL : list = None, z : int = 0,
                              trans : bool = False) -> None:
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
    if matrixL is not None:
        for i in range(len(matrixL)):
            matrix = matrixL[i]
            if i == 0:
                mshape = matrix.shape           # Shape of matrixL[0]
                if len(mshape) != 3:
                    raise ValueError("ERROR!!! Expected to be matrix with 3 spatial dims "
                                     "not {} dims".format(len(matrix.shape)))
                # Assume square
                if(mshape[0] != mshape[1] or mshape[1] != mshape[2] or
                   mshape[0] != mshape[2]):
                    raise ValueError("ERROR!!! Expected to be matrix to be cubic with "
                                     "dims {} == {} == {}".format(mshape[0], mshape[1],
                                     mshape[2]))
            else:
                # All matrices should be the same
                if mshape != matrix.shape :
                    raise ValueError("ERROR!!! shape {} != matrixL[{}].shape".format(mshape,
                                     i, matrix.shape))
    if trans is True:
        print("Taking TRANSPOSE!!!")
    else:
        print("Keeping order x,y,z ")
    # Let's bin and only select relevant halos
    minz = np.min(haloV['z'])
    maxz = np.max(haloV['z'])
    if matrixL is not None:
        dz = (maxz - minz)/mshape[0]
    else :
        dz = (maxz - minz)/densM.shape[0]
    lowerz = minz + z*dz
    upperz = minz + (z+1)*dz
    tmpV = haloV[haloV['z'] > lowerz]
    hsliceV = tmpV[tmpV['z'] <= upperz]

    fig = plt.figure()
    # Plot only halos and gas density
    if matrixL is None:
        nrow = 1
        ncol = 2
    # Plot halos, gas density and segmentation files
    else :
        nrow = 3
        ncol = 2
    gs = fig.add_gridspec(nrow,ncol)
    # halos
    haloax = fig.add_subplot(gs[0,0])
    haloax.scatter(hsliceV['x'], hsliceV['y'], s=np.log10(hsliceV['mass']+2)/1000)
    xmin,xmax = haloax.get_xlim()
    ymin,ymax = haloax.get_ylim()
    haloax.set_aspect(abs(xmax-xmin)/abs(ymax-ymin))

    # density
    ax = fig.add_subplot(gs[0,1])
    #density2D = np.sum(densM[:,:,:], axis=0)
    density2D = densM[:,:,z]
    if trans is True:
        im = ax.imshow(np.log10(density2D+1).T)
    else :
        im = ax.imshow(np.log10(density2D+1))
    #im = ax.imshow(np.log10(density2D+1))
    fig.colorbar(im, ax=ax, anchor=(0, 0.3), shrink=0.7)
    ax.set_xlim(0,density2D.shape[0])
    ax.set_ylim(0,density2D.shape[1])
    #ax.set_title("0-{} gas slab in z-axis".format(gasthresh))
    #fig.suptitle('z=[0-{}kpc/h]'.format(halothresh))

    if matrixL is not None:
        # Vessels
        matrix = matrixL[0]
        ax = fig.add_subplot(gs[1,0])
        #ax.imshow(np.log10(matrix[:,:,z]+1))        # This is doesn't look good.
        if trans is True:
            im = ax.imshow(matrix[:,:,z].T)        # This is doesn't look good.
        else:
            im = ax.imshow(matrix[:,:,z])        # This is doesn't look good.
        fig.colorbar(im, ax=ax, anchor=(0, 0.3), shrink=0.7)
        ax.set_xlim(0,matrix.shape[0])
        ax.set_ylim(0,matrix.shape[1])

        # Clusters
        matrix = matrixL[1]
        ax = fig.add_subplot(gs[1,1])
        #ax.imshow(np.log10(matrix[:,:,z]+1))        # This is doesn't look good.
        #ax.imshow(np.log10(matrix[:,:,z]+1).T)        # This is doesn't look good.
        if trans is True:
            im = ax.imshow(matrix[:,:,z].T)        # This is doesn't look good.
        else:
            im = ax.imshow(matrix[:,:,z])        # This is doesn't look good.
        fig.colorbar(im, ax=ax, anchor=(0, 0.3), shrink=0.7)
        ax.set_xlim(0,matrix.shape[0])
        ax.set_ylim(0,matrix.shape[1])

        # Voids
        matrix = matrixL[2]
        ax = fig.add_subplot(gs[2,0])
        #ax.imshow(np.log10(matrix[:,:,z]+1))        # This is doesn't look good.
        #ax.imshow(np.log10(matrix[:,:,z]+1).T)        # This is doesn't look good.
        if trans is True:
            im = ax.imshow(matrix[:,:,z].T)        # This is doesn't look good.
        else:
            im = ax.imshow(matrix[:,:,z])        # This is doesn't look good.
        fig.colorbar(im, ax=ax, anchor=(0, 0.3), shrink=0.7)
        ax.set_xlim(0,matrix.shape[0])
        ax.set_ylim(0,matrix.shape[1])
        
    plt.show()
    sys.exit(0)


if __name__ == "__main__":
    main()
