"""pygame_human_player.py
defines running of the game when a human (not an ai) is playing 

contains:
    class PyGameHumanPlayer
    PyGameHumanCombatPlayer(CombatPlayer)
"""

import pygame
from turn_combat import CombatPlayer

class PyGameHumanPlayer:
    def __init__(self) -> None:
        pass

#this selects 0-9 but not y/n,
    def selectAction(self, state): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if ord("0") <= event.key <= ord("9"):
                    return event.key
                if event.key == ord("y") or event.key == ord("n"):
                    return event.key 
        return ord(str(state.current_city))  # Not a safe operation for >10 cities

class PyGameHumanCombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [ord("s"), ord("a"), ord("f")]:
                        choice = {ord("s"): 1, ord("a"): 2, ord("f"): 3}[event.key]
                        self.weapon = choice - 1
                        return self.weapon
