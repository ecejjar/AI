'''
Created on 15/02/2012

@author: ecejjar
'''

from math import sqrt
from random import choice
try:
    from functools import reduce    # Only for Python 3
except:
    pass
import sys

import unittest
from Ex39 import Problem, ProblemSolver, CostBasedProblemSolver
from random import random

class ProblemTest(unittest.TestCase):

    def testProblem(self):
        initial = 1
        successor = lambda x : (2*x, 2*x + 1)
        cost = lambda x, y : 1
        
        goal = 8    # goal must be on the leftmost branch of the tree!!
        problem = Problem(initial, goal, successor, cost)
        
        solver = ProblemSolver()
        solver.solve(problem, ProblemSolver.depthFirstGenerator(successor))
        self.assertTrue(solver.solved(problem))
        self.assertEqual(
            solver.solution, [1, 2, 4, 8],
            "Solution found using depth-first search is " + str(solver.solution))

        goal = 10
        problem = Problem(initial, goal, successor, cost)
        solver = ProblemSolver()
        solver.solve(problem, ProblemSolver.breadthFirstGenerator(successor))
        self.assertTrue(solver.solved(problem))
        self.assertEqual(
            solver.solution, [1, 2, 5, 10],
            "Solution found using breadth-first search is " + str(solver.solution))

        goal = 10
        problem = Problem(initial, goal, successor, cost)
        solver = ProblemSolver()
        solver.solve(problem, ProblemSolver.depthLimitedGenerator(successor, 4))
        self.assertTrue(solver.solved(problem))
        self.assertEqual(
            solver.solution, [1, 2, 5, 10],
            "Solution found using depth-limited search is " + str(solver.solution))

        goal = 10
        problem = Problem(initial, goal, successor, cost)
        solver = ProblemSolver()
        solver.solve(problem, ProblemSolver.iterativeDeepeningGenerator(successor))
        self.assertTrue(solver.solved(problem))
        self.assertEqual(
            solver.solution, [1, 2, 5, 10],
            "Solution found using IDDF search is " + str(solver.solution))

        goal = 10
        successor = \
            lambda x: (random() < 0.5 and (2*x, 2*x + 1)) \
            or (max(1, int(x/2)), 2*x, 2*x + 1)
        problem = Problem(initial, goal, successor, cost)
        solver = ProblemSolver()
        solver.solve(problem, ProblemSolver.breadthFirstGenerator(successor), True)
        self.assertTrue(solver.solved(problem))
        self.assertEqual(
            solver.solution, [1, 2, 5, 10],
            "Solution found using breadth-first *graph* search is " + str(solver.solution))

        goal = 32
        successor = \
            lambda x: (random() < 0.5 and (2*x, 2*x + 1)) \
            or (max(1, int(x/2)), 2*x, 2*x + 1)
        problem = Problem(initial, goal, successor, cost)
        solver = ProblemSolver()
        solver.solve(problem, ProblemSolver.iterativeDeepeningGenerator(successor), True)
        self.assertTrue(solver.solved(problem))
        self.assertEqual(
            solver.solution, [1, 2, 4, 8, 16, 32],
            "Solution found using IDDF *graph* search is " + str(solver.solution))

    def testMissionariesAndCannibals(self):
        initial = ((3,3), (0,0))
        goal = ((0,0), (3,3))
        cost = lambda x, y : 1
        def successor ( s ):
            mis = lambda b: b[0]
            can = lambda b: b[1]
            ouch = lambda a: mis(a) > 0 and can(a) > 0 and mis(a) != can(a)
            def trip(a, b, a_to_b):
                if mis(a_to_b) > mis(a) or can(a_to_b) > can(a):      # check physical limits
                    raise Exception("Not enough people!")
                nxt_a = (mis(a) - mis(a_to_b), can(a) - can(a_to_b))
                if ouch(nxt_a):                                          # discard fail a->b trips
                    raise Exception("Holocaust!")
                nxt_b = (mis(b) + mis(a_to_b), can(b) + can(a_to_b))
                return nxt_a, nxt_b
                    
            result = []
            a, b = s[0], s[1]
            boat_floats = ((0,0), (1,0), (2,0), (1,1), (0,1), (0,2))
            for a_to_b in boat_floats:
                try:
                    tmp_a, tmp_b = trip(a, b, a_to_b)
                except:
                    continue
                for b_to_a in filter(lambda b_to_a: b_to_a != a_to_b, boat_floats):
                    try:
                        nxt_b, nxt_a = trip(tmp_b, tmp_a, b_to_a)
                    except:
                        continue
                    if not ouch(nxt_a):                          # discard wrong b->a trips
                        result.append((nxt_a, nxt_b))
            return result
                
        problem = Problem(initial, goal, successor, cost)
        solver = ProblemSolver()
        solver.solve(problem, ProblemSolver.depthFirstGenerator(successor), True)
        self.assertTrue(solver.solved(problem))
        
        print("M&C, solution found using depth-first search: " + str(solver.solution))
        print("Algorithm performance: ", solver.performance, ", memory used: ", solver.resources)
        
    def testQueens ( self, n = 8 ):
        initial = ()
        cost = lambda x, y : 1
        def goal ( board ):
            return len(board) == n
        def successor ( board ):
            def attacks ( q1, q2 ):
                return q1[0]==q2[0] or q1[1]==q2[1] or abs(q1[0]-q2[0]) == abs(q1[1]-q2[1])
            
            result = []
            for col in range(len(board), n):
                for row in range(n):
                    new_queen = (row, col)
                    hostiles = [q for q in board if attacks(new_queen, q)]
                    if len(hostiles) == 0:
                        nxt_board = board + (new_queen,)
                        result.append(nxt_board)            
            return tuple(result)

        problem = Problem(initial, goal, successor, cost)
        solver = ProblemSolver()
        solver.solve(problem, ProblemSolver.depthFirstGenerator(successor), True)
        self.assertTrue(solver.solved(problem))
        
        print("N queens, solution found using depth-first search: " + str(solver.solution[-1]))
        print("Algorithm performance: ", solver.performance, ", memory used: ", solver.resources)

    def testNavigation ( self ):
        distance = {
            ("Oradea","Zerind"): 71,
            ("Oradea","Sibiu"): 151,
            ("Neamt","Iasi"): 87,
            ("Zerind","Arad"): 75,
            ("Iasi","Vaslui"): 92,
            ("Arad","Sibiu"): 140,
            ("Arad","Timisoara"): 118,
            ("Sibiu","Fagaras"): 99,
            ("Sibiu","Rimnicu Vilcea"): 80,
            ("Fagaras","Bucharest"): 1211, #211,
            ("Vaslui","Urziceni"): 142,
            ("Rimnicu Vilcea","Pitesti"): 97,
            ("Rimnicu Vilcea","Craiova"): 146,
            ("Timisoara","Lugoj"): 111,
            ("Lugoj","Mehadia"): 70,
            ("Pitesti","Bucharest"): 101,
            ("Pitesti","Craiova"): 138,
            ("Hirsova","Urziceni"): 98,
            ("Hirsova","Eforie"): 86,
            ("Urcizeni","Bucharest"): 85,
            ("Mehadia","Drobeta"): 75,
            ("Bucharest","Giurgiu"): 90,
            ("Drobeta","Craiova"): 120,
        }
        sld_bucharest = {
            "Arad": 366,
            "Bucharest": 0,
            "Craiova": 160,
            "Drobeta": 242,
            "Eforie": 161,
            "Fagaras": 1300, #176,
            "Giurgiu": 77,
            "Hirsova": 151,
            "Iasi": 226,
            "Lugoj": 244,
            "Mehadia": 241,
            "Neamt": 234,
            "Oradea": 380,
            "Pitesti": 100,
            "Rimnicu Vilcea": 193,
            "Sibiu": 253,
            "Timisoara": 329,
            "Urcizeni": 80,
            "Vaslui": 199,
            "Zerind": 374,
        }
        
        def repr ( node ):
            parent = ''
            if not node.isInitial(): parent = node.parent().item() + ' ->'
            return "%s %s (%d)" % (parent, node.item(), node.cost())
        
        initial = "Arad"
        goal = "Bucharest"
        cost = lambda s, n: distance.get((s,n), distance.get((n,s))) or (s==n and 0)
        successor = lambda n: [p[1-i] for p in distance for i in (0,1) if p[i] == n]
        h = lambda n: sld_bucharest[n]            
        problem = Problem(initial, goal, successor, cost)
        
        solver = ProblemSolver(repr)
        solver.solve(problem, ProblemSolver.iterativeDeepeningGenerator(successor), True)
        self.assertTrue(solver.solved(problem))
        print ("Navigation: solution found using ID search: " + str(solver.solution))
        print("Algorithm performance: ", solver.performance, ", memory used: ", solver.resources)

        solver = ProblemSolver(repr)
        solver.solve(problem, CostBasedProblemSolver.greedyBestFirstGenerator(successor, h), True)
        self.assertTrue(solver.solved(problem))
        print ("Navigation: solution found using greedy-best-first search: " + str(solver.solution))
        print("Algorithm performance: ", solver.performance, ", memory used: ", solver.resources)
    
        solver = CostBasedProblemSolver(repr)
        solver.solve(problem, CostBasedProblemSolver.uniformCostGenerator(successor, cost))
        self.assertTrue(solver.solved(problem))
        print ("Navigation: solution found using uniform-cost search: " + str(solver.solution))
        print("Algorithm performance: ", solver.performance, ", memory used: ", solver.resources)
    
        solver = CostBasedProblemSolver(repr)
        solver.solve(problem, CostBasedProblemSolver.aStarGenerator(successor, cost, h))
        self.assertTrue(solver.solved(problem))
        print ("Navigation: solution found using A*: " + str(solver.solution))
        print("Algorithm performance: ", solver.performance, ", memory used: ", solver.resources)
    
        
    # testNpuzzle is not deterministic, it contains a random factor in the initial disposition
    # of the puzzle; resolution time varies and half the times it cannot be solved, since in
    # any N-puzzle problem only half of the possible states can be reached from a given initial state
    def testNpuzzle ( self, size = 8 ):
        side = int(sqrt(size+1))
        size = side*side-1
        row = lambda n: n[0]
        col = lambda n: n[1]
        
        def repr ( node ):
            puzzle = node.item()
            side = int(sqrt(len(puzzle)))
            lines = [[None]*side]*side
            for i, p in enumerate(puzzle):
                lines[p[0]][p[1]] = str(i)
            return "%s (%d)" % ('\n'.join([''.join(r) for r in lines]), node.cost()) 
                
        def successor ( n ):
            hole = n[0]
            adj = (range(row(hole)-1, row(hole)+2), range(col(hole)-1, col(hole)+2))
            result = []
            for i in range(1, size+1):
                for c in (0, 1):
                    if n[i][c] == hole[c] and n[i][1-c] in adj[1-c]:
                        nxt = list(n)
                        nxt[0], nxt[i] = nxt[i], nxt[0]
                        result.append(tuple(nxt))
            return result
        
        def successorInPlace ( n ):
            hole = n[0]
            adj = (range(row(hole)-1, row(hole)+2), range(col(hole)-1, col(hole)+2))
            for i in range(1, size+1):
                for c in (0, 1):
                    if n[i][c] == hole[c] and n[i][1-c] in adj[1-c]:
                        nl = list(n)
                        nl[0], nl[i] = nl[i], nl[0]
                        yield tuple(nl)

        goal = tuple([(r,c) for r in range(side) for c in range(side)])
        initial = tuple(goal)
        for n in range(6): initial = choice(successor(initial)) # more than 6 implies IDS would take more than 1K recursions
        cost = lambda s,n: 1
            
        #sys.setrecursionlimit(2000)
        
        problem = Problem(initial, goal, successor, cost)        
        solver = ProblemSolver(repr)
        solver.solve(problem, ProblemSolver.iterativeDeepeningGenerator(successor), True)
        self.assertTrue(solver.solved(problem))
        print ("N-puzzle, solution found using IDDF search: " + str(solver.solution))
        print("Algorithm performance: ", solver.performance, ", memory used: ", solver.resources)

        solver = CostBasedProblemSolver(repr)
        #solver.solve(problem, CostBasedProblemSolver.iterativeLengtheningGenerator(successor, cost), True)
        #self.assertTrue(solver.solved(problem))
        #print ("N-puzzle, solution found using iterative lengthening search: " + str(solver.solution))
        #print("Algorithm performance: ", solver.performance, ", memory used: ", solver.resources)

        manhattanDistance = lambda s: abs(row(s[1])-row(s[0])) + abs(col(s[1])-col(s[0]))
        h = lambda n: reduce(lambda x,y: x+y, map(manhattanDistance, zip(n,goal)))
        solver = CostBasedProblemSolver(repr)
        solver.solve(problem, CostBasedProblemSolver.aStarGenerator(successor, cost, h), True)
        self.assertTrue(solver.solved(problem))
        print ("N-puzzle, solution found using A* search: " + str(solver.solution))
        print("Algorithm performance: ", solver.performance, ", memory used: ", solver.resources)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
