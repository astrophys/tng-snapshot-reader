# Author : Ali Snedden
# Date   : 29-january-2024
# 
#
#
import sys
import argparse
import numpy as np
import pandas as pd
from file_io import read_matlab_int
from plot import plot_segmentation_results
import matplotlib.pyplot as plt
# https://matplotlib.org/stable/users/explain/figure/backends.html
import matplotlib
matplotlib.use('TKAgg')



def main():
    """

    Args:

    Returns:

    Raises:
    """
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--halos', metavar='halo_pos_mass.npz', type=str,
                        help='Halo npz file')
    parser.add_argument('--density', metavar='density.npy', type=str,
                        help='Gas Density npy file')
    parser.add_argument('--vessels', metavar='output', type=str, nargs='?',
                        help='')
    parser.add_argument('--clusters', metavar='output', type=str, nargs='?',
                        help='')
    parser.add_argument('--voids', metavar='output', type=str, nargs='?',
                        help='')
    #parser.add_argument('--output', metavar='output', type=str,
    #                    help='')
    args = parser.parse_args()
    print("Reading : {} ".format(args.halos))
    halos = np.load(args.halos, allow_pickle=True)
    density = np.load(args.density, allow_pickle=True)
    print("Reading : {} ".format(args.density))
    haloV = halos['data']         # This is an ugly np.vector of tuples, let's rework this
    #
    if args.vessels is not None:
        print("Reading : {} ".format(args.vessels))
        vesselM = read_matlab_int(args.vessels)
    if args.clusters is not None:
        print("Reading : {} ".format(args.clusters))
        clusterM = read_matlab_int(args.clusters)
    if args.voids is not None:
        print("Reading : {} ".format(args.voids))
        voidM = read_matlab_int(args.voids)
    if args.vessels is None and args.clusters is None and args.voids is None:
        plot_segmentation_results(haloV, density, z=0, trans=False)
    else :
        plot_segmentation_results(haloV, density, [vesselM, clusterM, voidM], z=0,
                              trans=False)

    ###### BIG RED FLAG #######
    ### STOP HERE 
    ### Until I figure out organization of halos vs. density
    sys.exit(0)



    # Put the haloV into a data frame that I can more easily handle
    haloL = []
    for i in range(haloV.shape[0]):
        #lst = [haloV[i][0], haloV[i][1], haloV[i][2], haloV[i][3], haloV[i][4]]
        haloL.append(list(haloV[i]))
    df = pd.DataFrame(haloL)
    # Strip out spaces, make lower case
    header = [string.split(' ')[0].lower() for string in halos['metadata'].item()['headers']]
    units = halos['metadata'].item()['units']
    
    df.columns = header
    # Only plot from 0 -> zthresh
    zthresh = 1000     # kpc/h
    subDF = df[df['z'] < zthresh]
    #slab = 

    fig = plt.figure()
    gs = fig.add_gridspec(1,1)
    ax = fig.add_subplot(gs[0,0])
    ax.scatter(subDF['x'], subDF['y'], s=np.log10(np.max(subDF['mass'])+2)/10000)
    ax.set_title("{:<.2f}kpc/h slab in z-axis".format(zthresh))

    print('Subset = {}'.format(subDF.shape))
    plt.show()

    fout.close()
    sys.exit(0)

if __name__ == "__main__":
    main()
