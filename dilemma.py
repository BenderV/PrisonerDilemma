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

import random
import itertools
import csv
from sklearn import svm, linear_model
from sklearn.linear_model import SGDClassifier, SGDRegressor
import sys
import numpy as np
# Pybrain import
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.learners import Q
from pybrain.rl.experiments import Experiment, ContinuousExperiment
from pybrain.rl.explorers import EpsilonGreedyExplorer
from pybrain.rl.agents import LearningAgent





REWARD = 3
SUCKER = 0
TEMPTATION = 5
PENALTY = 1


class Prisoner(object):
    """docstring for Prisoner"""
    def __init__(self, name, strategy = "cooperate"):
        self.name = name
        self.setstrategy(strategy)
        # The variable for the strategies
        self.defaultstrategy = "cooperate"
        self.grim = False # we are calm by nature
        self.ml_sizeoffunction = 5
        self.pybrain()

    def pybrain(self):
        av_table = ActionValueTable(3, 2)
        av_table.initialize(0.)
        # define Q-learning agent
        learner = Q(0.5, 0.0)
        learner._setExplorer(EpsilonGreedyExplorer(0.0))
        self.agent = LearningAgent(av_table, learner)

    def setstrategy(self, strategy):
        if strategy == "cooperate" : 
            self.strategy = self.cooperate
        elif strategy == "defect" :
            self.strategy = self.defect
        elif strategy == "random" :
            self.strategy = self.random
        elif strategy == "human" :
            self.strategy = self.human
        elif strategy == "titfortat" :
            self.strategy = self.titfortat
        elif strategy == "grim" :
            self.strategy = self.grim
        elif strategy == "pavlov" :
            self.strategy = self.pavlov
        elif strategy == "machinelearning" :
            self.strategy = self.machinelearning
        else:
            print "DEBUG : strategy = ", strategy
            self.strategy = self.human # easier to debug 

    @classmethod
    def cooperate(cls, *args):
        """Always cooperate."""
        return "cooperate"
    
    @classmethod
    def defect(cls, *args):
        """Always defect."""
        return "defect"
    
    @classmethod
    def random(cls, *args):
        """Cooperate or Defect at random."""
        if(random.uniform(0, 1) < 0.5):
            return "cooperate"
        else:
            return "defect"

    @classmethod
    def human(cls, move_id, history):
        """We ask for the player input."""
        choice = None
        option = ['cooperate','defect']
        while choice not in option:
            print "move n_", move_id
            print "history of the adversary : ", history
            choice = raw_input("Your choice, 'cooperate' or 'defect' ? \n")
        
        return choice

    @classmethod
    def titfortat(cls, move_id, history):
        """Cooperate at first, and play the opponents previous move after."""
        if move_id == 1:
            return "cooperate"
        else:
            if history[-1] in (0, 3):
                return "cooperate"
            else: # if history[-1] == (1 or 5): # or -1  
                return "defect"

    def grim(self, move_id, history):
        """Cooperate unless the opponent defects, in which case, defect forever.
        """
        if not history: # empty list
            self.grim = False # initiate
            return "cooperate"
        
        elif not self.grim :
            if history[-1] in (1, 5):
                self.grim = True
                return "defect"
            return "cooperate"
        else:
            return "defect"

    def pavlov(self, move_id, history):
        """Cooperate on the first move and on subsequent moves,
        switch strategies if you were punished on the previous move
        """
        if not history: # empty list => initiate
            self.defaultstrategy = "cooperate"
            return self.defaultstrategy
            
        elif history[-1] in (1, 5):
            if self.defaultstrategy == "cooperate": 
                self.defaultstrategy = "defect"
            else:
                self.defaultstrategy = "cooperate" 
        return self.defaultstrategy

    def machinelearning(self, move_id, history):
        """implement the simplest ML algorithm possible"""
        sizeoffunction = self.ml_sizeoffunction

        if not history: # empty list => initiate
            pass
        
        ### UPDATE
        if len(history) >= sizeoffunction:
            # 1 for "cooperate", -1 for "defect"
            myactionshistory = [(1 if (res==0 or res==3) else -1) for res in history]

        # Fot the first move, we use a random fonction
        if len(history)<=sizeoffunction*1: # 5*1 moves RANDOM !
            return self.random()
        else:
            print self.agent.indim
            ben = raw_input("..................");
            self.agent.integrateObservation(np.array(myactionshistory[-6:], dtype='f')) # remettre 5...
            print self.agent.lastobs
            action = self.agent.getAction()
            print "action : ", action
            self.agent.giveReward(sum(history[-1:]))

            self.agent.learn()

            if action > 0.99:
                return "cooperate"
            else:
                return "defect"

