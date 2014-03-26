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
    def cooperate(cls, *args):
        return "cooperate"
    
    @classmethod
    def defect(cls, *args):
        return "defect"
    
    @classmethod
    def beRandom(cls, *args):
        if(random.uniform(0,1) < 0.5):
            return "cooperate"
        else:
            return "defect"

    @classmethod
    def beHuman(cls, moveId, history):
        # We ask for the player input
        choice = None
        option = ['cooperate','defect']
        while choice not in option:
            choice = raw_input("Your choice, 'cooperate' or 'defect' ? \n")
            print "you choose :", choice
        return choice


    @classmethod
    def titfortat(cls, moveId, history):
        # Titfortat : cooperate on the first move and play the opponents previous move after that
        if moveId == 1:
            return "cooperate"
        else:
            if history[-1] in (0, 3):
                return "cooperate"
            else: # if history[-1] == (1 or 5): # or -1  
                return "defect"

    def grim(self, moveId, history):
        # Grim : cooperate on the first move, and keep cooperating unless the opponent defects, in which case, defect forever
        if not history: # empty list
            self.grim = False # initiate
            return "cooperate"
        
        elif not self.grim :
            # cooperate on the first move, and keep cooperating until it get grim
            if history[-1] in (1, 5):
                self.grim = True
                return "defect"
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
    def __init__(self, name, strategy=Action.beRandom):
        self.name = name
        self.action = Action()
        self.strategy = strategy # default strategy

    def decision(self, moveId, history):
        # implement gameId, strategy choice and result will follow ?
        return self.action.strategy


class Game(object):
    """docstring for Game"""
    def __init__(self, A, B):
        "initialize with the Prisoners"
        self.prisonerA = A
        self.prisonerB = B
        self.moveId = 0
        self.data = {'id': [], 'A': [], 'B': []}

    @classmethod
    def fromStrategy(cls, strategyA, strategyB):
        "initialize game with the strategy names"
        prisonerA = Prisoner("A", strategyA)
        prisonerB = Prisoner("B", strategyB)
        return cls(prisonerA, prisonerB)

    def play(self, moves): # add number of game
        for x in xrange(0,moves):
            self.playAMove()

    def playAMove(self):
        self.moveId += 1
        actionOfA = self.prisonerA.strategy(self.moveId,self.data['B']) # we give the history of the adversary
        actionOfB = self.prisonerB.strategy(self.moveId,self.data['A']) # same :)

        # print "A = ",actionOfA, "B = ", actionOfB

        if actionOfA == actionOfB == "defect":
            # self.prisonerA.punish
            returnA, returnB = Penalty, Penalty
            # print "A & B get 2 years"
        elif actionOfA == "defect" and actionOfB == "cooperate":
            returnA = Temptation
            returnB = Sucker
            # print "A is free and B get 3 years in prisons"
        elif actionOfA == "cooperate" and actionOfB == "defect":
            returnA = Sucker
            returnB = Temptation
            # print "B is free and A get 3 years in prisons"
        elif (actionOfA and actionOfB) == "cooperate":
            returnA, returnB =  Reward, Reward
            # print "A & B get 1 year"
        else  :
            # print "Error, wrong move"
            returnA, returnB = -1, -1

        self.data['id'].append(self.moveId)
        self.data['A'].append(returnA)
        self.data['B'].append(returnB)


def test():
    prisonerA = Prisoner("A")
    prisonerB = Prisoner("B")

    game = Game(Action.cooperate, Action().grim)
    for move in xrange(1,10):
        game.play()
    print game.data
    assert(game.data['A']==[3, 3, 3, 3, 3, 3, 3, 3, 3])
    assert(game.data['B']==[3, 3, 3, 3, 3, 3, 3, 3, 3])



def main():
    game = Game.fromStrategy(Action().titfortat, Action().beRandom)
    # game = Game(titfortat, random) #=> create a person name titfortat and pass it (avantage : accumulation des scores ?) ou passer juste la technique
    # game.prisonerA.strategy = game.prisonerB.action.beRandom # or Action.beRandom

    print "A = ", game.prisonerA.strategy
    print "B = ", game.prisonerB.strategy
    game.play(1000)
    print "Result A = ", sum(game.data['A'])
    print "Result B = ", sum(game.data['B'])

if __name__ == '__main__':
    #test()
    main()