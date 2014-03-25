import math
import random

"""
Two members of a criminal gang are arrested and imprisoned. Each prisoner is in solitary confinement with no means of speaking to or exchanging messages with the other. The police admit they don't have enough evidence to convict the pair on the principal charge. They plan to sentence both to a year in prison on a lesser charge. Simultaneously, the police offer each prisoner a Faustian bargain. Each prisoner is given the opportunity either to betray (defect) the other, by testifying that the other committed the crime, or to cooperate with the other by remaining silent. Here's how it goes:
If A and B both defect the other, each of them serves 2 years in prison
If A defects B but B remains silent, A will be set free and B will serve 3 years in prison (and vice versa)
If A and B both remain silent, both of them will only serve 1 year in prison (on the lesser charge)
"""

Reward = 3
Sucker = 0
Temptation = 5
Penalty = 1



class Action(object):
    """docstring for Action"""
    def __init__(self):
        #super(Action, self).__init__()
        pass
    
    @classmethod
    def cooperate(cls):
        return "cooperate"
    
    @classmethod
    def defect(cls):
        return "defect"
    
    @classmethod
    def beRandom(cls, probabilityOfcooperate = 0.5):
        if(random.uniform(0,1) < probabilityOfcooperate):
            return "cooperate"
        else:
            return "defect"

    # to test...
    @classmethod
    def beHuman(cls):
        # We ask for the player input
        choice = None
        option = ['cooperate','defect']
        while choice not in option:
            choice = raw_input("Your choice, 'cooperate' or 'defect' ? \n")
            print "you choose :", choice
        return choice

    # TODO implement
    @classmethod
    def titfortat(cls, moveId, history):
        # Titfortat : cooperate on the first move and play the opponents previous move after that
        if moveId == 1:
            return "cooperate"
        else:
            print "history-1 : ", history[-1]
            if history[-1] == (0 or 3):
                return "cooperate"
            else: # if history[-1] == (1 or 5): # or -1  
                return "defect"


    # TODO change moveId == 1 to history is empty
    def grim(self, moveId, history):
        # Grim : cooperate on the first move, and keep cooperating unless the opponent defects, in which case, defect forever
        if not history: # empty list
            self.grim = False # initiate
            return "cooperate"
        
        elif not self.grim :
            # cooperate on the first move, and keep cooperating until it get grim
            if history[-1] == (1 or 5):
                self.grim = True
            return "cooperate"
        else:
            return "defect"

    def pavlov(self, moveId, history):
        # Pavlov: cooperate on the first move, and on subsequent moves, switch strategies if you were punished on the previous move
        if not history: # empty list 
            self.strategy = "cooperate" # initiate
            return self.strategy
            
        elif history[-1] == (1 or 5):
            if self.strategy == "cooperate": self.strategy = "defect"
            else: self.strategy = "cooperate" 
        return self.strategy


class Prisoner(object):
    """docstring for Prisoner"""
    def __init__(self, name):
        self.name = name
        self.action = Action()
        self.strategy = Action.beRandom() # default strategy

    def decision(self, moveId):
        # implement gameId, strategy choice and result will follow ?
        return self.strategy


class Game(object):
    """docstring for Game"""
    def __init__(self, prisonerA, prisonerB):
        self.prisonerA = prisonerA
        self.prisonerB = prisonerB
        self.moveId = 0
        self.data = {'id': [], 'A': [], 'B': []}

    def play(self):
        self.moveId += 1
        actionOfA = self.prisonerA.strategy(self.moveId,self.data['B']) # we give the history of the adversary
        actionOfB = self.prisonerB.strategy(self.moveId,self.data['A']) # same :)

        print actionOfA, actionOfB

        if (actionOfA and actionOfB) == "defect":
            # self.prisonerA.punish
            returnA, returnB = Penalty, Penalty
            print "A & B get 2 years"
        elif actionOfA == "defect" and actionOfB == "cooperate":
            returnA = Temptation
            returnB = Sucker
            print "A is free and B get 3 years in prisons"
        elif actionOfA == "cooperate" and actionOfB == "defect":
            returnA = Sucker
            returnB = Temptation
            print "B is free and A get 3 years in prisons"
        elif (actionOfA and actionOfB) == "cooperate":
            returnA, returnB =  Reward, Reward
            print "A & B get 1 year"
        else  :
            print "Error, wrong move"
            returnA, returnB = -1, -1

        self.data['id'].append(self.moveId)
        self.data['A'].append(returnA)
        self.data['B'].append(returnB)



def main():
    prisonerA = Prisoner("A")
    prisonerB = Prisoner("B")
    game = Game(prisonerA, prisonerB)
    #prisonerA.strategy = Action.titfortat
    prisonerA.strategy = prisonerA.action.pavlov
    prisonerB.strategy = prisonerB.action.grim
    #print prisonerA.strategy(700)
    #print "Test = ", prisonerA.decision(700)
    print "A = ", prisonerA.strategy
    print "B = ", prisonerB.strategy
    for move in xrange(1,10):
        game.play()
    print game.data

if __name__ == '__main__':
    main()