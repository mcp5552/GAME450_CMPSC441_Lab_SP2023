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
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def get_combat_surface(size):
    landscape = get_combat_bg(size)
    print("Created a landscape of size", landscape.shape)
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
    money = 100
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

    cities = get_randomly_spread_cities(size, len(city_names))
    routes = get_routes(cities)

    random.shuffle(routes)
    routes = routes[:10]

    player_sprite = Sprite(sprite_path, cities[start_city])

    """Set player of game to either human or AI """
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
    

    while True: #main gameplay loop
        money_text = "Money: " + str(state.money) + "£"
        text_surface = game_font.render(money_text, True, (0, 0, 150))
        screen.blit(text_surface, (10, 440))
        action = player.selectAction(state)
        if 0 <= int(chr(action)) <= 9:
            if int(chr(action)) != state.current_city and not state.travelling:
                start = cities[state.current_city]
                state.destination_city = int(chr(action))
                destination = cities[state.destination_city]
                player_sprite.set_location(cities[state.current_city])
                state.travelling = True
                print(
                    "Travelling from", state.current_city, "to", state.destination_city
                )
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
            if not state.travelling:
                print('Arrived at', state.destination_city)
                state.journal_entry_produced=False

        if not state.journal_entry_produced: #if a new journal entry is needed 
            if state.encounter_cnt == 0: #if there we no encounters 
                state.journal.append(getResponse("Generate a single journal entry about traveling by foot through the country from" + city_names[state.current_city] + "to " + city_names[state.destination_city] + ". Feel free to make up details about the cities. Mention that you did not encounter any bandits. Write in a medieval style."))
            elif state.encounter_cnt == 1:
                state.journal.append(getResponse("Generate a single journal entry about traveling by foot through the country from" + city_names[state.current_city] + "to " + city_names[state.destination_city] + ". Feel free to make up details about the cities. Mention that you encountered a bandit but you defeated him. Write in a medieval style.")) 
            elif state.encounter_cnt > 1: 
                state.journal.append(getResponse("Generate a single journal entry about traveling by foot through the country from" + city_names[state.current_city] + "to " + city_names[state.destination_city] + ". Feel free to make up details about the cities. Mention that there were " + str(state.encounter_cnt) + " encounters with bandits, but that you managed to defeat the bandits at every encounter. Write in a medieval style." )) 
            print("Journal updated: " + str(journal[-1]))

        if not state.travelling:
            encounter_event = False
            state.encounter_cnt=0
            state.current_city = state.destination_city

        if state.encounter_event:
            run_pygame_combat(combat_surface, screen, player_sprite)
            state.encounter_cnt += 1
            state.encounter_event = False

        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()
        if state.current_city == end_city:
            print('You have reached the end of the game!')
            break
