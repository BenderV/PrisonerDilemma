#!/usr/bin/env python
""" A little script to play the prisoner's dilemma between bot. 
"""

__author__ = 'Benjamin Derville, benjamin.derville@gmail.com'


from prisonersdilemmagame import PrisonersDilemmaGame
from prisonersplayers import RandomPrisonerPlayer, GrimPlayer, ReinforcementLearningPlayer
from robintournament import RobinTournament
from prisonerstask import PrisonersTask
from pybrain.tools.shortcuts import buildNetwork
from pybrain import SigmoidLayer

from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.learners import Q
from pybrain.rl.experiments import Experiment, ContinuousExperiment
from pybrain.rl.explorers import EpsilonGreedyExplorer
from pybrain.rl.agents import LearningAgent

game = PrisonersDilemmaGame()
randAgent = RandomPrisonerPlayer(game, name = 'rand')
grimAgent = GrimPlayer(game, name="grimy")

# the network's outputs are probabilities of choosing the action, thus a sigmoid output layer
#net = buildNetwork(game.indim, game.outdim, outclass = SigmoidLayer)
#netAgent = ReinforcementLearningPlayer(net, game, name = 'net')

# agents = [randAgent, netAgent]
# print 'Starting tournament...'
# tourn = RobinTournament(game, agents)
# tourn.organize(1) # we play only one game
# print tourn
# print game.data


# define action-value table
av_table = ActionValueTable(32, 2)
av_table.initialize(0.)
# define Q-learning agent
learner = Q(0.5, 0.0)
learner._setExplorer(EpsilonGreedyExplorer(0.0))
agent1 = ReinforcementLearningPlayer(av_table, learner)
agent2 = ReinforcementLearningPlayer(av_table, learner)


# define the environmment (one for both)
env = PrisonersDilemmaGame()
# # define the task (the same here)
task = PrisonersTask(env)


""" We don't, we are doing by hand for now
# # finally, define experiment
# experiment = ContinuousExperiment(task, agent)
"""

agent1.color = env.startcolor
agent2.color = -agent1.color
# ready to go, start the process
while True:
    # experiment.doInteractionsAndLearn(1)
    agent1.integrateObservation(task.getObservation(agent1.color))
    agent2.integrateObservation(task.getObservation(agent2.color))
    """self.task1.performAction(self.agent1.getAction())
    self.task2.performAction(self.agent2.getAction())
    Replace by """
    env.performActions(agent1.getAction(), agent2.getAction())
    # Do the processing in the agent !
    agent1.giveReward(task.getReward(agent1.color))
    agent2.giveReward(task.getReward(agent2.color))
    agent1.learn()
    agent2.learn()
