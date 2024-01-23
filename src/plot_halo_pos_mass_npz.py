# Author : Ali Snedden
# Date   : 22-january-2024
# 
#
#
import sys
import argparse
import numpy as np
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
    #parser.add_argument('--output', metavar='output', type=str,
    #                    help='')
    args = parser.parse_args()
    data = np.load(args.data)
    #fout = open(args.output, "w+")
    nx = data.shape[0]
    ny = data.shape[1]
    nz = data.shape[2]
    #fout.write("# vtk DataFile Version 1.0. next line is dim[]... Dx=change"
    #           "column, Dy=each row, Dz=every dim[0] rows\n")
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
