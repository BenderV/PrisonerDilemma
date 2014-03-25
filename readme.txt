Prisoner's dilemma


About the prisoner dilemma 
see more at : http://en.wikipedia.org/wiki/Prisoner's_dilemma



Why dilemna
	# To complete

Rules :
Defect or Cooperate

The number of moves should not be known to the two palers
The winner is the player with the highest score in the end
Usually, there are many players :
	Do a Round Robin Tournament (to implement)


Parameters : 
we will choose the commonly used values T = 5, R = 3, P = 1, and S = 0.
	It's a positive valuation of the game,
		3 years of prison => 0 points (S for Sucker)
		2 years of prison => 1 points (P for Penalty)
		1 year  of prison => 3 points (R for Reward)
		0 year  of prison => 5 points (T for Temptation)


Basic strategies implemented: 
(1) Tit-for-tat: cooperate on the ﬁrst move, and play the last opponents move after that
(2) Grim: cooperate on the ﬁrst move, and keep cooperating unless the opponent defects, in which case, defect forever
(3) Pavlov: cooperate on the ﬁrst move, and on subsequent moves, switch strategies if you were punished on the previous move

But don't forget:
	There is no universal best strategy, as it depends upon the opponents strategy 


The Nash equilibrium solution for a two player zero-sum problem can be easily obtained as a solution to a convex optimization problem. 
We consider a problem of an iterated zero-sum game



it's a Non zero Sum Game : both players can simultaneously win or lose !!
 	=> but you can make a version of it
 	=> just change (T+S)/2 < R to (T+S = 2R)
