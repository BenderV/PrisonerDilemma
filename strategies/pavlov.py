from .prisoner import Prisoner

class Pavlov(Prisoner):
    """Cooperate on the first move and on subsequent moves,
    switch strategies if you were punished on the previous move"""
    def __init__(self, arg):
        super(Titfortat, self).__init__(arg)
    
    def strategy(self, history):
        if not history: # empty list => initiate
            self.defaultstrategy = "cooperate"
            return self.defaultstrategy
            
        elif history[-1] in (1, 5):
            if self.defaultstrategy == "cooperate": 
                self.defaultstrategy = "defect"
            else:
                self.defaultstrategy = "cooperate" 
        return self.defaultstrategy