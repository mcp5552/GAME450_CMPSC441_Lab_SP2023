""" agent_environment.py
creates the game and battle maps and contains the main gameplay loop 

contains:
    get_landscape_surface(size)
    get_combat_surface(size)
    setup_window(width, height, caption)
    displayCityNames(city_locations, city_names)
        Class State (defined in main)
"""

import sys
import pygame
import random
from chatGPT import getResponse
from sprite import Sprite
from pygame_combat import run_pygame_combat
from pygame_human_player import PyGameHumanPlayer
from landscape import get_landscape, get_combat_bg
from pygame_ai_player import PyGameAIPlayer

from pathlib import Path
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))
from cities_n_routes import get_randomly_spread_cities, get_routes

pygame.font.init()
game_font = pygame.font.SysFont("Bradley Hand ITC", 17)

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
    money = 100.0
    journal = []
    screen = setup_window(width, height, "Journey to Evereska")

    landscape_surface = get_landscape_surface(size)
    combat_surface = get_combat_surface(size)
    city_names = [
        "Loudwater",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Evereska",
    ]

    cities = get_randomly_spread_cities(size, len(city_names)) #list of (x,y) tuples
    routes = get_routes(cities) #list of 2-tuples of (x,y) tuples
    random.shuffle(routes) #randomize routes
    routes = routes[:10] #only keep 10 random routes 
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
        journal=journal,
        journal_entry_produced=True,
        encounter_cnt = 0
    )
    
    print("\nWelcome to Journey to Evereska!") 
    print("You must reach the city of Evereska without running out of money. Traveling between cities costs money.") 
    print("If you are attacked by bandits you must defeat them.")
    print("What city do you want to travel to? (Use numbers 0-9)")
    while True: #main gameplay loop
        money_text = "Money: " + str(state.money) + "£"
        if state.money <= 0.0:
            print("You ran out of money!")
            break
        text_surface = game_font.render(money_text, True, (0, 0, 150)) #this isn't working ? 
        screen.blit(text_surface, (50, 50))
        action = player.selectAction(state)
        if 0 <= int(chr(action)) <= 9:
            if int(chr(action)) != state.current_city and not state.travelling: 
                route1 = (cities[state.current_city], cities[int(chr(action))]) #tuple for start to dest city
                route2 = (cities[int(chr(action))], cities[state.current_city]) #tuple for dest to start city
                if route1 in routes or route2 in routes:  #if the (start city coords, end city coords) tuple is in routes list
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

        for city in cities:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for line in routes:
            pygame.draw.line(screen, (255, 0, 0), *line)

        displayCityNames(cities, city_names)
        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling: #if you make to the end of the route 
                print('Arrived at', city_names[state.destination_city])
                state.journal_entry_produced=False

        if not state.journal_entry_produced: #if a new journal entry is needed 
            if state.encounter_cnt == 0: #if there were no encounters 
                state.journal.append(getResponse("Generate a single 1 paragraph journal entry about traveling by foot through the country from a city called" 
                                                 + city_names[state.current_city] + "to one called" + city_names[state.destination_city] + 
                                                 ". Feel free to make up details about the cities. Maybe refer indirectly to the fact that you are an elf from the elf country, and an archer. Mention that you did not encounter any bandits. Write in a medieval style."))
            elif state.encounter_cnt == 1: #if there was 1 encounter
                state.journal.append(getResponse("Generate a single 1 paragraph journal entry about traveling by foot through the country from a city called" 
                                                 + city_names[state.current_city] + "to one called" + city_names[state.destination_city] + 
                                                 ". Feel free to make up details about the cities. Maybe refer indirectly to the fact that you are an elf from the elf country, and an archer. Mention that you encountered a bandit but you defeated him with a bow and arrow and a sword. Write in a medieval style.")) 
            elif state.encounter_cnt > 1: #if there were multiple encounters 
                state.journal.append(getResponse("Generate a single 1 paragraph journal entry about traveling by foot through the country from a city called" 
                                                 + city_names[state.current_city] + "to a city called" + city_names[state.destination_city] + 
                                                 ". Feel free to make up details about the cities. Mention that you encountered " + str(state.encounter_cnt) 
                                                 + " bandits along the way, but that you managed to defeat the bandits at every encounter bow and arrow and a sword. Maybe refer indirectly to the fact that you are an elf from the elf country, and an archer. Write in a medieval style." )) 
            print("Journal updated: " + str(journal[-1]))
            state.journal_entry_produced = True

        if not state.travelling:
            encounter_event = False
            state.encounter_cnt=0
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
