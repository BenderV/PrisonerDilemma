__author__ = 'Tom Schaul, tom@idsia.ch'

from pybrain.utilities import abstractMethod
from pybrain.rl.environments.twoplayergames.twoplayergame import CompetitiveEnvironment


class SimultaneousTwoPlayerGame(CompetitiveEnvironment):
    """ a game between 2 players, simultaneous turns. 
    Winner is an option, only the result count """

    DRAW = 'draw'

    def reset(self):
        self.winner = None
        self.lastplayer = None

    def performAction(self, actions):
        self.doMove(*actions)

    def doMove(self, action1, action2):
        """ the core method to be implemented bu all SimultaneousTwoPlayerGames:
        what to do if White play action1 and B play action2. """
        abstractMethod()

    def isLegal(self, player, action):
        """ is this a legal move? By default, everything is allowed. """
        return True

    def gameOver(self):
        """ is the game over? """
        return self.winner != None

    def getWinner(self):
        """ returns the id of the winner, 'draw' if it's a draw, and None if the game is undecided. """
        return self.winner