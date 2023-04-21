'''
Lab 13: My first AI agent.
In this lab, you will create your first AI agent.
You will use the run_episode function from lab 12 to run a number of episodes
and collect the returns for each state-action pair.
Then you will use the returns to calculate the action values for each state-action pair.
Finally, you will use the action values to calculate the optimal policy.
You will then test the optimal policy to see how well it performs.

Sidebar-
If you reward every action you may end up in a situation where the agent
will always choose the action that gives the highest reward. Ironically,
this may lead to the agent losing the game.
'''
import sys
from pathlib import Path
from copy import deepcopy
# line taken from turn_combat.py
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab11.pygame_combat import PyGameComputerCombatPlayer
from lab11.turn_combat import CombatPlayer
from lab12.episode import run_episode

from collections import defaultdict
import random
import numpy as np

random.seed(555)


class PyGameRandomCombatPlayer(PyGameComputerCombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        self.weapon = random.randint(0, 2)
        return self.weapon


class PyGamePolicyCombatPlayer(CombatPlayer):
    def __init__(self, name, policy):
        super().__init__(name)
        self.policy = policy

    def weapon_selecting_strategy(self):
        self.weapon = self.policy[self.current_env_state]
        return self.weapon


def run_random_episode(player, opponent):
    player.health = random.choice(range(10, 110, 10))
    opponent.health = random.choice(range(10, 110, 10))
    return run_episode(player, opponent)

'''
get_history_returns(history)
Creates & returns a dictionary of dictionaries (called "returns") from a history. 
Dictionary: Keys = states, values = dictionaries (keys = actions, values = rewards)
'''
def get_history_returns(history): 
    total_return = sum([reward for _, _, reward in history])
    returns = {}
    for i, (state, action, reward) in enumerate(history):
        if state not in returns: #add state (key) if not added already 
            returns[state] = {}
        returns[state][action] = total_return - sum(
            [reward for _, _, reward in history[:i]]
        )
    return returns

'''
def run_episodes(n_episodes)
Runs 'n_episodes' random episodes and return the action values for each state-action pair.
Action values are calculated as the average return for each state-action pair over the 'n_episodes' episodes.
'''
def run_episodes(n_episodes):
    ''' 
        Use the get_history_returns function to get the returns for each state-action pair in each episode.
        Collect the returns for each state-action pair in a dictionary of dictionaries where the keys are states and
            the values are dictionaries of actions and their returns.
        After all episodes have been run, calculate the average return for each state-action pair.
        Return the action values as a dictionary of dictionaries where the keys are states and 
            the values are dictionaries of actions and their values (average returns).
        values are floating point numbers
        ex: action_values = { (100,100): {0: value1, 1: value2, 2: value3}, (80,90): {0:value1, 1:value2}}
    '''
    ret_dict = {} # a dictionary of dictionaries, keys=states (observations), values=returns (dictionaries, keys=actions, values=rewards)
    action_values = {} 
    history = [] #list of results of each episode (results are lists- [observation (i.e. state), action, reward]) 
    player = PyGameRandomCombatPlayer("Rando") #player that takes random actions 
    opponent = PyGameComputerCombatPlayer("Comp")
    for n in range(n_episodes):
        print("Episode # = " + str(n))
        history = run_random_episode(player, opponent) 
        returns = get_history_returns(history) #Use the get_history_returns function to get the returns for each state-action pair in each episode.
        #get_history_returns returns a nested dictionary with keys=states, values="returns" (dictionaries, keys=actions, values=rewards)
        for k, v in returns.items(): #iterate through entire returns dictionary 
            if k not in ret_dict:
                ret_dict[k] = {}
            if list(v.keys())[0] not in ret_dict[k]: #want just the key (the action) from v, not the entire v dictionary
                ret_dict[k][list(v.keys())[0]] = [] 
            ret_dict[k][list(v.keys())[0]].append(list(v.values())[0]) 

    # after all the episodes have been run 
    for observation in ret_dict: #for every state 
        for action in ret_dict[observation]: #for every action of every state
            average_return = sum(ret_dict[observation][action]) / len(ret_dict[observation][action]) #sum list of rewards and divide by list len
            if observation not in action_values: #if action_values has no entry for state 
                action_values[observation] = {}   #insert entry for state and empty dict for key 
            action_values[observation][action] = average_return  #insert average of returns for action as value of inner dict 
        # for each action for a particular state, average all of the returns over all of the episodes 
    return action_values


def get_optimal_policy(action_values):
    optimal_policy = defaultdict(int)
    for state in action_values:
        optimal_policy[state] = max(action_values[state], key=action_values[state].get)
    return optimal_policy


def test_policy(policy):
    names = ["Legolas", "Saruman"]
    total_reward = 0
    for _ in range(100):
        player1 = PyGamePolicyCombatPlayer(names[0], policy)
        player2 = PyGameComputerCombatPlayer(names[1])
        players = [player1, player2]
        total_reward += sum(
            [reward for _, _, reward in run_episode(*players)]
        )
    return total_reward / 100


if __name__ == "__main__":
    action_values = run_episodes(10000) # 10000 originally 
    print(action_values)
    optimal_policy = get_optimal_policy(action_values)
    print(optimal_policy)
    print(test_policy(optimal_policy))
