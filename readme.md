### Prisoner's dilemma : Machine Learning bots to solve the Prisoner's dilemma [help needed]

Python implementation of the Prisoner's dilemma with the classical strategies, and two machine 
learning agents: QLearning and DeepQLearning.

### Why

I wanted to solve the Prisoner's dilemma using machine learning bots. There is already two agents available, QLearning and DeepQLearning (Deepmind).
Both agents works on simple learning task:
- learn how to play against a given strategy (titfortat, grim, ...).
- learn to the play against another both in the non iterated version of the game.

However, both agents (QLearning/DeepQLearning) still fail to converge to work together on the iterated version of the game. It would make themself better if they would learn to cooperate with each other but it appears that they rarely do so. They frequently implement the "titfortat" strategy, but are trapped in a devious circle where they alternate "defect" and "cooperate".

### Where to start

##### Installation

`pip install numpy pandas`

- You will need the Tensorflow algorithm to use DeepQLearning. See: http://www.tensorflow.org/get_started/os_setup.html#binary-installation
- If you want to run the notebook locally, you will need to download jupyter: `pip install jupyter`
- If you want to display with plotly.js, as on the jupyter notebook: `pip install plotly`

You can start by the Jupyter Notebook to see how to use the library and some example of game.
Or check the test.py file for example of game.

##### TO DO

- Make two machine learning bots cooperate in an iterated version of the game. (and understand why it doesn't do so as for now)

I would gladly accept your help on this issue. Thanks.


### About the Prisoner's dilemma

Read more about the Prisoner's dilemma [here](http://en.wikipedia.org/wiki/Prisoner's_dilemma)

```
Two members of a criminal gang are arrested and imprisoned. 
Each prisoner is in solitary confinement with no means of speaking to 
or exchanging messages with the other.
The police admit they don't have enough evidence 
to convict the pair on the principal charge. 
They plan to sentence both to a year in prison on a lesser charge.
Simultaneously, the police offer each prisoner a Faustian bargain. 
Each prisoner is given the opportunity either to betray (defect) the other,
by testifying that the other committed the crime,
or to cooperate with the other by remaining silent. 
Here's how it goes:
- If A and B both defect the other
    each of them serves 2 years in prison
- If A defects B but B remains silent
    A will be set free and B will serve 3 years in prison
- If A and B both remain silent
    both of them will only serve 1 year in prison
```

### Parameters : 
The commonly used values T = 5, R = 3, P = 1, and S = 0.
It's a positive valuation of the game,
- 3 years of prison => 0 points (S for Sucker)
- 2 years of prison => 1 points (P for Penalty)
- 1 year  of prison => 3 points (R for Reward)
- 0 year  of prison => 5 points (T for Temptation)
