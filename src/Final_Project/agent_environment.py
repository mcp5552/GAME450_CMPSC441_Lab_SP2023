""" agent_environment.py
creates the game and battle maps and contains the main gameplay loop 

contains:
    get_landscape_surface(size)
    get_combat_surface(size)
    setup_window(width, height, caption)
    displayCityNames(city_locations, city_names)
        Class State (defined in main)
"""

#TODO: 
# money values are sometimes not rounded nicely  
# maybe route costs are not rounded and this 
# y/n for choosing a route 
# genetic algorithm for city placement 

import sys
import pygame
import random
from chatGPT import getResponse
from sprite import Sprite
from pygame_combat import run_pygame_combat
from pygame_human_player import PyGameHumanPlayer
from landscape import get_landscape, get_combat_bg
from landscape import get_elevation, elevation_to_rgba #trying to add elevation chekcking for routes 
from travel_cost import get_route_cost
from pygame_ai_player import PyGameAIPlayer

from pathlib import Path
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))
from cities_n_routes import get_randomly_spread_cities, get_routes

pygame.font.init()
game_font = pygame.font.SysFont("Bradley Hand ITC", 17)

""" get_landscape_surface(size)
Uses get_landscape, which uses elevation_to_rgba() on get_elevation()
param: size, a tuple of two integers"""
def get_landscape_surface(size):
    landscape = get_landscape(size) 
    #print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface

def get_combat_surface(size):
    landscape = get_combat_bg(size)
    #print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface

def setup_window(width, height, caption):
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return window


def displayCityNames(city_locations, city_names):
    for i, name in enumerate(city_names):
        text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
        screen.blit(text_surface, city_locations[i])

class State:
    def __init__(
        self,
        current_city,
        destination_city,
        travelling,
        encounter_event,
        cities,
        routes,
        money,
        new_money,
        journal,
        journal_entry_produced,
        encounter_cnt
    ):
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes
        self.money = money
        self.new_money = new_money
        self.journal = journal 
        self.journal_entry_produced = journal_entry_produced,
        self.encounter_cnt = encounter_cnt 

