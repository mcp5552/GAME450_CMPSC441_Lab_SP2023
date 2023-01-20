''' 
Lab 2: Cities and Routes

In the final project, you will need a bunch of cities spread across a map. Here you 
will generate a bunch of cities and all possible routes between them.
'''
import random

#random.randint(a,b) <- returns random int between range a and b
import itertools
#itertools 
# a = [1, 2, 3] 
# combinations = itertools.combinations(a, 2)
# print(list(combinations))

def get_randomly_spread_cities(size, n_cities):
    """
    > This function takes in the size of the map and the number of cities to be generated 
    and returns a list of cities with their x and y coordinates. The cities are randomly spread
    across the map.
    
    :param size: the size of the map as a tuple of 2 integers
    :param n_cities: The number of cities to generate
    :return: A list of cities with random x and y coordinates.
    """

    city_locations = [] 

    for z in range(0, n_cities):
        #assign random x and y values 
        city_locations.append((random.randint(0,size[0]),random.randint(0,size[1]))) #append a tuple with random x & y

    return city_locations



def get_routes(city_names):
    """
    It takes a list of cities and returns a list of all possible routes between those cities. 
    Equivalently, all possible routes is just all the possible pairs of the cities. 
    
    :param city_names: a list of city names
    :return: A list of tuples representing all possible links between cities/ pairs of cities, 
            each item in the list (a link) represents a route between two cities.
    """

    route_list = []

    for i in range(0, len(city_names)):
        for j in range(i+1, len(city_names)):
            route_list.append((city_names[i],city_names[j]))

    return route_list

# TODO: Fix variable names
if __name__ == '__main__':
    city_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    '''print the cities and routes'''
    city_locations = get_randomly_spread_cities((100, 200), len(city_names)) #city_locations (list of tuples) [(x1, y1), (x2, y2)...]
    routes = get_routes(city_names)
    print('Cities:')
    for i, city in enumerate(city_locations):
        print(f'{city_names[i]}: {city}')
    print('Routes:')
    for i, route in enumerate(routes):
        print(f'{i}: {route[0]} to {route[1]}')
