__author__ = 'Benjamin Derville, benjamin.derville@gmail.com'

from random import choice

from prisonerplayer import PrisonerPlayer

# TODO : add a parameter to the randomness
class RandomPrisonerPlayer(PrisonerPlayer):
    """ defect or cooperate at random (50/50)"""

    def getAction(self):
        return [self.color, choice(['cooperate','defect'])]