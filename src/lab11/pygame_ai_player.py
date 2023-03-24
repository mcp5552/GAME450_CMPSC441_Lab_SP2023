""" Create PyGameAIPlayer class here"""
import pygame
from lab11.turn_combat import CombatPlayer
import random

class PyGameAIPlayer:
    def __init__(self) -> None:
        pass

    def selectAction(self, state):
        return random.choice([0,1,2,3,4,5,6,7,8,9])


""" Create PyGameAICombatPlayer class here"""


class PyGameAICombatPlayer:
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        return random.choice([0,1,2])
