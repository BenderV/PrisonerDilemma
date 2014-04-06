__author__ = 'Benjamin Derville, benjamin.derville@gmail.com'


from prisonerplayer import PrisonerPlayer

class CooperatePlayer(PrisonerPlayer):
    """Always cooperate.
    """

    def getAction(self):
        return [self.color, 'cooperate']