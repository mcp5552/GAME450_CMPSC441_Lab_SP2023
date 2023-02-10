'''
Lab 5: PCG and Project Lab

This a combined procedural content generation and project lab. 
You will be creating the static components of the game that will be used in the project.
Use the landscape.py file to generate a landscape for the game using perlin noise.
Use the lab 2 cities_n_routes.py file to generate cities and routes for the game.
Draw the landscape, cities and routes on the screen using pygame.draw functions.
Look for triple quotes for instructions on what to do where.
The intention of this lab is to get you familiar with the pygame.draw functions, 
use perlin noise to generate a landscape and more importantly,
build a mindset of writing modular code.
This is the first time you will be creating code that you may use later in the project.
So, please try to write good modular code that you can reuse later.
You can always write non-modular code for the first time and then refactor it later.
'''

import sys
import pygame
import random
import numpy as np
from landscape import get_landscape

from pathlib import Path
sys.path.append(str((Path(__file__)/'..'/'..').resolve().absolute()))
from lab2.cities_n_routes import get_randomly_spread_cities, get_routes


# TODO: Demo blittable surface helper function

''' Create helper functions here '''
def get_landscape_surface(size):
    landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3]) 
    return pygame_surface

if __name__ == "__main__":
    pygame.init()
    size = width, height = 640, 480
    black = 1, 1, 1
    screen = pygame.display.set_mode(size)
    pygame_surface = get_landscape_surface(size)
    city_names = ['Morkomasto', 'Morathrad', 'Eregailin', 'Corathrad', 'Eregarta',
                  'Numensari', 'Rhunkadi', 'Londathrad', 'Baernlad', 'Forthyr']
    city_number = len(city_names)
    city_locations = get_randomly_spread_cities(size, city_number)
    routes = get_routes(city_names)

    city_locations_dict = {name: location for name, location in zip(city_names, city_locations)}
    random.shuffle(routes)
    routes = routes[:10] 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(black)
        screen.blit(pygame_surface, (0, 0))

        line_color = pygame.Color(100,100,100) 
        line_width = 1; 

        ''' draw cities '''
        city_color = pygame.Color(200,200,200) 
        for i in range(0,len(city_names)):
            pygame.draw.circle(pygame_surface, city_color, city_locations[i],5)

        ''' draw first 10 routes '''
        for i in range (0,9):
            start_city = routes[i][0]  #string
            end_city = routes[i][1] #string
            start_coords = city_locations_dict[start_city]
            end_coords = city_locations_dict[end_city]
            pygame.draw.line(pygame_surface, line_color, start_coords, end_coords, line_width)

        pygame.display.flip()
