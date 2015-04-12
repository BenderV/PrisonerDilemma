from .prisoner import Prisoner

class Defect(Prisoner):
    """Always defect."""
    def __init__(self, arg):
        super(Defect, self).__init__(arg)
    
    def strategy(self, **context):
        return "defect"