__author__ = 'Benjamin Derville, benjamin.derville@gmail.com'


from prisonerplayer import PrisonerPlayer

class DefectPlayer(PrisonerPlayer):
    """Always defect.
    """

    def getAction(self):
        return [self.color, 'defect']