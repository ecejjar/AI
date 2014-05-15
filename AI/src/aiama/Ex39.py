'''
Created on 09/02/2012

Code for Exercise 3.9 from AI: A Modern Approach

@author: ecejjar
'''

import sys
import heapq                    # needed for A* and its variants
import logging

logger = logging.getLogger("Ex39")
logger.setLevel(logging.DEBUG)
#logging.debug("kk")

class Problem(object):
    '''
    Model of a problem following the problem formulation theory of chapter 3
    '''
            
    def __init__ ( self, initial, goal, successor, cost ):
        '''
        Constructor
        '''
        self.__goal = (callable(goal) and goal) or (lambda g: g == goal) 
        self.__successor = successor
        self.__cost = cost
        self.__initial = initial
        
    def getInitial ( self ):
        return self.__initial
    initial = property(getInitial)

    def getGoal ( self ):
        return self.__goal
    goal = property(getGoal)

    def getSuccessor ( self ):
        return self.__successor
    successor = property(getSuccessor)

    def getCost ( self ):
        return self.__cost
    cost = property(getCost)


class ProblemSolver(object):
    '''
    A generic problem solver
    '''
    
    class Node(tuple):
        '''
        A simple tuple wrapper to make the algorithm implementations easier to understand
        '''
        cost = lambda n: n[0]
        item = lambda n: n[1]
        parent = lambda n: n[2]
        isInitial = lambda n: n.parent() is None            
    
    def __init__ ( self, noderepr = None ):
        '''
        Constructor
        '''
        self.__solution = None
        self.__performance = None
        self.__memusage = 0
        self.__noderepr = noderepr or repr
        
    def getPerformance ( self ):
        return self.__performance
    def setPerformance ( self, value ):
        self.__performance = value
    performance = property(getPerformance, setPerformance)
    
    def getResources ( self ):
        return self.__memusage
    def setResources ( self, value ):
        self.__memusage = value
    resources = property(getResources, setResources)
    
    def getSolution ( self ):
        return self.__solution
    def setSolution ( self, value ):
        self.__solution = value
    solution = property(getSolution, setSolution)
    
    def noderepr ( self, node ):
        return self.__noderepr(node)
    
    def solved ( self, problem ):
        return self.__solution and problem.goal(self.__solution[-1])
    
    def solve ( self, problem, gen, chk_dups = False ):
        self.treeSearch(problem, gen, chk_dups)
        
    def graphSearch ( self, problem, gen ):
        return self.treeSearch(problem, gen, True)
    
    def treeSearch ( self, problem, gen, chk_dups = False ):
        self.__performance = 0
        self.__memusage = 0
        visited = None
        h = None
        if chk_dups:
            visited = set()
            h = lambda n: n.item() not in visited
        while True:
            if chk_dups: visited.clear()
            fringe = [ProblemSolver.Node((sys.maxsize, problem.initial, None))]
            sol = self.__recurse(fringe, problem, gen, visited, h)
            if sol is None: break   # sol is None, meaning search tree exhausted
            if any(sol):
                self.__solution = [n.item() for n in sol if n]
                break
            logger.debug("Play it again, Sam!")
                        
    def __recurse ( self, fringe, problem, gen, visited, h ):
        for n in filter(h, fringe):
            logger.debug("Checking:\n" + self.noderepr(n))
            self.__performance += 1
            self.__memusage += sys.getsizeof(n, 0)
            if problem.goal(n.item()):
                logger.debug("********* GOAL! ***********")
                return [n]                                # the base case            

        limitReached = False
        logger.debug("Expanding fringe:")
        for desc in gen(filter(h, fringe)):
            if any(desc):
                logger.debug("descendants: " + str(desc))
                logger.debug("--------recursing----------")

                try:
                    visited.update(map(lambda n: ProblemSolver.Node.item(ProblemSolver.Node.parent(n)), desc))
                except AttributeError:           # 'NoneType' has no attribute 'update' (visited is undefined)
                    pass                         # user doesn't want us to check for dups
    
                sol = self.__recurse(desc, problem, gen, visited, h)   # the recursive case
                if sol is not None:
                    if any(sol):
                        if not sol[0].isInitial(): sol.insert(0, sol[0].parent())
                        return sol
                    else:
                        limitReached = True # the recursive case
            else:
                limitReached = True         # the base case
            
        logger.debug("EOT, tracing back")
        if limitReached: return []

    @staticmethod
    def depthFirstGenerator ( successor ):
        def nestedGenerator ( fringe ):
            for n in fringe:
                descendants = successor(n.item()) or []
                for desc in descendants:
                    yield [ProblemSolver.Node((0, desc, n))]
        return nestedGenerator
        
    @staticmethod
    def breadthFirstGenerator ( successor ):
        def nestedGenerator ( fringe ):
            new_fringe = []
            for n in fringe:
                descendants = successor(n.item()) or []
                for desc in descendants:
                    new_fringe.append(ProblemSolver.Node((0, desc, n)))
            yield new_fringe
        return nestedGenerator
            
    @staticmethod
    def depthLimitedGenerator ( successor, max_level ):
        var = { "level": 0 }
        def nestedGenerator ( fringe ):
            if var["level"] == max_level - 1: return
            var["level"] = var["level"] + 1
            for n in fringe:
                descendants = successor(n.item()) or []
                for desc in descendants:
                    yield [ProblemSolver.Node((0, desc, n))]
            var["level"] = var["level"] - 1
        return nestedGenerator
        
    @staticmethod
    def iterativeDeepeningGenerator ( successor ):
        var = { "max_level": 0, "level": 0 }
        def nestedGenerator ( fringe ):
            var["level"] = var["level"] + 1
            for n in fringe:
                if n.isInitial():
                    var["level"] = 1
                    var["max_level"] = var["max_level"] + 1                        
                if var["level"] == var["max_level"]:
                    logger.debug("Limit reached!")
                    yield []    # yielding an empty sequence means limit reached
                else:
                    descendants = successor(n.item()) or []
                    for desc in descendants:
                        #print(str(var))
                        #print("Yielding " + str(desc))
                        yield [ProblemSolver.Node((0, desc, n))]
            var["level"] = var["level"] - 1
        return nestedGenerator

    @staticmethod
    def bidirectionalSearchGenerator ( goal ):
        def nestedGenerator ( fringe ):
            yield fringe

    @staticmethod
    def greedyBestFirstGenerator ( successor, h ):
        heuristicSuccessor = lambda n: sorted(successor(n), key=h)
        return ProblemSolver.breadthFirstGenerator(heuristicSuccessor)    

    
