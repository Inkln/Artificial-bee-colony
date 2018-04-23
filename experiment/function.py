import numpy as np
import sympy as sp

import functools

def function(x):
    result = 418.9829 * len(x)

    for i in range(len(x)):
        result += ( -x[i] * np.sin( np.sqrt( np.abs( x[i] ) ) ) ) 

    return result 

def get_lattice(l1, l2):
    xx, yy = np.meshgrid(l1, l2)
    zz = np.zeros(xx.shape)
    for i in range(zz.shape[0]):
        for j in range(zz.shape[1]):
            zz[i, j] = function( [ xx[i, j], yy[i, j] ]  )
    return zz
