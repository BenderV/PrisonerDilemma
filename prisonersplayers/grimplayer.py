__author__ = 'Benjamin Derville, benjamin.derville@gmail.com'


from prisonerplayer import PrisonerPlayer

class GrimPlayer(PrisonerPlayer):
    """Cooperate unless the opponent defects, in which case, defect forever.
    """

    def getAction(self):
    	history = self.game.getHistory(-self.color) # we want the opponent history
 
        if not history: # empty list
            self.grim = False # initiate
            return [self.color, 'cooperate']
        
        elif not self.grim :
            if history[-1] in (1, 5):
                self.grim = True
                return [self.color, 'defect']
            return [self.color, 'cooperate']
        else:
            return [self.color, 'defect']