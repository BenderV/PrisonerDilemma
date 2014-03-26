"""Prisoners Dilemma 

Two members of a criminal gang are arrested and imprisoned. 
Each prisoner is in solitary confinement with no means of speaking to 
or exchanging messages with the other.
The police admit they don't have enough evidence 
to convict the pair on the principal charge. 
They plan to sentence both to a year in prison on a lesser charge.
Simultaneously, the police offer each prisoner a Faustian bargain. 
Each prisoner is given the opportunity either to betray (defect) the other,
by testifying that the other committed the crime,
or to cooperate with the other by remaining silent. 
Here's how it goes:
If A and B both defect the other
    each of them serves 2 years in prison
If A defects B but B remains silent
    A will be set free and B will serve 3 years in prison
If A and B both remain silent
    both of them will only serve 1 year in prison
"""

import random


REWARD = 3
SUCKER = 0
TEMPTATION = 5
PENALTY = 1


class Prisoner(object):
    """docstring for Prisoner"""
    def __init__(self, name, strategy = "cooperate"):
        self.name = name
        self.setstrategy(strategy)
        # The variable for the strategies
        self.defaultstrategy = "cooperate"
        self.grim = False # we are calm by nature

    def setstrategy(self, strategy):
        if strategy == "cooperate" : 
            self.strategy = self.cooperate
        elif strategy == "defect" :
            self.strategy = self.defect
        elif strategy == "random" :
            self.strategy = self.random
        elif strategy == "human" :
            self.strategy = self.human
        elif strategy == "titfortat" :
            self.strategy = self.titfortat
        elif strategy == "grim" :
            self.strategy = self.grim
        elif strategy == "pavlov" :
            self.strategy = self.pavlov
        else:
            self.strategy = self.human # easier to debug 

    @classmethod
    def cooperate(cls, *args):
        """Always cooperate."""
        return "cooperate"
    
    @classmethod
    def defect(cls, *args):
        """Always defect."""
        return "defect"
    
    @classmethod
    def random(cls, *args):
        """Cooperate or Defect at random."""
        if(random.uniform(0, 1) < 0.5):
            return "cooperate"
        else:
            return "defect"

    @classmethod
    def human(cls, move_id, history):
        """We ask for the player input."""
        choice = None
        option = ['cooperate','defect']
        while choice not in option:
            print "move n_", move_id
            print "history of the adversary : ", history
            choice = raw_input("Your choice, 'cooperate' or 'defect' ? \n")
        
        return choice

    @classmethod
    def titfortat(cls, move_id, history):
        """Cooperate at first, and play the opponents previous move after."""
        if move_id == 1:
            return "cooperate"
        else:
            if history[-1] in (0, 3):
                return "cooperate"
            else: # if history[-1] == (1 or 5): # or -1  
                return "defect"

    def grim(self, move_id, history):
        """Cooperate unless the opponent defects, in which case, defect forever.
        """
        if not history: # empty list
            self.grim = False # initiate
            return "cooperate"
        
        elif not self.grim :
            if history[-1] in (1, 5):
                self.grim = True
                return "defect"
            return "cooperate"
        else:
            return "defect"

    def pavlov(self, move_id, history):
        """Cooperate on the first move and on subsequent moves,
        switch strategies if you were punished on the previous move
        """
        if not history: # empty list 
            self.strategy = "cooperate" # initiate
            return self.strategy
            
        elif history[-1] in (1 or 5):
            if self.strategy == "cooperate": 
                self.strategy = "defect"
            else:
                self.strategy = "cooperate" 
        return self.strategy




class Game(object):
    """docstring for Game"""
    def __init__(self, prisoner_a, prisoner_b):
        "initialize with the Prisoners"
        self.prisoner_a = prisoner_a
        self.prisoner_b = prisoner_b
        self.move_id = 0
        self.data = {'id': [], 'A': [], 'B': []}

    @classmethod
    def fromstrategy(cls, strategy_a, strategy_b):
        "initialize game with the strategy names"
        prisoner_a = Prisoner("A", strategy_a)
        prisoner_b = Prisoner("B", strategy_b)
        return cls(prisoner_a, prisoner_b)

    def play(self, moves): # add parameters of the game
        """Play x times"""
        for _ in xrange(0, moves):
            self.play_a_move()

    def play_a_move(self):
        """Execute one iteration of the game
        We ask for strategy and then save the results
        """
        self.move_id += 1
        # we give the history of the adversary
        print self.prisoner_a.name
        print self.prisoner_a.strategy
        action_a = self.prisoner_a.strategy(self.move_id, self.data['B'])
        action_b = self.prisoner_b.strategy(self.move_id, self.data['A'])

        # print "A = ",action_a, "B = ", action_b

        if action_a == action_b == "defect":
            # self.prisoner_a.punish
            return_a, return_b = PENALTY, PENALTY
            # print "A & B get 2 years"
        elif action_a == "defect" and action_b == "cooperate":
            return_a = TEMPTATION
            return_b = SUCKER
            # print "A is free and B get 3 years in prisons"
        elif action_a == "cooperate" and action_b == "defect":
            return_a = SUCKER
            return_b = TEMPTATION
            # print "B is free and A get 3 years in prisons"
        elif (action_a and action_b) == "cooperate":
            return_a, return_b =  REWARD, REWARD
            # print "A & B get 1 year"
        else  :
            # print "Error, wrong move"
            return_a, return_b = -1, -1

        self.data['id'].append(self.move_id)
        self.data['A'].append(return_a)
        self.data['B'].append(return_b)


def test():
    """Test the game engine
    """
    prisoner_a = Prisoner("A", "cooperate()")
    prisoner_b = Prisoner("B", "grim")
    game = Game(prisoner_a, prisoner_b)
    game.play(10)
    print game.data
    assert(game.data['A']==[3, 3, 3, 3, 3, 3, 3, 3, 3])
    assert(game.data['B']==[3, 3, 3, 3, 3, 3, 3, 3, 3])



def main():
    """ We give the choice of what to do 
    Humans player or strategy tests
    """
    a = Prisoner("A", "grim")
    b = Prisoner("B", "random")
    game = Game.fromstrategy(a, b)

    print "A = ", game.prisoner_a.strategy
    print "B = ", game.prisoner_b.strategy
    game.play(1000)
    print "Result A = ", sum(game.data['A'])
    print "Result B = ", sum(game.data['B'])

if __name__ == '__main__':
    #test()
    main()