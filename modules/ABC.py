import numpy
import random
import math

import functools
import itertools
import multiprocessing
import threading
import tqdm


class Bee(object):

    #################################################################
    #  Initial function of Bee
    #
    # function - function to minimize (numpy.array -> float)
    # min_bounds - min corner of parallelepiped
    # max_bounds - max corner of parallelepiped
    # sigma - dispersion of initial velocities
    #
    ################################################################
    def __init__(self, function, min_bounds, max_bounds):

        self.function = function
        self.position = numpy.zeros(min_bounds.shape[0])

        for i in range(min_bounds.shape[0]):
            self.position[i] = numpy.random.uniform(
                min_bounds[i], max_bounds[i], 1)

        self.velocity = numpy.zeros(shape=min_bounds.shape)

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
    # global_attraction - coefficient of attration to global minimum
    #                                               (float between 0 and 1)
    # sigma - speed random dispersion
    #
    ################################################################
    def calculate_next_velocity(self, global_minimum, weight,
                                local_attraction, global_attraction, sigma):

        local_speed, global_speed = numpy.random.uniform(0, 1, 2)

        # vector to pointed to local minimum
        to_local = (self.local_minimum - self.position)

        #vector poited to global minimum
        to_global = (global_minimum - self.position)

        # calculation of the next velocity
        self.velocity = self.velocity * weight +\
            local_attraction * local_speed * to_local +\
            global_attraction * global_speed * to_global +\
            numpy.random.normal(0, sigma, 2)

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

        if fc <= self.local_minimum_value:
            self.local_minimum_value = fc
            self.local_minimum = numpy.copy(self.position)

        return [numpy.copy(self.position), numpy.copy(self.local_minimum),
                self.local_minimum_value]

    ################################################################
    # Technical methods

    def __str__(self):
        s = 'pos: {}, vel: {}'.format(self.position, self.velocity)





class BeeColony(object):


    ################################################################
    # This is constructor of colony
    #
    # n_bees - the number of bees in colony (int)
    # min_bounds, max_bounds - the bounds of optimiztion area
    # function - function to optimize
    # n_iter - the number of iteration for one epoch (int)
    # weight_generator - lambda expression to geneerate current
    #           weight from the number of the current iteration
    #           (int->float)
    # local_attraction_generator - lambda expression to generate
    #           local_attraction from the number of the current
    #           iteration (int -> float)
    # global_attraction_generator - lambda expression to generate
    #           global_attraction from the number of the current
    #           iteration (int -> float)
    # sigma_generator - lambda exression to generate speed dispersion
    #           from the number of the current iteration
    #           (int -> float)
    #
    ################################################################
    def __init__(self, function, min_bounds, max_bounds,
                 n_bees=10, n_iter=100,
                 weight_generator=lambda n: 0.9,
                 local_attraction_generator=lambda n: 0.2,
                 global_attraction_generator=lambda n: 0.1,
                 sigma_generator=lambda n: 10):

        self.weight_generator = weight_generator
        self.local_attraction_generator = local_attraction_generator
        self.global_attraction_generator = global_attraction_generator
        self.sigma_generator = sigma_generator
        self.function = function

        self.min_bounds = numpy.copy(min_bounds)
        self.max_bounds = numpy.copy(max_bounds)

        self.n_iter = n_iter
        self.n_bees = n_bees

        self.bee_array = [ Bee(self.function, self.min_bounds, \
                               self.max_bounds) for i in range(self.n_bees) ]

        self.global_minimum = numpy.copy(self.bee_array[0].position)
        self.global_minimum_value = self.function(self.global_minimum)


    ################################################################
    # This methos begins the algorithm, without different debug or
    # another information
    #
    ################################################################
    def run_clear(self):

        progress_bar = tqdm.tqdm(list(range(self.n_iter)))


        for iteration in progress_bar:

            progress_bar.set_description_str('{}'.format(
                round(self.global_minimum_value, 4)))

            cached_global_minimum = numpy.copy(self.global_minimum)

            for bee in self.bee_array:
                bee.calculate_next_velocity(
                    cached_global_minimum,
                    self.weight_generator(iteration),
                    self.local_attraction_generator(iteration),
                    self.global_attraction_generator(iteration),
                    self.sigma_generator(iteration))
                retval = bee.move()

                if retval[2] <= self.global_minimum_value:
                    self.global_minimum = numpy.copy(retval[1])
                    self.global_minimum_value = retval[2]

        return (self.global_minimum_value, self.global_minimum)


    ################################################################
    # This methods returns trjaectories of all bees
    #
    ################################################################
    def run_trajectories(self):

        progress_bar = tqdm.tqdm(list(range(self.n_iter)))

        trajectories = []
        global_min = []

        for iteration in progress_bar:

            progress_bar.set_description_str('traj:{}'.format(
                round(self.global_minimum_value, 4)))

            cached_global_minimum = numpy.copy(self.global_minimum)

            local = []

            for bee in self.bee_array:
                bee.calculate_next_velocity(
                    cached_global_minimum,
                    self.weight_generator(iteration),
                    self.local_attraction_generator(iteration),
                    self.global_attraction_generator(iteration),
                    self.sigma_generator(iteration))
                retval = bee.move()
                local.append([numpy.copy(retval[0]), \
                              numpy.copy(bee.local_minimum)])

                if retval[2] <= self.global_minimum_value:
                    self.global_minimum = numpy.copy(retval[1])
                    self.global_minimum_value = retval[2]

            trajectories.append(local)
            global_min.append(numpy.copy(self.global_minimum))

        return numpy.array(trajectories), numpy.array(global_min)




