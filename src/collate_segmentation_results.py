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
    parser.add_argument('--vessels', metavar='output', type=str,
                        help='')
    parser.add_argument('--clusters', metavar='output', type=str,
                        help='')
    parser.add_argument('--voids', metavar='output', type=str,
                        help='')
    #parser.add_argument('--output', metavar='output', type=str,
    #                    help='')
    args = parser.parse_args()
    print("Reading : {} ".format(args.data))
    halos = np.load(args.data, allow_pickle=True)
    density = np.load(args.density, allow_pickle=True)
    haloV = halos['data']         # This is an ugly np.vector of tuples, let's rework this
    #
    print("Reading : {} ".format(args.vessels))
    vesselM = read_matlab_int(args.vessels)
    print("Reading : {} ".format(args.clusters))
    clusterM = read_matlab_int(args.clusters)
    print("Reading : {} ".format(args.voids))
    voidM = read_matlab_int(args.voids)
    plot_segmentation_results(haloV, desnity, [vesselM, clusterM, voidM], z=0)
    
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

    ### 12-feb-2024
    # Not sure where / why I put this in here
    # This is the format used by Disperse
    ##fout = open("{}.NDfield_ascii".format(args.output), "w+")
    ### Header
    ##fout.write("ANDFIELD COORDS\n")
    ##fout.write("3 {}\n".format(subDF.shape[0]))
    ##for index, row in subDF.iterrows():
    ##    fout.write("{} {} {}\n".format(row['x'], row['y'], row['z']))
    #fout.write("%i %i %i\n"%(nx,ny,nz))

    #for k in range(0, nz):
    #    for j in range(0, ny):
    #        for i in range(0, nx):
    #            fout.write("{:<.4e} ".format(data[i,j,k]))
    #        fout.write("\n")
    #print("Finished outputting : %s"%(args.output))
    fout.close()
    sys.exit(0)

if __name__ == "__main__":
    main()
