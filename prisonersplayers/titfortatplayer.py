__author__ = 'Benjamin Derville, benjamin.derville@gmail.com'


from prisonerplayer import PrisonerPlayer

class TitForTatPlayer(PrisonerPlayer):
    """Cooperate at first, and play the opponents previous move after."""

    def getAction(self):
    	history = self.game.getHistory(-self.color) # we want the opponent history
 
        if not history:
            return [self.color, 'cooperate']
        else:
            if history[-1] in (0, 3):
                return [self.color, 'cooperate']
            else: # if history[-1] == (1 or 5): # or -1  
                return [self.color, 'defect']