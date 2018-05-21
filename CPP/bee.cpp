//
// Created by alexander on 29.04.18.
//

#define DEBUG
#include <debug.h>

#include <vector>
#include <random>
#include <cstdint>
#include <cmath>
#include <functional>
#include <iterator>
#include <iomanip>
#include <iostream>
#include <fstream>
#include <algorithm>

#include <omp.h>


#include <bee.hpp>

class Bee {
protected:
    unsigned int size;
    std::vector< double > position;
    std::vector< double > velocity;

    std::vector< double > local_minimum;
    double local_minimum_value;
    std::vector< double > min_bounds;
    std::vector< double > max_bounds;

public:
    Bee(unsigned int size, std::vector< int > position)


};

