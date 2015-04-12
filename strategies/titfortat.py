from .prisoner import Prisoner 

## Redundancy...
REWARD = 4 # put 4 here?
SUCKER = 0
TEMPTATION = 5
PENALTY = 1


class Titfortat(Prisoner):
    """Cooperate at first, and play the opponents previous move after."""
    def __init__(self, arg):
        super(Titfortat, self).__init__(arg)
    
    def strategy(self, move_id, history):
        if move_id == 1:
            return "cooperate"
        else:
            if history[-1] in (SUCKER, REWARD):
                return "cooperate"
            else: # if history[-1] == (1 or 5): # or -1  
                return "defect"