class Game(object):
    """docstring for Game"""
    def __init__(self, prisoner_a, prisoner_b):
        "initialize with the Prisoners"
        self.prisoner_a = prisoner_a
        self.prisoner_b = prisoner_b
        self.move_id = 0
        self.data = {'id': [], 'A': [], 'B': []}

    @classmethod
    def fromstrategy(cls, strategy_a, strategy_b):
        "initialize game with the strategy names"
        prisoner_a = Prisoner("A", strategy_a)
        prisoner_b = Prisoner("B", strategy_b)
        return cls(prisoner_a, prisoner_b)

    def play(self, moves=1): # add parameters of the game
        """Play x times"""
        for _ in xrange(0, moves):
            self.play_a_move()

    def play_a_move(self):
        """Execute one iteration of the game
        We ask for strategy and then save the results
        """
        self.move_id += 1
        # we give the history of the adversary
        action_a = self.prisoner_a.strategy(self.move_id, self.data['B'])
        action_b = self.prisoner_b.strategy(self.move_id, self.data['A'])

        # print "A = ",action_a, "B = ", action_b

        if action_a == action_b == "defect":
            # self.prisoner_a.punish
            return_a, return_b = PENALTY, PENALTY
            # print "A & B get 2 years"
        elif action_a == "defect" and action_b == "cooperate":
            return_a = TEMPTATION
            return_b = SUCKER
            # print "A is free and B get 3 years in prisons"
        elif action_a == "cooperate" and action_b == "defect":
            return_a = SUCKER
            return_b = TEMPTATION
            # print "B is free and A get 3 years in prisons"
        elif (action_a and action_b) == "cooperate":
            return_a, return_b =  REWARD, REWARD
            # print "A & B get 1 year"
        else  :
            # print "Error, wrong move"
            return_a, return_b = -1, -1

        self.data['id'].append(self.move_id)
        self.data['A'].append(return_a)
        self.data['B'].append(return_b)


def test():
    """Test the game engine
    """
    prisoner_a = Prisoner("A", "cooperate")
    prisoner_b = Prisoner("B", "grim")
    game = Game(prisoner_a, prisoner_b)
    game.play(10)
    print game.data
    assert(game.data['A']==[3, 3, 3, 3, 3, 3, 3, 3, 3])
    assert(game.data['B']==[3, 3, 3, 3, 3, 3, 3, 3, 3])


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

        print "A = ", game.prisoner_a.strategy
        print "B = ", game.prisoner_b.strategy
        game.play(numberofgames)
        print "Result A = ", sum(game.data['A'])
        print "Result B = ", sum(game.data['B'])

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
    print "Data exported to CSV"


def main(argv="output.csv"):
    """ We give the choice of what to do 
    Humans player or strategy tests
    """
    #strategies = ["cooperate", "defect", "random", "titfortat", "grim", "pavlov"]

    strategies = ["machinelearning", "titfortat"] 
    result = robintournement(1000, *strategies)
    tocsv(result, argv)

if __name__ == '__main__':
    # test()
    main(sys.argv[1])
