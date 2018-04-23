import numpy as np
import pandas as pd

import functools
import itertools

import random
import tqdm

import multiprocessing
import threading


# One bee in R^n
class Bee(object):

    def __init__(self, min_bounds, max_bounds, function, sigma, c1, c2):

        # c1 is local
        # c2 is global ideas :-)
        # sigma if analogue of bee mass, 0 < sigma < 1

        self.file = open("{}.log".format(random.randint(1, 10000000000)), "w")

        self.position = np.zeros(min_bounds.shape)
        for i in range(len(min_bounds)):
            self.position[i] = np.random.uniform( min_bounds[i],
                                                  max_bounds[i], 1 )

        self.function = function
        self.velocity = np.random.normal( 0, sigma, len(min_bounds) )
        self.c1 = c1
        self.c2 = c2
        self.local_minimum = self.position
        self.local_minimum_value = self.function( self.local_minimum)
        self.min_bounds = min_bounds[:]
        self.max_bounds = max_bounds[:]


    def calculate_next_velocity(self, global_minimum, w):
        r1, r2 = np.random.uniform(0, 1, 2)

        self.velocity = self.velocity * w + \
                    self.c1 * r1 * (self.local_minimum - self.position) + \
                    self.c2 * r2 * (global_minimum - self.position)


    def move(self):

        self.file.write("{}, {}\n".format(self.position[0], self.position[1]))
        self.file.flush()

        self.position += self.velocity
        fc = self.function(self.position)

        if fc < self.local_minimum_value:
            self.local_minimum_value = fc
            self.local_minimum = self.position

        # print(self.position, self.local_minimum, self.local_minimum_value, self.function(self.position))

        return (self.local_minimum, self.local_minimum_value)


class BeeColony():

    def __init__(self, n_bees, min_bounds, max_bounds,
                 function, n_iter, weight):

        # The magic constants here
        self.w = weight

        self.bees = [ Bee(min_bounds, max_bounds, function, 5, 0.5, 0.2)
                     for i in range(n_bees) ]
        self.n_iter = n_iter
        self.min_bounds = min_bounds[:]
        self.max_bounds = max_bounds[:]

        self.global_minimum = max_bounds[:]
        self.global_minimum_value = function(self.global_minimum)


    def run(self):

        self.global_minimum = self.max_bounds[:]
        self.global_minimum_value = f(self.global_minimum)

        for it in range(self.n_iter):

            print('Iteration:', it)
            local = []

            for bee in self.bees:
                bee.calculate_next_velocity(self.global_minimum, self.w)

                retval = bee.move()
                local.append(retval)

            local.sort(key=lambda x: x[1])

            self.global_minimum, self.global_minimum_value = local[0]

            print("Global minimum:", self.global_minimum,\
                  " value:", self.global_minimum_value )
            print('-' * 60)
            #input()



from function import function as f


if __name__ == "__main__":

    print (f([5, 9])  )

    min_bounds = np.array([ -200, -200 ])
    max_bounds = np.array([  200,  200 ])

    b = BeeColony(8, min_bounds, max_bounds, f, n_iter=1000, weight=0.4 )

    b.run()

    #
















