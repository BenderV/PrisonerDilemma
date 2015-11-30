from dilemma import Game
from strategies import *
from collections import Counter

"""
If the machine learning algorithm don't care about future rewards. (decay == 0)
It's the non-iterated version of the game.
The best strategy is to defect (and win 1 or 5).
 
If the machine learning algorithm care about future rewards.
It's the iterated version of the game.
The best strategy is up to the opponant strategy.
"""


def ml_vs_titfortat_non_iterate():
    
    print("Start a non-iterated game between MachineLearning and Titfortat")
    prisoner_a = MachineLearning("A")
    prisoner_a.qlearning.gamma = 0.0 # We don't care about future rewards
    prisoner_b = Titfortat("B")
    game = Game(prisoner_a, prisoner_b)
    game.play(10000)
    print("last 10 moves: ", prisoner_a.actions[-10:])
    print("ml values: ", prisoner_a.qlearning.values)

def ml_vs_titfortat_iterate():
    print("Start an _iterated_ game between MachineLearning and Titfortat")
    prisoner_a = MachineLearning("A")
    prisoner_a.qlearning.gamma = 0.9 # We deeply care about future rewards
    prisoner_b = Titfortat("B")
    game = Game(prisoner_a, prisoner_b)
    game.play(10000)
    print("last 10 moves: ", prisoner_a.actions[-10:])

def ml_vs_ml_non_iterate():
    print("Start a non-iterated game between two MachineLearning bots")
    prisoner_a = MachineLearning("A")
    prisoner_a.qlearning.gamma = 0.0 # We don't care about future rewards
    prisoner_b = MachineLearning("B")
    prisoner_b.qlearning.gamma = 0.0 # We don't care about future rewards
    game = Game(prisoner_a, prisoner_b)
    game.play(10000)
    print("last 10 moves of a: ", prisoner_a.actions[-10:])
    print("last 10 moves of b: ", prisoner_b.actions[-10:])

def ml_vs_ml_iterate():
    print("Start an _iterated_ game between two MachineLearning bots")
    prisoner_a = MachineLearning("A")
    prisoner_a.qlearning.gamma = 0.9 # We care about future rewards
    prisoner_b = MachineLearning("B")
    prisoner_b.qlearning.gamma = 0.9 # We care about future rewards
    game = Game(prisoner_a, prisoner_b)
    game.play(10000)
    print("last 10 moves of a: ", prisoner_a.actions[-10:])
    print("last 10 moves of b: ", prisoner_b.actions[-10:])

def deepqlearning_vs_titfortat_non_iterate():
    print("Start a non-iterated game between DeepQLearning and Titfortat")
    agent_a = DeepQLearnerAdaptater(2, 1, decay=0.0, learning_rate=0.02)
    prisoner_a = MachineLearning("A", agent=agent)
    prisoner_b = Titfortat("B")
    game = Game(prisoner_a, prisoner_b)
    game.play(10000)
    print('Last 1000 moves:')
    print('prisoner_a:', Counter(prisoner_a.actions[-1000:]))
    print('prisoner_b:', Counter(prisoner_b.actions[-1000:]))

def deepqlearning_vs_titfortat_non_iterate():
    print("Start an non-iterated game between DeepQLearning and Titfortat")
    agent_a = DeepQLearnerAdaptater(2, 1, decay=0.0, learning_rate=0.02)
    prisoner_a = MachineLearning("A", agent=agent)
    prisoner_b = Titfortat("B")
    game = Game(prisoner_a, prisoner_b)
    game.play(10000)
    print('Last 1000 moves:')
    print('prisoner_a:', Counter(prisoner_a.actions[-1000:]))
    print('prisoner_b:', Counter(prisoner_b.actions[-1000:]))

def deepqlearning_vs_deepqlearning_iterate():
    print("Start an _iterated_ game between DeepQLearning and Titfortat")
    agent_a = DeepQLearnerAdaptater(2, 1, decay=0.9, learning_rate=0.02)
    prisoner_a = MachineLearning("A", agent=agent)
    prisoner_b = Titfortat("B")
    game = Game(prisoner_a, prisoner_b)
    game.play(10000)
    print('Last 1000 moves:')
    print('prisoner_a:', Counter(prisoner_a.actions[-1000:]))
    print('prisoner_b:', Counter(prisoner_b.actions[-1000:]))


def main():
    pass

if __name__ == '__main__':
    main()