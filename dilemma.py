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

import random
import itertools
import csv
from sklearn import svm, linear_model
from sklearn.linear_model import SGDClassifier, SGDRegressor
import sys
import numpy as np
import math
# import matplotlib.pyplot as plt

REWARD = 4 # put 4 here?
SUCKER = 0
TEMPTATION = 5
PENALTY = 1


STATES = [('defect'), ('cooperate')] # with a history of one => what we played
ACTIONS = [('defect'), ('cooperate')] # cooperate or defect

def unexp(x):
   return math.exp(-x)

 
class QLearning(object):
    """docstring for QLearning"""
    def __init__(self):
      super(QLearning, self).__init__()
      self.values = {}
      self.lrate = 0.4 # step size, for now, we always learn a bit on everything.
      self.gamma = 0 # discount factor
      self.id = 0 

      # initialization
      for action in ACTIONS:
          for state in STATES:
              self.values[state, action] = 0.5

    def learn(self, state, action, reward):
        old_value = self.values[state, action]
        lrate = self.lrate

        qmax = max([self.values[action, a] for a in ACTIONS]) # just because new_state = action
        
        new_value = old_value + lrate * (reward + self.gamma * qmax  - old_value)
        self.values[state, action] = new_value


    def choose(self, state, actions):
        if not state: # if we don't have any state, randomly do an action.
            return random.choice(actions)

        self.id += 1
        if random.random > 0.1 and self.id < 1000:
            return random.choice(actions)

        action_max_value = - 10000
        action_max = 'default'

        for action in actions:
            predict = self.values[state, action]
            if predict > action_max_value:
                action_max = action
                action_max_value = predict


        return action_max






class Prisoner(object):
    """docstring for Prisoner"""
    def __init__(self, name, strategy = "cooperate"):
        self.name = name
        self.history = [] # history of action ?
        self.rewards = []

    def strategy(self, **context):
        pass

    def punish(self, reward, **context):
        pass


class Random(Prisoner):
    """Cooperate or Defect at random."""
    def __init__(self, arg):
        super(Random, self).__init__(arg)

    def strategy(self, **context):
        if(random.uniform(0, 1) < 0.5):
            return "cooperate"
        else:
            return "defect"

class Cooperate(Prisoner):
    """Always cooperate."""
    def __init__(self, arg):
        super(Cooperate, self).__init__(arg)
    
    def strategy(self, **context):
        return "cooperate"

class Defect(Prisoner):
    """Always defect."""
    def __init__(self, arg):
        super(Defect, self).__init__(arg)
    
    def strategy(self, **context):
        return "defect"


class Grim(Prisoner):
    """Cooperate unless the opponent defects, in which case, defect forever."""
    def __init__(self, arg):
        super(Grim, self).__init__(arg)
        self.grim = False

    def strategy(self, history, **context):
        if not history: # empty list    
            self.grim = False # useful?
            return "cooperate"
        elif not self.grim:
            if history[-1] in (1, 5):
                self.grim = True
                return "defect"
            return "cooperate"
        else:
            return "defect"


class Human(Prisoner):
    """We ask for the player input."""
    def __init__(self, arg):
        super(Human, self).__init__(arg)
    
    def strategy(self, move_id, history):
        choice = None
        while choice not in ['cooperate','defect']:
            print("move n_", move_id)
            print("history of the adversary : ", history)
            choice = raw_input("Your choice, 'cooperate' or 'defect' ? \n")
        return choice


class Titfortat(Prisoner):
    """Cooperate at first, and play the opponents previous move after."""
    def __init__(self, arg):
        super(Titfortat, self).__init__(arg)
    
    def strategy(self, move_id, history):
        if move_id == 1:
            return "cooperate"
        else:
            if history[-1] in (SUCKER, REWARD):
                return "cooperate"
            else: # if history[-1] == (1 or 5): # or -1  
                return "defect"


class Pavlov(Prisoner):
    """Cooperate on the first move and on subsequent moves,
    switch strategies if you were punished on the previous move"""
    def __init__(self, arg):
        super(Titfortat, self).__init__(arg)
    
    def strategy(self, move_id, history):
        if not history: # empty list => initiate
            self.defaultstrategy = "cooperate"
            return self.defaultstrategy
            
        elif history[-1] in (1, 5):
            if self.defaultstrategy == "cooperate": 
                self.defaultstrategy = "defect"
            else:
                self.defaultstrategy = "cooperate" 
        return self.defaultstrategy

class MachineLearning(Prisoner):
    """implement the simplest ML algorithm possible
    Non iterative version of the game
    It should learn that he should always defect"""
    def __init__(self, arg):
        super(MachineLearning, self).__init__(arg)
        self.qlearning = QLearning()
        self.last_action = None
    
    def strategy(self, history, **context):
        action = self.qlearning.choose(state=self.last_action, actions=ACTIONS)
        return action

    def punish(self, reward, **context):
        print(self.qlearning.values)
        if self.last_action:
            self.qlearning.learn(state=self.last_action, action=context['action'], reward=reward)
        self.last_action = context['action']
        

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

        # Give rewards/punishment
        self.prisoner_a.rewards.append(return_a)
        self.prisoner_b.rewards.append(return_b)

        self.prisoner_a.punish(reward=return_a, action=action_a)
        self.prisoner_b.punish(reward=return_b, action=action_b)

        self.data['id'].append(self.move_id)
        self.data['A'].append(return_a)
        self.data['B'].append(return_b)


def test():
    """Test the game engine
    """
    strategies = [MachineLearning, Cooperate, Grim, Human]
    prisoner_a = MachineLearning("A")
    prisoner_b = Titfortat("B")
    game = Game(prisoner_a, prisoner_b)
    game.play(10000)
    print(game.data['A'])
    #assert(game.data['A']==[3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
    #assert(game.data['B']==[3, 3, 3, 3, 3, 3, 3, 3, 3, 3])


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

        print("A = ", game.prisoner_a.strategy)
        print("B = ", game.prisoner_b.strategy)
        game.play(numberofgames)
        print("Result A = ", sum(game.data['A']))
        print("Result B = ", sum(game.data['B']))

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
    """ We give the choice of what to do 
    Humans player or strategy tests
    """
    test()
    #strategies = ["cooperate", "defect", "random", "titfortat", "grim", "pavlov"]
    #strategies = ["machinelearning", "titfortat"] 
    #result = robintournement(2000, *strategies)
    #tocsv(result, argv)
    #display(result[1][2:])

if __name__ == '__main__':
    # test()
    main(sys.argv[1])
