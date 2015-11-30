from .prisoner import Prisoner
import math
from .agents._models import MLP
from .agents.deepqlearning import DiscreteDeepQ
from .agents.qlearning import QLearning
import tensorflow as tf
import random
import numpy as np

# https://github.com/nivwusquorum/tensorflow-deepq/blob/master/notebooks/game_memory.ipynb
# https://github.com/nivwusquorum/tensorflow-deepq


ACTIONS = [('defect'), ('cooperate')] # cooperate or defect

class DeepQLearnerAdaptater(object):
    def __init__(self, num_actions, 
                       observation_size, 
                       decay=0.9, 
                       learning_rate=0.1, 
                       exploration_random_prob=0.2,
                       exploitation_random_prob=0.0,
                       exploration_period=8000,
                       store_every_nth=5,
                       train_every_nth=5,
                       minibatch_size=32,
                       max_experience=30000,
                       target_network_update_rate=0.01,
                       scope="MLP"):

        self.observation_size = observation_size
        self.num_actions = num_actions

        optimizer = tf.train.RMSPropOptimizer(learning_rate=learning_rate, decay=decay)
        self.brain = MLP([observation_size,], [num_actions], [tf.identity], scope=scope)
        self.session = tf.InteractiveSession()

        self.deepqlearning = DiscreteDeepQ(
           observation_size=observation_size,
           num_actions=num_actions,
           observation_to_actions=self.brain,
           optimizer=optimizer,
           session=self.session,
           exploration_random_prob=float(exploration_random_prob),
           exploitation_random_prob=float(exploitation_random_prob),
           exploration_period=exploration_period,
           store_every_nth=store_every_nth,
           train_every_nth=train_every_nth,
           minibatch_size=minibatch_size,
           discount_rate=decay,
           max_experience=max_experience,
           target_network_update_rate=target_network_update_rate,
        )
        self.session.run(tf.initialize_all_variables())

    def __del__(self):
        self.session.close()

    def learn(self, state, action, reward, new_state):
        state = np.array(state[-self.observation_size:])
        new_state = np.array(new_state[-self.observation_size:])

        self.deepqlearning.store(state, action, reward, new_state)
        self.deepqlearning.training_step()

    def choose(self, state):
        state = np.array(state[-self.observation_size:])
        if not state: # if we don't have any state, randomly do an action.
            return random.choice(range(self.num_actions))
        return self.deepqlearning.action(observation=state)

class MachineLearning(Prisoner):
    """implement the simplest ML algorithm possible
    Non iterative version of the game
    It should learn that he should always defect"""
    def __init__(self, name, agent=False): # False => automatically generated
        super(MachineLearning, self).__init__(name)
        self.agent = agent if agent else QLearning(2)
        self.last_action = None
    
    def punish(self, state, action, reward, new_state):
        action = ACTIONS.index(action)
        if self.last_action:
            self.agent.learn(state=state, action=action, reward=reward, new_state=new_state)
        self.last_action = True

    def strategy(self, state, **context):
        action = ACTIONS[self.agent.choose(state=state)]
        self.actions.append(action)
        return action

