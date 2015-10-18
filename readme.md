### Prisoner's dilemma

Python Implementation of the Prisonner's dilemma.

Readme more about the Prisoner's dilemma [here](http://en.wikipedia.org/wiki/Prisoner's_dilemma)

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

### Why

I wanted to solve the Prisoner's dilemma using machine learning bot. The current implementation is a simple QLearning algorithm. The next step is too implement a Deep Q Learning to allow the bot to create more sophisticated strategies.

