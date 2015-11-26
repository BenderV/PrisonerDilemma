import random
from .prisoner import Prisoner
import math

"""
from sknn.mlp import Classifier, Layer
nn = Classifier(
    layers=[
        Layer("Maxout", units=100, pieces=2),
        Layer("Softmax")],
    learning_rate=0.001,
    n_iter=25)
"""
ACTIONS = [('defect'), ('cooperate')] # cooperate or defect

def unexp(x):
   return math.exp(-x)

# 1. read image
# 2. generate state
# 3. choose which action in gonna lead to be the best next state
# 4. 
# class nnAdapteur(object):
#     """docstring for nnAdapteur"""
#     def __init__(self, arg):
#         super(nnAdapteur, self).__init__()
#         self.arg = arg


# class DeepQLearning(object):
#     """DeepQLearning is a QLearning backed by a neural network"""
#     def __init__(self, arg):
#         super(QneuralLearning, self).__init__()
#         self.values = {}
#         self.lrate = 0.4 # step size, for now, we always learn a bit on everything.
#         self.gamma = 0 # discount factor, tell if we care about the future.
#         self.epsilon = 0.1

#     def learn(self, state, action, new_state, reward):
#         # We need to train the neural network to determine wheter a state is good.
#         # This also integrate wheter a state actions are available.
#         action_evaluation = nn.predict(state + action)
#         # qmax = state_evaluation = max(state result of actions)
#         qmax = max([nn.predict(new_state + action) for action in ACTIONS]) # just because new_state = action
        
#         stateaction_value = reward + self.gamma * qmax  - action_evaluation
#         nn.fit(state + action, stateaction_value)
   
#     def choose(self, state, actions):
#         # => should be changed to random nn.
#         if not state: # if we don't have any state, randomly do an action.
#             return random.choice(actions)

#         if random.random() < self.epsilon: # We explore
#             return random.choice(actions)
#         # else, We try to exploit

#         # Select best options...
#         best_action = max(actions, key=lambda action: nn.predict(state, action))
#         return best_action

  
class QLearning(object):
    """docstring for QLearning"""
    def __init__(self):
      super(QLearning, self).__init__()
      self.values = {}
      self.lrate = 0.22 # step size, for now, we always learn a bit on everything.
      self.gamma = 0 # discount factor
      self.id = 0
      self.epsilon = lambda x : 0.1 if x < 7000 else 0

    def learn(self, state, action, reward, new_state):
        state = state[-1] # We take only the last episode
        new_state = new_state[-1]

        old_value = self.values.get((state, action), 0.5) # try to get, otherwise init at 0.5
        lrate = self.lrate

        qmax = max([self.values.get((new_state, action), 0.5) for action in ACTIONS])
        
        new_value = old_value + lrate * (reward + self.gamma * qmax  - old_value)
        self.values[state, action] = new_value


    def choose(self, state, actions):
        if not state: # if we don't have any state, randomly do an action.
            return random.choice(actions)
        state = state[-1] # We take only the last episode

        self.id += 1
        if random.random() < self.epsilon(self.id): # We explore
            return random.choice(actions)

        return max(ACTIONS, key=lambda action: self.values.get((state, action), 0.5))

class MachineLearning(Prisoner):
    """implement the simplest ML algorithm possible
    Non iterative version of the game
    It should learn that he should always defect"""
    def __init__(self, arg):
        super(MachineLearning, self).__init__(arg)
        self.qlearning = QLearning()
        self.last_action = None
    
    def strategy(self, state, **context):
        action = self.qlearning.choose(state=state, actions=ACTIONS)
        self.actions.append(action)
        return action

    def punish(self, state, action, reward, new_state):
        if self.last_action:
            self.qlearning.learn(state=state, action=action, reward=reward, new_state=new_state)
        self.last_action = action


