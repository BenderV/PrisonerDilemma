__author__ = 'Benjamin Derville, benjamin.derville@gmail.com'

# from pybrain.rl.environments.twoplayergames.twoplayergame import TwoPlayerGame
from twoplayergame import SimultaneousTwoPlayerGame
from pybrain.utilities import Named
import itertools

class RobinTournament(Named):
    """Round-robin tournament : Every strategy play against all other
    Including itself.
    The return is a flat data, with the name of the 'player', the adversary
    and the data/result of the player
    To only fight strategy1 vs strategy1, just do strategies ="strategy1","strategy1"]
    """

    # do all moves need to be checked for legality?
    forcedLegality = False

    def __init__(self, env, agents):
        assert isinstance(env, SimultaneousTwoPlayerGame)
        self.startcolor = env.startcolor
        self.env = env
        self.agents = agents
        for a in agents:
            a.game = self.env
        self.reset()
        self.iterations = 100

    def reset(self):
        # a dictionnary attaching a list of outcomes to a player-couple-key
        self.results = {}
        self.rounds = 0
        self.numGames = 0

    def _produceAllPairs(self):
        """ produce a list of all pairs of agents (assuming ab == ba)"""
        return itertools.combinations(self.agents, 2)


    def _oneGame(self, p1, p2):
        """ play one game between two agents p1 and p2."""
        self.numGames += 1
        self.env.reset()
        players = (p1, p2)
        p1.color = self.startcolor
        p2.color = -p1.color
        p1.newEpisode()
        p2.newEpisode()
        i = 0
        for _ in xrange(0, self.iterations):
            act1 = p1.getAction()
            act2 = p2.getAction()

            self.env.performAction([act1, act2])

        b = raw_input("pause...")
        if players not in self.results:
            self.results[players] = []
        wincolor = self.env.getWinner()
        if wincolor == p1.color:
            winner = p1
        else:
            winner = p2
        self.results[players].append(winner)

    def organize(self, repeat=1):
        """ have all agents play all others in all orders, and repeat. """
        for _ in range(repeat):
            self.rounds += 1
            for p1, p2 in self._produceAllPairs():
                self._oneGame(p1, p2)
        return self.results


    def __str__(self):
        s = 'Tournament results (' + str(self.rounds) + ' rounds, ' + str(self.numGames) + ' games):\n'
        for p1, p2 in self._produceAllPairs():
            wins = len(filter(lambda x: x == p1, self.results[(p1, p2)]))
            losses = len(filter(lambda x: x == p2, self.results[(p1, p2)]))
            s += ' ' * 3 + p1.name + ' won ' + str(wins) + ' times and lost ' + str(losses) + ' times against ' + p2.name + '\n'
        return s