class CostBasedProblemSolver(ProblemSolver):
    '''
    A problem solver using cost-based search algorithms
    '''
    
    def __init__ ( self, noderepr = None ):
        '''
        Constructor
        '''
        super(CostBasedProblemSolver, self).__init__(noderepr)
        
        
    def treeSearch ( self, problem, gen, chk_dups = False ):
        self.performance = 0
        self.memusage = 0
        visited = set()
        h = lambda n: fringe[0] == n and n.item() not in visited
        while True:
            visited.clear()
            fringe = [CostBasedProblemSolver.Node((0, problem.initial, None))]
            sol = self.__recurse(fringe, problem, gen, visited, h)
            if sol is None: break   # sol is None, meaning search tree exhausted
            if any(sol):
                self.solution = [n.item() for n in sol if n]
                break
            logger.debug("Play it again, Sam!")
                        
    def __recurse ( self, fringe, problem, gen, visited, h ):
        for n in filter(h, fringe):
            logger.debug("Checking " + self.noderepr(n))
            self.performance += 1
            self.memusage += sys.getsizeof(n, 0)
            if problem.goal(n.item()):
                logger.debug("********* GOAL! ***********")
                return [n]                    # the base case
                
        limitReached = False
        logger.debug("Expanding fringe:")
        for desc in gen(fringe):
            if any(desc):
                logger.debug("descendants: " + str(desc))
                logger.debug("--------recursing----------")
                
                try:
                    visited.update(map(lambda n: CostBasedProblemSolver.Node.item(CostBasedProblemSolver.Node.parent(n)), desc))
                except AttributeError:           # 'NoneType' has no attribute 'visited'
                    pass                         # visited is undefined so user doesn't want us to check for dups

                sol = self.__recurse(desc, problem, gen, visited, h)     # the recursive case
                if sol is not None:
                    if any(sol):
                        if not sol[0].isInitial(): sol.insert(0, sol[0].parent())
                    return sol
            else:
                limitReached = True

        logger.debug("EOT, tracing back")
        if limitReached: return []
                        
    @staticmethod
    def iterativeLengtheningGenerator ( successor, cost ):
        var = { "max_cost": 0, "new_max_cost": 0 }
        def nestedGenerator ( fringe ):
            best_node = heapq.heappop(fringe)
            if best_node.isInitial():
                var["max_cost"] = var["new_max_cost"]
                var["new_max_cost"] = 0
                
            max_cost = var["max_cost"]
            new_max_cost = var["new_max_cost"]
            descendants = successor(best_node.item()) or []            
            for desc in descendants:
                f = best_node.cost() + cost(desc, best_node.item())
                if f <= max_cost:
                    heapq.heappush(fringe, CostBasedProblemSolver.Node((f, desc, best_node)))
                else:
                    new_max_cost = min(f, new_max_cost or f)
            var["new_max_cost"] = new_max_cost
            yield fringe
        return nestedGenerator
                        
    @staticmethod
    def uniformCostGenerator ( successor, cost ):
        def nestedGenerator ( fringe ):
            best_node = heapq.heappop(fringe)
            descendants = successor(best_node.item()) or []
            for desc in descendants:
                f = best_node.cost() + cost(desc, best_node.item())
                heapq.heappush(fringe, CostBasedProblemSolver.Node((f, desc, best_node)))
            yield fringe
        return nestedGenerator
    
    @staticmethod
    def aStarGenerator ( successor, cost, h ):
        def nestedGenerator ( fringe ):
            best_node = heapq.heappop(fringe)
            descendants = successor(best_node.item()) or []
            for desc in descendants:
                g = best_node.cost() - h(best_node.item()) + cost(desc, best_node.item())
                f = g + h(desc)
                heapq.heappush(fringe, CostBasedProblemSolver.Node((f, desc, best_node)))
            yield fringe
        return nestedGenerator
