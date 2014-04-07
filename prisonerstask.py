__author__ = 'Tom Schaul, tom@idsia.ch'

from scipy import clip, asarray

from pybrain.rl.environments.task import Task
from numpy import *

class PrisonersTask(Task):
    """ A task is associating a purpose with an environment. It decides how to evaluate the observations, potentially returning reinforcement rewards or fitness values. 
    Furthermore it is a filter for what should be visible to the agent.
    Also, it can potentially act as a filter on how actions are transmitted to the environment. """

    def __init__(self, environment):
        """ All tasks are coupled to an environment. """
        self.env = environment
        self.lastreward = 0 # r = last reward

    def performAction(self, action):
        """ A filtered mapping towards performAction of the underlying environment. """                
        self.env.performAction(action)
        
    def getObservation(self, color):
        """ A filtered mapping to getSample of the underlying environment. """
        if color == self.env.BLACK:
            return self.env.data['B'][-5:]
        else:
            return self.env.data['W'][-5:]

    def getReward(self, color):
        """ Compute and return the current reward (i.e. corresponding to the last action performed) """
        history = self.env.getHistory(color)
        reward = sum(history[-1:])
        cur_reward = self.lastreward
        self.lastreward = reward
        return cur_reward

    @property
    def indim(self):
        return self.env.indim
    
    @property
    def outdim(self):
        return self.env.outdim