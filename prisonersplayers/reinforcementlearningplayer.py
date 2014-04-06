__author__ = 'Benjamin Derville, benjamin.derville@gmail.com'


from prisonersplayers import RandomPrisonerPlayer

class ReinforcementLearningPlayer(RandomPrisonerPlayer):
    """Use Pybrain Reinforcement Learning to play
    By default, is random
    """
    def __init__(self, module, *args, **kwargs):
        RandomPrisonerPlayer.__init__(self, *args, **kwargs)
        self.module = module # the learning module

    def getAction(self):
    	history = self.game.getHistory(-self.color) # we want the opponent history
        if not history:
            return super(ReinforcementLearningPlayer, self).getAction()
        elif len(history)<5:
            return super(ReinforcementLearningPlayer, self).getAction()
        else:
            myactionshistory = [(0 if (res==0 or res==3) else 2) for res in history]
            spacesolution = sum(map(pow, myactionshistory[-4:], range(1, 5)))
            if myactionshistory[-5] == 0:
                spacesolution += 0
            else:
                spacesolution += 1 # we add the last bit... (Because pow(0,0)=1 !!!) 
            print sum(history[-1:])
            test = self.module.activate(myactionshistory[-5:])

            print test
            b = raw_input("pause IA !!")
            return [self.color, 'cooperate']

    def integrateObservation(data):
        # We don't use that
        self.data = data

    def giveReward(self, r):
        """ Reward or punish the agent.
            :key r: reward, if C{r} is positive, punishment if C{r} is negative
            :type r: double
        """
        reward = raw_input("reward ? :")
        return reward