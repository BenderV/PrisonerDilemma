__author__ = 'Benjamin Derville, benjamin.derville@gmail.com'

from random import choice
from scipy import zeros

from pybrain.rl.environments.twoplayergames.twoplayergame import TwoPlayerGame
from twoplayergame import SimultaneousTwoPlayerGame

class PrisonersDilemmaGame(TwoPlayerGame):
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



    # ID 
    BLACK = 1
    WHITE = -1
    startcolor = BLACK

    def __init__(self):
        self.params()
        self.reset()

    def reset(self):
        """ empty history, records. (reset TwoPlayerGame) """
        TwoPlayerGame.reset(self)
        self.data = {'id': [], 'W': [], 'B': []}
        self.movesDone = 0

    def params(self):
        """ create the parameters for the game """
        self.reward = 3
        self.sucker = 0
        self.temptation = 5
        self.penalty = 1

    @property
    def indim(self):
        # the number of action values the environment accepts
        return 5 #2 ** 5

    @property
    def outdim(self):
        # the number of sensor values the environment produces
        return 2

    def getSensors(self):
        """ the currently visible state of the world (the observation may be stochastic - repeated calls returning different values) 
            :rtype: by default, this is assumed to be a numpy array of doubles
        """
        pass


    def getHistory(self, color):
        if color == self.BLACK:
            return self.data['B']
        if color == self.WHITE:
            return self.data['W']

    def isLegal(self, action):
        return True


    def performAction(self, action):
        if not self.lastplayer: # The first to play this move
            self.lastplayer = action[0]
            self.actionB = action[1]
        else:
            self.actionW = action[1]
        self.lastplayer = None
        self.doMove(actionB, "cooperate")

    def doMove(self, actionB, actionW):
        """ action is a tuple (color, move)
            move is the action of the agent (defect or cooperate)
        returns True if the move was legal. """
        self.movesDone += 1
        assert actionW[0] == self.WHITE
        assert actionB[0] == self.BLACK

        action_w = actionW[1]
        action_b = actionB[1]
        if (action_w and action_b) not in ['defect', 'cooperate']:
            return False
        else:  
            if action_w == action_b == "defect":
                # self.prisoner_a.punish
                return_w, return_b = self.penalty, self.penalty
                # print "A & B get 2 years"
            elif action_w == "defect" and action_b == "cooperate":
                return_w = self.temptation
                return_b = self.sucker
                # print "A is free and B get 3 years in prisons"
            elif action_w == "cooperate" and action_b == "defect":
                return_w = self.sucker
                return_b = self.temptation
                # print "B is free and A get 3 years in prisons"
            elif (action_w and action_b) == "cooperate":
                return_w, return_b =  self.reward, self.reward
                # print "A & B get 1 year"
            else  :
                # print "Error, wrong move"
                return_w, return_b = -1, -1


            self.data['id'].append(self.movesDone)
            self.data['W'].append(return_w)
            self.data['B'].append(return_b)
            return True