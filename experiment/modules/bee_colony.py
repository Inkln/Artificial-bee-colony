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
        
        self.position = np.zeros(min_bounds.shape)
        for i in range(len(min_bounds)):
            self.position[i] = np.random.uniform(min_bounds[i],
                                                 max_bounds[i], 1)
        
        self.function = function
        self.velocity = np.random.normal(0, sigma, len(min_bounds))
        self.c1 = c1
        self.c2 = c2
        
        self.sigma = sigma
        
        self.local_minimum = np.copy(self.position)
        self.local_minimum_value = self.function(self.local_minimum)
        
        self.min_bounds = min_bounds[:]
        self.max_bounds = max_bounds[:]

        # self.counter = 0
    
    def calculate_next_velocity(self, global_minimum, w):
        
        r1, r2 = np.random.uniform(0, 1, 2)
        
        to_local = (self.local_minimum - self.position)
        # to_local /= np.linalg.norm(to_local, ord=2) + 0.01
        # to_local *= 10
        
        to_global = global_minimum - self.position
        #
        # to_global /= np.linalg.norm(to_global, ord=2) + 0.01
        # to_global *= 10
        
        self.velocity = self.velocity * w + self.c1 * r1 * to_local + \
                        self.c2 * r2 * to_global + \
                        np.random.normal(0, np.linalg.norm(self.velocity) / 3 + 1, 2)

        # if (self.position == global_minimum).all():
        #    self.counter += 1

        # if self.counter == 5:
        #    self.counter = 0
        #    self.position = np.zeros(min_bounds.shape)
        #    for i in range(len(min_bounds)):
        #        self.position[i] = np.random.uniform( min_bounds[i],
        #                                              max_bounds[i], 1 )
        
        #    self.velocity = np.random.normal( 0, self.sigma, len(min_bounds) )
    
    def move(self):
        
        self.position += self.velocity
        
        self.position = np.minimum(self.position, self.max_bounds)
        self.position = np.maximum(self.position, self.min_bounds)
        
        fc = self.function(self.position)
        
        if fc < self.local_minimum_value:
            self.local_minimum_value = fc
            self.local_minimum = np.copy(self.position)
        
        return (self.local_minimum, self.local_minimum_value)


class BeeColony():
    
    def __init__(self, n_bees, min_bounds, max_bounds,
                 function, n_iter, weight):
        
        # The magic constants here
        self.w = weight
        
        self.bees = [Bee(min_bounds, max_bounds, function, 10, 0.2, 0.05)
                     for i in range(n_bees)]
        self.n_iter = n_iter
        self.min_bounds = min_bounds[:]
        self.max_bounds = max_bounds[:]
        
        self.global_minimum = np.zeros(min_bounds.shape)
        # for i in range(len(min_bounds)):
        #    self.global_minimum[i] = np.random.uniform( min_bounds[i], max_bounds[i], 1 )
        
        self.global_minimum_value = function(self.global_minimum)
        
        self.function = function
    
    def run(self):
        
        coords = []
        
        for it in list(range(self.n_iter)):
            
            # print('Iteration:', it)
            local = []
            
            for bee in self.bees:
                bee.calculate_next_velocity(self.global_minimum, self.w)
                
                retval = bee.move()
                local.append(retval)
            
            local.sort(key=lambda x: x[1])
            
            if local[0][1] < self.global_minimum_value:
                self.global_minimum, self.global_minimum_value = local[0][0], local[0][1]
            
            tmp = [np.copy(bee.position) for bee in self.bees] + [self.global_minimum_value]
            
        return np.array(coords)