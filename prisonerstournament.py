#!/usr/bin/env python
""" A little script to play the prisoner's dilemma between bot. 
"""

__author__ = 'Benjamin Derville, benjamin.derville@gmail.com'


from prisonersdilemmagame import PrisonersDilemmaGame
from prisonersplayers import RandomPrisonerPlayer, GrimPlayer, ReinforcementLearningPlayer
from robintournament import RobinTournament

from pybrain.tools.shortcuts import buildNetwork
from pybrain import SigmoidLayer

from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.learners import Q
from pybrain.rl.experiments import Experiment
from pybrain.rl.explorers import EpsilonGreedyExplorer


game = PrisonersDilemmaGame()
randAgent = RandomPrisonerPlayer(game, name = 'rand')
grimAgent = GrimPlayer(game, name="grimy")

# the network's outputs are probabilities of choosing the action, thus a sigmoid output layer
net = buildNetwork(game.indim, game.outdim, outclass = SigmoidLayer)
netAgent = ReinforcementLearningPlayer(net, game, name = 'net')

agents = [randAgent, netAgent]
print 'Starting tournament...'
tourn = RobinTournament(game, agents)
tourn.organize(1) # we play only one game
print tourn
print game.data



# define action-value table
av_table = ActionValueTable(32, 2)
av_table.initialize(0.)
# define Q-learning agent
learner = Q(0.5, 0.0)
learner._setExplorer(EpsilonGreedyExplorer(0.0))
agent = LearningAgent(av_table, learner)

# define the environmment
env = PrisonersDilemmaGame()
# # define the task
# ...
# # finally, define experiment
# experiment = Experiment(task, agent)

# ready to go, start the process
while True:
    experiment.doInteractions(1)
    agent.learn()
    agent.reset()


