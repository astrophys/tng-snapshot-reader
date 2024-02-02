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
import matplotlib.pyplot as plt

def main():
    """

    Args:

    Returns:

    Raises:
    """
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--data', metavar='halo_pos_mass.npz', type=str,
                        help='Input npy file')
    parser.add_argument('--vessels', metavar='output', type=str,
                        help='')
    parser.add_argument('--clusters', metavar='output', type=str,
                        help='')
    parser.add_argument('--voids', metavar='output', type=str,
                        help='')
    #parser.add_argument('--output', metavar='output', type=str,
    #                    help='')
    args = parser.parse_args()
    npz = np.load(args.data, allow_pickle=True)
    dataV = npz['data']         # This is an ugly np.vector of tuples, let's rework this
    #
    vesselM = read_matlab_int(args.vessels)
    clusterM = read_matlab_int(args.clusters)
    voidM = read_matlab_int(args.voids)
    
    # Put the dataV into a data frame that I can more easily handle
    dataL = []
    for i in range(dataV.shape[0]):
        #lst = [dataV[i][0], dataV[i][1], dataV[i][2], dataV[i][3], dataV[i][4]]
        dataL.append(list(dataV[i]))
    df = pd.DataFrame(dataL)
    # Strip out spaces, make lower case
    header = [string.split(' ')[0].lower() for string in npz['metadata'].item()['headers']]
    units = npz['metadata'].item()['units']
    
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

    fout = open("{}.NDfield_ascii".format(args.output), "w+")
    # Header
    fout.write("ANDFIELD COORDS\n")
    fout.write("3 {}\n".format(subDF.shape[0]))
    for index, row in subDF.iterrows():
        fout.write("{} {} {}\n".format(row['x'], row['y'], row['z']))
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
