import math
import random

"""
Two members of a criminal gang are arrested and imprisoned. Each prisoner is in solitary confinement with no means of speaking to or exchanging messages with the other. The police admit they don't have enough evidence to convict the pair on the principal charge. They plan to sentence both to a year in prison on a lesser charge. Simultaneously, the police offer each prisoner a Faustian bargain. Each prisoner is given the opportunity either to betray the other, by testifying that the other committed the crime, or to cooperate with the other by remaining silent. Here's how it goes:
If A and B both betray the other, each of them serves 2 years in prison
If A betrays B but B remains silent, A will be set free and B will serve 3 years in prison (and vice versa)
If A and B both remain silent, both of them will only serve 1 year in prison (on the lesser charge)
"""

class Action(object):
    """docstring for Action"""
    def __init__(self, arg):
        super(Action, self).__init__()
        self.arg = arg
    
    @classmethod
    def beSilent(cls):
        return "silent"
    
    @classmethod
    def betray(cls):
        return "betray"
    
    @classmethod
    def beRandom(cls, probabilityOfSilent = 0.5):
        if(random.uniform(0,1) < probabilityOfSilent):
            return "silent"
        else:
            return "betray"

    # to test...
    @classmethod
    def beHuman(cls):
        # We ask for the player input
        choice = None
        option = ['silent','betray']
        while choice not in option:
            choice = raw_input("Your choice, 'silent' or 'betray' ? \n")
            print "you choose :", choice
        return choice
        

class Prisoner(object):
    """docstring for Prisoner"""
    def __init__(self, name):
        self.name = name
        self.strategy = Action.beSilent()

    def decision(self):
        return self.strategy



class Game(object):
    """docstring for Game"""
    def __init__(self, prisonerA, prisonerB):
        self.prisonerA = prisonerA
        self.prisonerB = prisonerB

    def play(self):
        actionOfA = self.prisonerA.decision()
        actionOfB = self.prisonerB.decision()   
        if (actionOfA and actionOfB) == "betray":
            return "A & B get 2 years"
        if actionOfA == "betray" and actionOfB == "silent":
            return "A is free and B get 3 years in prisons"
        if actionOfA == "silent" and actionOfB == "betray":
            return " B is free and A get 3 years in prisons"
        if (actionOfA and actionOfB) == "silent":
            return "A & B get 1 year"


def main():
    prisonerA = Prisoner("A")
    prisonerB = Prisoner("B")
    game = Game(prisonerA, prisonerB)
    print "A = ", prisonerA.strategy
    print "B = ", prisonerB.strategy
    print game.play()

    prisonerA.strategy = Action.betray()
    print "A = ", prisonerA.strategy
    print "B = ", prisonerB.strategy
    print game.play()

    prisonerA.strategy = Action.beHuman()
    print game.play()

def test():
    prisonerA = Prisoner("A")
    prisonerB = Prisoner("B")
    game = Game(prisonerA, prisonerB)

    prisonerA.strategy = Action.beSilent()
    prisonerB.strategy = Action.beSilent()
    assert(game.play() == "A & B get 1 year")
    
    prisonerA.strategy = Action.betray()
    prisonerB.strategy = Action.betray()
    assert(game.play() == "A & B get 2 years")


if __name__ == '__main__':
    #test()
    main()