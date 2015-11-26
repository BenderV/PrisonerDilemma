"""Prisoners Dilemma 

Two members of a criminal gang are arrested and imprisoned. 
Each prisoner is in solitary confinement with no means of speaking to 
or exchanging messages with the other.
The police admit they don't have enough evidence 
to convict the pair on the principal charge. 
They plan to sentence both to a year in prison on a lesser charge.
Simultaneously, the police offer each prisoner a Faustian bargain. 
Each prisoner is given the opportunity either to betray (defect) the other,
by testifying that the other committed the crime,
or to cooperate with the other by remaining silent. 
Here's how it goes:
If A and B both defect the other
    each of them serves 2 years in prison
If A defects B but B remains silent
    A will be set free and B will serve 3 years in prison
If A and B both remain silent
    both of them will only serve 1 year in prison
"""

"""
Next objectif, with Qlearning, refind the reward with titfortat
"""

import itertools
import csv
import numpy as np
import math
from strategies import *        

class Game(object):
    """docstring for Game"""
    def __init__(self, prisoner_a, prisoner_b):
        "initialize with the Prisoners"
        self.prisoner_a = prisoner_a
        self.prisoner_b = prisoner_b
        self.move_id = 0
        self.data = {'id': [], 'A': [], 'B': []}

        self.REWARD = 4 # put 4 here?
        self.SUCKER = 0
        self.TEMPTATION = 5
        self.PENALTY = 1

    def reset_players(self):
        pass

    def play(self, moves=1, iterated=False): # add parameters of the game
        """Play x times"""
        for _ in range(0, moves):
            if not iterated:
                self.reset_players()
            self.play_a_move()

    def play_a_move(self):
        """Execute one iteration of the game
        We ask for strategy and then save the results
        """
        # The state here is the history of the player results
        action_a = self.prisoner_a.strategy(state=self.data['A'])
        action_b = self.prisoner_b.strategy(state=self.data['B'])

        ## Game mechanic
        if action_a == action_b == "defect":
            return_a, return_b = self.PENALTY, self.PENALTY
        elif action_a == "defect" and action_b == "cooperate":
            return_a = self.TEMPTATION
            return_b = self.SUCKER
        elif action_a == "cooperate" and action_b == "defect":
            return_a = self.SUCKER
            return_b = self.TEMPTATION
        elif (action_a and action_b) == "cooperate":
            return_a, return_b =  self.REWARD, self.REWARD
        else:
            assert False # "Error, impossible move"

        # state = history
        # state, action, reward, new_state
        self.move_id += 1
        self.data['id'].append(self.move_id)
        self.data['A'].append(return_a)
        self.data['B'].append(return_b)

        # history, action, return_a, history
        self.prisoner_a.punish(state=self.data['A'][:-1], action=action_a, reward=return_a, new_state=self.data['A'])
        self.prisoner_b.punish(state=self.data['B'][:-1], action=action_b, reward=return_b, new_state=self.data['B'])
        
