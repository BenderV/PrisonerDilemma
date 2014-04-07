__author__ = 'Benjamin Derville, benjamin.derville@gmail.com'


from prisonersplayers import RandomPrisonerPlayer
from pybrain.rl.agents import LearningAgent
from random import choice

class ReinforcementLearningPlayer(LearningAgent, RandomPrisonerPlayer):
    """Use Pybrain Reinforcement Learning to play
    By default, is random
    """
    def __init__(self, module, *args, **kwargs):
        LearningAgent.__init__(self, module, *args, **kwargs)

    def getAction(self):
        # history = self.getHistory(-self.color) # we want the opponent history
        history = self.history
        if not history:
            return [self.color, choice(['cooperate','defect'])]
        elif len(history)<5:
            self.lastaction = 1.0
            return [self.color, choice(['cooperate','defect'])]
        else:
            myactionshistory = [(0 if (res==0 or res==3) else 2) for res in history]
            """spacesolution = sum(map(pow, myactionshistory[-4:], range(1, 5)))
            if myactionshistory[-5] == 0:
                spacesolution += 0
            else:
                spacesolution += 1 # we add the last bit... (Because pow(0,0)=1 !!!) 
            print sum(history[-1:])
            test = self.module.activate(myactionshistory[-5:])

            print test
            b = raw_input("pause IA !!")
            return [self.color, 'cooperate']"""
            super(LearningAgent, self).getAction()

    def integrateObservation(self, data):
        self.history = data        
        self.lastobs = '8'
        self.lastaction = None
        self.lastreward = None