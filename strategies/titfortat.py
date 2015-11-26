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
        self.id = 0

    def strategy(self, state, **context):
        self.id += 1
        if self.id <= 1:
            self.actions.append("cooperate")
            return "cooperate"

        if state[-1] in (TEMPTATION, REWARD):
            self.actions.append("cooperate")
            return "cooperate"
        else: # if history[-1] == (1 or 5): # or -1
            self.actions.append("defect") 
            return "defect"