if __name__ == "__main__":
    size = width, height = 640, 480
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    sprite_path = "assets/lego.png"
    sprite_speed = 1
    money = random.randint(20,70)
    new_money = 0
    journal = []
    screen = setup_window(width, height, "Journey to Evereska")

    elevation = get_elevation(size)  #Added this, trying to add elevation checking for routes 
    landscape = elevation_to_rgba(elevation) 
    landscape_surface = pygame.surfarray.make_surface(landscape[:, :, :3])

    #next line should not be necessary
    #landscape_surface = get_landscape_surface(size)

    combat_surface = get_combat_surface(size)
    
    city_names = [
        "Loudwater",
        getResponse("Generate a medieval-sounding city name, make it sound Dwarvish").replace("\n", ""),
        getResponse("Generate a medieval-sounding city name, make it sound Orcish").replace("\n", ""),
        getResponse("Generate a medieval-sounding city name, make it sound French").replace("\n", ""),
        getResponse("Generate a medieval-sounding city name, make it sound Elvish").replace("\n", ""),
        getResponse("Generate a medieval-sounding city name, make it sound Dwarvish").replace("\n", ""),
        getResponse("Generate a medieval-sounding city name, make it sound English").replace("\n", ""),
        getResponse("Generate a medieval-sounding city name, make it sound Orcish").replace("\n", ""),
        getResponse("Generate a medieval-sounding city name, make it sound Norewegian").replace("\n", ""),
        "Evereska",
    ]

    cities = get_randomly_spread_cities(size, len(city_names)) #list of (x,y) tuples
    routes = get_routes(cities) #list of 2-tuples of (x,y) tuples
    random.shuffle(routes) #randomize routes
    routes = routes[:10] #only keep 10 random routes 

    route_costs = []
    for i, route in enumerate(routes):
        #get route cost using elevation map and route tuples. Ignore negatives, round to nearest 100th 
        route_costs.append(round(max(0,get_route_cost(routes[i], elevation),2)))

    player_sprite = Sprite(sprite_path, cities[start_city])
    
    #Set player of game to either human or AI
    player = PyGameHumanPlayer()
    #player = PyGameAIPlayer() 

    state = State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=cities,
        routes=routes,
        money=money,
        new_money = new_money,
        journal=journal,
        journal_entry_produced=True,
        encounter_cnt = 0
    )
    
    print("\nWelcome to Journey to Evereska!") 
    print("You must reach the city of Evereska without running out of money. Traveling between cities costs money.") 
    print("If you are attacked by bandits you must defeat them.")
    print("You now have £" + str(state.money))
    print("What city do you want to travel to? (Use numbers 0-9)")

    while True: #main gameplay loop
        money_text = "Money: £" + str(state.money) 
        if state.money <= 0.0:
            print("You ran out of money!")
            break

        action = player.selectAction(state)

        if 0 <= int(chr(action)) <= 9:
            if int(chr(action)) != state.current_city and not state.travelling: 
                route1 = (cities[state.current_city], cities[int(chr(action))]) #tuple for start to dest city
                route2 = (cities[int(chr(action))], cities[state.current_city]) #tuple for dest to start city
                
                true_route = () #have to account for that the actual route could be in the list in either order 
                if route1 in routes: 
                    true_route = route1
                if route2 in routes:
                    true_route = route2 

                if true_route in routes:  #if the (start city coords, end city coords) tuple is in routes list
                    route_cost = route_costs[routes.index(true_route)]
                    print("The route you chose costs " + str(route_cost) + ".")
                    print("Do you want to take that route? (y/n) ")
                    choice = player.selectAction(state)

                    #checking y/n doesnt work because it repeatedly returns numbers 0-9 
                    while chr(choice) != "y" or chr(choice) != "n":  #lock the program and wait for y/n input
                        choice = player.selectAction(state)
                        if chr(choice) == "y": #
                            pass
                        elif chr(choice) == "n":
                            continue

                    state.money -= route_cost #reduce money by cost of route
                    #index of that route in routes will serve for looking up cost 
                    start = cities[state.current_city] 
                    state.destination_city = int(chr(action))
                    destination = cities[state.destination_city]
                    player_sprite.set_location(cities[state.current_city])
                    state.travelling = True
                    print(
                        "Travelling from", city_names[state.current_city], "to", city_names[state.destination_city]
                    )
                else:
                    print("There is no route from " + city_names[state.current_city], "to", city_names[int(chr(action))]+ "!")
        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))

        text_surface = game_font.render(money_text, True, (210, 210, 210)) #Print money on screen this isn't working ? 
        screen.blit(text_surface, (10, 10))

        for city in cities:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for line in routes:
            pygame.draw.line(screen, (255, 0, 0), *line) #draw the line 
        
        displayCityNames(cities, city_names)
        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling: #if you make to the end of the route 
                print('Arrived at', city_names[state.destination_city])
                print("You now have " + "£" + str(state.money))
                state.journal_entry_produced=False

        if not state.journal_entry_produced: #if a new journal entry is needed 
            if state.encounter_cnt == 0: #if there were no encounters 
                state.journal.append(getResponse("Generate a single 1 paragraph journal entry about traveling by foot through the country from a city called" 
                                                 + city_names[state.current_city] + "to one called" + city_names[state.destination_city] + 
                                                 ". Feel free to make up details about the cities. Maybe refer indirectly to the fact that you are an elf from the elf country, and an archer. Mention that you did not encounter any bandits. Write in a medieval style."))
            elif state.encounter_cnt == 1: #if there was 1 encounter
                state.journal.append(getResponse("Generate a single 1 paragraph journal entry about traveling by foot through the country from a city called" 
                                                 + city_names[state.current_city] + "to one called" + city_names[state.destination_city] + 
                                                 ". Feel free to make up details about the cities. Maybe refer indirectly to the fact that you are an elf from the elf country, and an archer. Mention that you encountered a bandit but you defeated him with a bow and arrow and a sword."
                                                  + "Mention that the bandit you killed dropped " + "£" + str(state.new_money) + "Write in a medieval style.")) 
            elif state.encounter_cnt > 1: #if there were multiple encounters 
                state.journal.append(getResponse("Generate a single 1 paragraph journal entry about traveling by foot through the country from a city called" 
                                                 + city_names[state.current_city] + "to a city called" + city_names[state.destination_city] + 
                                                 ". Feel free to make up details about the cities. Mention that you encountered " + str(state.encounter_cnt) 
                                                 + " bandits along the way, but that you managed to defeat the bandits at every encounter with bow and arrow and a sword. Mention that the bandits you killed dropped " + "£" + str(state.new_money) + " altogether. Maybe refer indirectly to the fact that you are an elf from the elf country, and an archer. Write in a medieval style." )) 
            print("Journal updated: " + str(journal[-1]))
            state.journal_entry_produced = True

        if not state.travelling:
            encounter_event = False
            state.encounter_cnt=0
            state.new_money = 0
            state.current_city = state.destination_city

        if state.encounter_event:
            print("You have encountered a bandit!") 
            combat_outcome = run_pygame_combat(combat_surface, screen, player_sprite)
            if combat_outcome == -1: #-1 if lose
                print("You died!")
                break
            elif combat_outcome == 1: #win
                print("You have defeated the bandit!")
                new_money = round(random.uniform(.10, 10.00), 2)
                print("£"+ str(new_money) + " earned!")
                state.money += new_money
                state.new_money += new_money
            elif combat_outcome == 0: #draw
                print("The bandit attacks again!") 
                combat_outcome = run_pygame_combat(combat_surface, screen, player_sprite)
            state.encounter_cnt += 1
            state.encounter_event = False
        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()

        if state.current_city == end_city:
            print('You made it to Evereska! Congratulations, you win!')
            break

    print("Game Over") 
