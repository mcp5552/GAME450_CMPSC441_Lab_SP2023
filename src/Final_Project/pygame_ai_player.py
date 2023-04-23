""" pygame_ai_player.py
defines the AI player classes for playing the game and for handling combat

contains:
    class PyGameAIPlayer
    class PyGameAiPlayer(CombatPlayer)
"""

import pygame
import sys
from pathlib import Path

# line taken from turn_combat.py
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))
from Final_Project.turn_combat import CombatPlayer
import random

class PyGameAIPlayer:
    def __init__(self) -> None:
        pass

    def selectAction(self, state):
        return random.choice([ord("0"),ord("1"),ord("2"),ord("3"),ord("4"),ord("5"),ord("6"),ord("7"),ord("8"),ord("9")])

class PyGameAICombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        print("selecting weapon") #debug
        while True:
            self.weapon = random.randint(0, 2)
            print("choice is: " + self.weapon) #debug
            return self.weapon
