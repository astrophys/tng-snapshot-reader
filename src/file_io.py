# Author : Ali Snedden
# Date   : 22-january-2024
# 
#
#
import sys
import numpy as np


def read_matlab_int(path : str) -> np.ndarray :
    """Reads in text file in matlab_int format and puts it into a numpy array

    Args:
        path : str, path to the file

    Returns:
        dataM : np.ndarray, numpy array with 3D data from file

    Raises:
        ValueError : when comments are misplaced or not all values in file are read
    """
    fin = open(path, "r")
    lidx = 0                            # index to track which line we are on
    i = 0
    j = 0
    k = 0
    for line in fin:
        # First two lines are metadata or comments 
        if line[0] == '#' and lidx >= 2:
            raise ValueError("ERROR!! I'm not sure why there are comments after the "
                             "first two lines. See line {}".format(lidx))
        # commetn
        if lidx == 0 :
            comment = line
        # size
        elif lidx == 1 :
            line = line.strip()
            sizeL = line.split(' ')
            sizeL = [int(x) for x in sizeL]
            dataM = np.zeros(sizeL, dtype=np.float64)
        # Actual data    
        else :
            line = line.strip()
            lineL= line.split(' ')
            lineL= [float(x) for x in lineL]
            
            # loop over x
            for i in range(sizeL[0]):
                dataM[i,j,k] = float(lineL[i])
            if j == sizeL[1] - 1:
                j = 0
                k += 1
            else :
                j += 1
        lidx += 1
    if i != sizeL[0] -1 or j != sizeL[1] or k != sizeL[2]:
        raise ValueError("ERROR!! ({}, {}, {}) != ({}, {}, {})".format(i, j, k, sizeL[0],
                                                                       sizeL[1], sizeL[2]))
    fin.close()
    return dataM


