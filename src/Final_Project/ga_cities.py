""" ga_cities.py
Has methods for instantiating a genetic algorithm and evaluating generations of the algorithm
with a fitness function

contains:
    game_fitness(cities, idx, elevation, size)
    setup_GA(fitness_fn, n_cities, size)
    solution_to_cities(solution,size)
    generate_elevation(size)
    show_cities(cities, landscape_pic, cmap="gist_earth")
"""

import matplotlib.pyplot as plt
import pygad #needs to be version 2.18 
import numpy as np
from perlin_noise import PerlinNoise

import sys
from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / ".." / "..").resolve().absolute()))

from landscape import elevation_to_rgba

""" game_fitness(cities, idx, elevation, size)
Determines the fitness of some city distribution based on the elevations of cities """
def game_fitness(cities, idx, elevation, size): #input 1 of game_fitness() is actually (list of grid cell numbers), not cities
    max_height = .7 
    min_height = .35
    fitness = 1  # Do not return a fitness of 0, it will mess up the algorithm.
    city_coords = solution_to_cities(cities, size)
    #for all cities, check the elevation, if any are out of bounds then decrease fitness 
    for i in range(len(cities)):
        current_elevation = elevation[city_coords[i][1]][city_coords[i][0]]
        if current_elevation < min_height:
           fitness = 0.0001
           #break
        if current_elevation > max_height:
            fitness = 0.0001
           #break
    return fitness

""" setup_GA(fitness_fn, n_cities, size)
Sets up the genetic algorithm with the given fitness function,
number of cities, and size of the map
:param fitness_fn: The fitness function to be used
:param n_cities: The number of cities in the problem
:param size: The size of the grid
:return: The fitness function and the GA instance. """
def setup_GA(fitness_fn, n_cities, size):
    num_generations = 100
    num_parents_mating = 10 #initially 10
    solutions_per_population = 300 #initially 300
    num_genes = n_cities
    init_range_low = 0
    init_range_high = size[0] * size[1]
    parent_selection_type = "sss"
    keep_parents = 10
    crossover_type = "single_point"
    mutation_type = "random"
    mutation_percent_genes = 10

    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,
        fitness_func=fitness_fn,
        sol_per_pop=solutions_per_population,
        num_genes=num_genes,
        gene_type=int,
        init_range_low=init_range_low,
        init_range_high=init_range_high,
        parent_selection_type=parent_selection_type,
        keep_parents=keep_parents,
        crossover_type=crossover_type,
        mutation_type=mutation_type,
        mutation_percent_genes=mutation_percent_genes,
    )

    return fitness_fn, ga_instance

"""solution_to_cities(solution,size)
Takes a GA solution and size of the map, and returns the city coordinates
in the solution.
:param solution: a solution to GA
:param size: the size of the grid/map
:return: The cities as a list of lists."""
def solution_to_cities(solution, size):
    cities = np.array(
        list(map(lambda x: [int(x / size[0]), int(x % size[1])], solution))
    )
    return cities

"""show_cities(cities, landscape_pic, cmap="gist_earth")
It takes a list of cities and a landscape picture, and plots the cities on top of the landscape
:param cities: a list of (x, y) tuples
:param landscape_pic: a 2D array of the landscape
:param cmap: the color map to use for the landscape picture, defaults to gist_earth (optional) """
def show_cities(cities, landscape_pic, cmap="gist_earth"):
    cities = np.array(cities)
    plt.imshow(landscape_pic, cmap=cmap)
    plt.plot(cities[:, 1], cities[:, 0], "r.")
    plt.show()

"""generate_elevation(size)
generates an elevation numpy array using perlin noise """
def generate_elevation(size):
    xpix, ypix = size
    noise = PerlinNoise(octaves=6, seed=3)
    elevation = np.array([[noise([i/xpix, j/ypix]) for j in range(ypix)] for i in range(xpix)])
    return elevation

if __name__ == "__main__":
    print("Initial Population")
    size = 100, 100
    n_cities = 10
    elevation = generate_elevation(size) #use perlin noise to create elevation map
    elevation = np.array(elevation)
    # normalize landscape
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())
    landscape_pic = elevation_to_rgba(elevation) #create image of elevation map 

    # setup fitness function and GA
    fitness = lambda cities, idx: game_fitness(cities, idx, elevation=elevation, size=size)
    fitness_function, ga_instance = setup_GA(fitness, n_cities, size)

    # Show one of the initial solutions.
    cities = ga_instance.initial_population[0]
    cities = solution_to_cities(cities, size)
    show_cities(cities, landscape_pic)

    # Run the GA to optimize the parameters of the function.
    ga_instance.run()
    ga_instance.plot_fitness()
    print("Final Population")

    # Show the best solution after the GA finishes running.
    cities = ga_instance.best_solution()[0]
    cities_t = solution_to_cities(cities, size)
    plt.imshow(landscape_pic, cmap="gist_earth")
    plt.plot(cities_t[:, 1], cities_t[:, 0], "r.")
    plt.show()
    print(fitness_function(cities, 0))
