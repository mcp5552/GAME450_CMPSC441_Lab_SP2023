"""
episode.py

contains:
run_episode(player1, player2)
"""

''' 
Lab 12: Beginnings of Reinforcement Learning
We will modularize the code in pygame_combat.py from lab 11 together.

Create a function called run_episode that takes in two players
and runs a single episode of combat between them. 
As per RL conventions, the function should return a list of tuples
of the form (observation/state, action, reward) for each turn in the episode.

Note that observation/state is a tuple of the form (player1_health, player2_health).
Action is simply the weapon selected by the player.
Reward is the reward for the player for that turn.
'''

from lab11.pygame_combat import run_turn
from lab11.pygame_combat import run_pygame_combat

import sys
from pathlib import Path

# (line taken from turn_combat)
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

def run_episode(player1, player2): #one episode is multiple turns 
    reward, i = 0, 0
    result = []  # the result of the episode, a list of tuples for each turn of the episode 
    while reward == 0: # run until combat ends with (1 or -1)
        observation = (player1.health, player2.health)
        action = player1.weapon
        #might want to make changes in run_turn to get other stuff from there (Maybe)
        reward = run_turn(player1, player2) # checkWin() returns -1 if lose, 1 if win, 0 if draw or no winner yet 
        result[i] = (observation, action, reward) 
        i += 1 
    return result 