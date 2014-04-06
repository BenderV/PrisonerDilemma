__author__ = 'Benjamin Derville, benjamin.derville@gmail.com'


from prisonerplayer import PrisonerPlayer

class PavlovPlayer(PrisonerPlayer):
    """Cooperate on the first move and on subsequent moves,
    switch strategies if you were punished on the previous move
    """

    def getAction(self):
    	history = self.game.getHistory(-self.color) # we want the opponent history
 
        if not history: # empty list => initiate
            self.defaultstrategy = "cooperate"
            return [self.color, self.defaultstrategy]
            
        elif history[-1] in (1, 5):
            if self.defaultstrategy == "cooperate": 
                self.defaultstrategy = "defect"
            else:
                self.defaultstrategy = "cooperate" 
        return [self.color, self.defaultstrategy]