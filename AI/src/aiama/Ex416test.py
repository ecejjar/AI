'''
Created on Oct 2, 2012

@author: ecejjar
'''

import unittest
from Ex39 import Problem
from Ex416 import LSOProblemSolver

class LSOProblemSolverTest(unittest.TestCase):

    def testQueens ( self, n = 8 ):
        initial = tuple(zip((0,)*n, range(n)))
        cost = lambda x,y: 1
        
        def successor ( board ):
            result = []
            for q in board:
                t = tuple(filter(lambda x: x!=q, board))
                for row in range(n):
                    new_queen = (row, q[1])
                    if new_queen != q:
                        result.append(t + (new_queen,))
            return result                        
            
        def value ( board ):
            def attacks ( q1, q2 ):
                return q1 != q2 and (q1[0]==q2[0] or q1[1]==q2[1] or abs(q1[0]-q2[0]) == abs(q1[1]-q2[1]))
            
            pairs = set()
            for q1 in board:
                for q2 in board:
                    if attacks(q1,q2):
                        pairs.add((min(q1,q2), max(q1,q2)))
            return len(pairs)

        def goal ( board ):
            return value(board) == 0
        
        #print("Successors of initial state ", str(initial), " with value ", value(initial))
        #for s in successor(initial): print(str(s), ", value: ", value(s))

        # Note that hill-climbing does not always find a solution,
        # thus we can't check for solver.solved(problem) here        
        problem = Problem(initial, goal, successor, cost)
        solver = LSOProblemSolver()
        solver.solve(problem, LSOProblemSolver.hillClimbingGenerator(successor, value))
        print("Algorithm performance: ", solver.performance, ", memory usage: ", solver.resources)
        #self.assertTrue(solver.solved(problem))
        #print ("N queens, solution found using hill-climbing search: " + str(solver.solution[-1]))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
