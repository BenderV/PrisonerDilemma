from .prisoner import Prisoner

class Grim(Prisoner):
    """Cooperate unless the opponent defects, in which case, defect forever."""
    def __init__(self, arg):
        super(Grim, self).__init__(arg)
        self.grim = False

    def strategy(self, history, **context):
        if not history: # empty list    
            self.grim = False # useful?
            return "cooperate"
        elif not self.grim:
            if history[-1] in (1, 5):
                self.grim = True
                return "defect"
            return "cooperate"
        else:
            return "defect"