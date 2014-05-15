'''
Created on Oct 1, 2012

Code for Exercise 4.16 from AI: A Modern Approach

@author: ecejjar
'''

import heapq
from random import choice
from Ex39 import ProblemSolver
try:
    from functools import reduce    # Only for Python 3
except:
    pass

class LSOProblemSolver(ProblemSolver):
    '''
    A problem solver using local search and optimization techniques
    '''
    
    def __init__ ( self, noderepr = None ):
        '''
        Constructor
        '''
        super(LSOProblemSolver, self).__init__(noderepr)
        
    @staticmethod
    def hillClimbingGenerator ( successor, value ):
        def nestedGenerator ( fringe ):
            for n in fringe:
                #it = map(lambda s: LSOProblemSolver.Node((value(s), s, n)), successor(n.item()))
                it = \
                    filter(lambda d: d.cost() < n.cost(), \
                           map(lambda s: LSOProblemSolver.Node((value(s), s, n)), \
                               successor(n.item())))
                descendants = list(it)
                if any(descendants):    # ADDED
                    heapq.heapify(descendants)
                #if descendants and descendants[0].cost() < n.cost(): # the lower the cost, the higher the value
                    yield [descendants[0]]
        return nestedGenerator

    @staticmethod
    def stochasticHillClimbingGenerator ( successor, value ):
        def nestedGenerator ( fringe ):
            for n in fringe:
                it = \
                    filter(lambda d: d.cost() < n.cost(), \
                           map(lambda s: LSOProblemSolver.Node((value(s), s, n)), \
                               successor(n.item())))
                descendants = list(it)
                if any(descendants):
                    V = reduce(lambda s1, s2: s1.cost() + s2.cost(), descendants)
                    while True:
                        desc = choice(descendants)
                        v = desc.cost() / V
                        