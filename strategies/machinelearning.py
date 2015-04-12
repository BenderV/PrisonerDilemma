import random
from .prisoner import Prisoner
import math

STATES = [('defect'), ('cooperate')] # with a history of one => what we played
ACTIONS = [('defect'), ('cooperate')] # cooperate or defect

def unexp(x):
   return math.exp(-x)

class QLearning(object):
    """docstring for QLearning"""
    def __init__(self):
      super(QLearning, self).__init__()
      self.values = {}
      self.lrate = 0.4 # step size, for now, we always learn a bit on everything.
      self.gamma = 0 # discount factor
      self.id = 0 

      # initialization
      for action in ACTIONS:
          for state in STATES:
              self.values[state, action] = 0.5

    def learn(self, state, action, reward):
        old_value = self.values[state, action]
        lrate = self.lrate

        qmax = max([self.values[action, a] for a in ACTIONS]) # just because new_state = action
        
        new_value = old_value + lrate * (reward + self.gamma * qmax  - old_value)
        self.values[state, action] = new_value


    def choose(self, state, actions):
        if not state: # if we don't have any state, randomly do an action.
            return random.choice(actions)

        self.id += 1
        if random.random() > 0.1 and self.id < 1000:
            return random.choice(actions)

        action_max_value = - 10000
        action_max = 'default'

        for action in actions:
            predict = self.values[state, action]
            if predict > action_max_value:
                action_max = action
                action_max_value = predict


        return action_max

class MachineLearning(Prisoner):
    """implement the simplest ML algorithm possible
    Non iterative version of the game
    It should learn that he should always defect"""
    def __init__(self, arg):
        super(MachineLearning, self).__init__(arg)
        self.qlearning = QLearning()
        self.last_action = None
    
    def strategy(self, history, **context):
        action = self.qlearning.choose(state=self.last_action, actions=ACTIONS)
        return action

    def punish(self, reward, **context):
        if self.last_action:
            self.qlearning.learn(state=self.last_action, action=context['action'], reward=reward)
        self.last_action = context['action']


