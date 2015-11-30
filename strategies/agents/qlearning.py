import random
from _models import linear_annealing

class QLearning(object):
    """docstring for QLearning"""
    def __init__(self, num_actions, 
                       observation_size = "auto", 
                       decay=0.9, 
                       learning_rate=0.1, 
                       exploration_period=8000, 
                       explore_random_prob=0.2, 
                       exploit_random_prob=0.0):
      super(QLearning, self).__init__()
      self.id = 0
      self.values = {}
      self.learning_rate = learning_rate # step size, for now, we always learn a bit on everything.
      self.decay = decay # discount factor  
      self.exploration_period = exploration_period
      self.explore_random_prob = explore_random_prob
      self.exploit_random_prob = exploit_random_prob
      self.epsilon = lambda x: linear_annealing(x, self.exploration_period, 
                                                   self.explore_random_prob, 
                                                   self.exploit_random_prob)
      self.actions = range(num_actions)
      self.observation_size = observation_size

    def learn(self, state, action, reward, new_state):
        if self.observation_size == "auto": # We try to predict the size
            self.observation_size = len(state)
        state = tuple(state[-self.observation_size:]) # We take only the last episode
        new_state = tuple(new_state[-self.observation_size:])

        old_value = self.values.get((state, action), 0.5) # try to get, otherwise init at 0.5
        learning_rate = self.learning_rate

        qmax = max([self.values.get((new_state, _action), 0.5) for _action in self.actions])
        
        new_value = old_value + learning_rate * (reward + self.decay * qmax  - old_value)
        self.values[state, action] = new_value


    def choose(self, state):
        if not state: # if we don't have any state, randomly do an action.
            return random.choice(self.actions)

        if self.observation_size == "auto": # We try to predict the size
            self.observation_size = len(state)
        state = tuple(state[-self.observation_size:]) # We take only the last episode

        self.id += 1
        if random.random() < self.epsilon(self.id): # We explore
            return random.choice(self.actions)

        return max(self.actions, key=lambda action: self.values.get((state, action), 0.5))
