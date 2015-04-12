from .prisoner import Prisoner

class Human(Prisoner):
    """We ask for the player input."""
    def __init__(self, arg):
        super(Human, self).__init__(arg)
    
    def strategy(self, move_id, history):
        choice = None
        while choice not in ['cooperate','defect']:
            print("move n_", move_id)
            print("history of the adversary : ", history)
            choice = raw_input("Your choice, 'cooperate' or 'defect' ? \n")
        return choice