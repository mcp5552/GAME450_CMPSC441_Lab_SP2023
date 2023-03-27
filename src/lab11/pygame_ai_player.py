""" Create PyGameAIPlayer class here"""
import pygame
from lab11.turn_combat import CombatPlayer
import random

class PyGameAIPlayer:
    def __init__(self) -> None:
        pass

    def selectAction(self, state):
        return random.choice([ord("0"),ord("1"),ord("2"),ord("3"),ord("4"),ord("5"),ord("6"),ord("7"),ord("8"),ord("9")])


""" Create PyGameAICombatPlayer class here"""
class PyGameAICombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        print("selecting weapon") #debug
        while True:
            self.weapon = random.randint(0, 2)
            print("choice is: " + self.weapon) #debug
            return self.weapon
