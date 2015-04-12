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
# import matplotlib.pyplot as plt

REWARD = 4 # put 4 here?
SUCKER = 0
TEMPTATION = 5
PENALTY = 1

        

class Game(object):
    """docstring for Game"""
    def __init__(self, prisoner_a, prisoner_b):
        "initialize with the Prisoners"
        self.prisoner_a = prisoner_a
        self.prisoner_b = prisoner_b
        self.move_id = 0
        self.data = {'id': [], 'A': [], 'B': []}

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
        self.move_id += 1
        # we give the history of the adversary
        action_a = self.prisoner_a.strategy(move_id=self.move_id, history=self.data['B'])
        action_b = self.prisoner_b.strategy(move_id=self.move_id, history=self.data['A'])

        if action_a == action_b == "defect":
            return_a, return_b = PENALTY, PENALTY
        elif action_a == "defect" and action_b == "cooperate":
            return_a = TEMPTATION
            return_b = SUCKER
        elif action_a == "cooperate" and action_b == "defect":
            return_a = SUCKER
            return_b = TEMPTATION
        elif (action_a and action_b) == "cooperate":
            return_a, return_b =  REWARD, REWARD
        else:
            assert False # "Error, impossible move"

        self.prisoner_a.actions.append(action_a)
        self.prisoner_b.actions.append(action_b)

        # Give rewards/punishment
        self.prisoner_a.rewards.append(return_a)
        self.prisoner_b.rewards.append(return_b)

        self.prisoner_a.punish(reward=return_a, action=action_a)
        self.prisoner_b.punish(reward=return_b, action=action_b)

        self.data['id'].append(self.move_id)
        self.data['A'].append(return_a)
        self.data['B'].append(return_b)


# Fix later.
def robintournement(numberofgames=1000, *strategies):
    """Round-robin tournament : Every strategy play against all other
    Including itself.
    The return is a flat data, with the name of the 'player', the adversary
    and the data/result of the player
    To only fight strategy1 vs strategy1, just do strategies = ["strategy1"]
    OR strategies = ["strategy1","strategy1"], with_replacement=True
    """
    data = []
    players = []

    header = ["player1", "player2"]
    header.extend(range(1,numberofgames+1))
    data.append(header)

    for index, strategy in enumerate(strategies):
        players.append(Prisoner(strategy, strategy)) # one for the name, one for the function
    
    
    # We decide if we play a strategy against itself
    games = itertools.combinations(players, 2)


    for player_a, player_b in games:
        game = Game(player_a, player_b)

        game.play(numberofgames)
        
        gamebya = [player_a.name, player_b.name]
        gamebya.extend(game.data['A'])
        gamebyb = [player_b.name, player_a.name]
        gamebyb.extend(game.data['B'])
        data.append(gamebya) # We append the data of player_a
        data.append(gamebyb) # We append the data of player_b
    return data

def tocsv(data, name="default.csv"):
    with open(name, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    print("Data exported to CSV")

def display(data):
    plt.plot(data,'r')
    plt.show()

def main(argv="output.csv"):
    pass

if __name__ == '__main__':
    main()
