"""Implement the pattern for prisoner strategy
"""

class Prisoner(object):
    """docstring for Prisoner"""
    def __init__(self, name, strategy = "cooperate"):
        self.name = name
        self.history = [] # history of action ?
        self.rewards = []
        self.actions = []

    def strategy(self, **context):
        pass

    def punish(self, **context):
        pass
