from .prisoner import Prisoner

class Cooperate(Prisoner):
    """Always cooperate."""
    def __init__(self, arg):
        super(Cooperate, self).__init__(arg)
    
    def strategy(self, **context):
        return "cooperate"