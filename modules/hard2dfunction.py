import numpy as np
import pandas as pd
import math
import random

class Hard2dFunction:
    # This class provides the ability to generate functions of two arguments

    def __init__(self):
        self.generate_new_coefficients()


    # This method builds new function
    def generate_new_coefficients(self):
        self.p1 = np.random.uniform(-0.8, -0.1, 1)
        self.p2 = np.random.uniform(0.1, 0.8, 1)
        self.p3, self.p4, self.p5 = np.random.uniform(0.05, 0.6, 3)
        self.p6, self.p7, self.p8 = np.random.uniform(100, 400, 3)
        self.p9, self.p10 = np.random.uniform(0, 0.00002, 2)


    # This method calls function for one argument (np.array)
    def __call__(self, x):

        result = 418.9829 * len(x)

        for i in range(len(x)):
            result += ( -(abs(x[i]) + 1) ** (self.p1) * \
                       np.sin( np.abs( x[i] ) ** self.p2  ) * x[i] )

            n = np.linalg.norm(x, ord=2)

        return  (-result * (1 + np.sin(x[1] / self.p6) * self.p3 + \
                           np.sin(x[0] / self.p7) * self.p4 + \
                           np.cos(n / self.p8) * self.p5  ) \
                            + (x[0] ** 2) * self.p9 + (x[1] ** 2) * self.p10)[0] + 3000


    # This method returns the numeric lattice on lx, ly - coordinate linscpace
    def get_lattice(self, lx: np.array, ly: np.array):

        xx, yy = np.meshgrid(lx, ly)
        zz = np.zeros(xx.shape)

        for i in range(zz.shape[0]):
            for j in range(zz.shape[1]):
                zz[i, j] = self.__call__([ xx[i, j], yy[i, j] ])

        return xx, yy, zz


    # This method dumps the coefficients into string
    def __str__(self):
        s = "1:{}  2:{}  3:{}  4:{}  5:{}  6:{}  7:{}  8:{}  9:{}  10:{}" \
            .format(self.p1, self.p2, self.p3, self.p4, self.p5, self.p5, \
                    self.p6, self.p7, self.p8, self.p9, self.p10)
        return s

