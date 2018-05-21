import numpy
import random
import math

import functools
import itertools
import multiprocessing
import threading



class Bee(object):

    #################################################################
    #  Initial function of Bee
    #
    # function - function to minimize (np.array -> float)
    # min_bounds - min corner of parallelepiped
    # max_bounds - max corner of parallelepiped
    # sigma - dispersion of initial velocities
    #
    ################################################################
    def __init__(self, function, min_bounds, max_bounds, sigma):

        self.function = function
        self.position = numpy.zeros(min_bounds.shape[0])

        for i in range(min_bounds.shape[0]):
            self.position[i] = numpy.random.uniform(
                min_bounds[i], max_bounds[i], 1)

        self.velocity = numpy.random.normal(0, sigme, min_bounds.shape[0])

        self.local_minimum = numpy.copy(self.position)
        self.local_minimum_value = self.function(self.local_minimum)

        self.min_bounds = numpy.copy(min_bounds)
        self.max_bounds = numpy.copy(max_bounds)


    ################################################################
    # This function calculates velocity of the next step
    #
    # global_minimum - global_minimum, founded by algorithm (numpy.array)
    # weight - current weight of bee (float between 0 and 1)
    # local_attraction - coefficient of attration to local minimum
    #                                               (float between 0 and 1)
    # global_attraction - coefficient ogf attration to global minimum
    #                                               (float between 0 and 1)
    #
    ################################################################
    def calculate_next_velocity(self, global_minimum, weight,
                                local_attraction, global_attraction):

        local_speed, global_speed = numpy.random.uniform(0, 1, 2)

        # vector to pointed to local minimum
        to_local = (self.local_minimum - self.position)

        #vector poited to global minimum
        to_global = (global_minimum - self.position)

        # calculation of the next velocity
        self.velocity = self.velocity * weight +
            local_attraction * local_speed * to_local +
            global_attraction * global_speed * to_global


    ################################################################
    # This function moves the Bee
    #
    # No arguments
    #
    ################################################################
    def move(self):

        self.position += self.velocity

        # checking bounds
        self.position = numpy.minimum(self.position, self.max_bounds)
        self.position = numpy.maximum(self.position, self.min_bounds)

        fc = self.function(self.position)

        if fc < self.local_minimum_value:
            self.local_minimum_value = fc
            self.local_minimum = np.copy(self.position)

        return (self.local_minimum, self.local_minimum_value)




