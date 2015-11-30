from .prisoner import Prisoner
import random

class Unpredictable(Prisoner):
    """Cooperate or Defect at random."""
    def __init__(self, arg):
        super(Unpredictable, self).__init__(arg)

    def strategy(self, **context):
        if(random.uniform(0, 1) < 0.5):
            return "cooperate"
        else:
            return "defect"