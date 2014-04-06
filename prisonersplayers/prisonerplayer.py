__author__ = 'Benjamin Derville, benjamin.derville@gmail.com'

from pybrain.rl.agents.agent import Agent
from prisonersdilemmagame import PrisonersDilemmaGame
# from pybrain.rl.environments.twoplayergames import CaptureGame


class PrisonerPlayer(Agent):
    """ a class of agent that can play the prisoner dilemma
    have access to the game object, and play with "defect" or "cooperate"
    It generally also has access to the game object. 
    playerid is self.color (by convention, and because it's how it's implemented in pybrain)
    """
    def __init__(self, game, color = PrisonersDilemmaGame.BLACK, **args):
        self.game = game
        self.color = color
        self.setArgs(**args)


