from dilemma import Game
from strategies import *



def ml_vs_titfortat_non_iterate():
    """The MachineLearning algorithm don't care about future rewards.
    It's the non-iterated version of the game.
    The best strategy is to defect (and win 1 or 5).
    """
    print("Start a non-iterated game between MachineLearning and Titfortat")
    prisoner_a = MachineLearning("A")
    prisoner_a.qlearning.gamma = 0.0 # We don't care about future rewards
    prisoner_b = Titfortat("B")
    game = Game(prisoner_a, prisoner_b)
    game.play(10000)
    print("last 10 moves: ", prisoner_a.actions[-10:])
    print("ml values: ", prisoner_a.qlearning.values)

def ml_vs_titfortat_iterate():
    """The MachineLearning algorithm that into account the future rewards
    It's the iterated version of the game.
    The best strategy is to cooperate if the other cooperate too, otherwise, defect
    """
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

def main():
    """"
    prisoner_a = Titfortat("A")
    prisoner_b = Titfortat("B")
    game = Game(prisoner_a, prisoner_b)
    game.play(10000)
    print("last 10 moves of a: ", prisoner_a.actions[-10:])
    print("last 10 moves of b: ", prisoner_b.actions[-10:])
    """

    ml_vs_titfortat_non_iterate()
    ml_vs_titfortat_iterate()
    ml_vs_ml_non_iterate()
    ml_vs_ml_iterate()

if __name__ == '__main__':
    main()