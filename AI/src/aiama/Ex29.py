'''
Created on 21/12/2011

Code for Exercise 2.9 from AI: A Modern Approach

@author: ecejjar
'''

from Ex27 import Environment, ReflexCleaningAgent

class PenalizingEnvironment(Environment):
    '''
    An environment that penalizes agent's performance if it moves
    '''

    def __init__( self, shape ):
        '''
        Constructor
        '''
        super(PenalizingEnvironment, self).__init__(shape)

    def getPerformance ( self ):
        return \
            super(PenalizingEnvironment, self).getPerformance() \
            - self.__penalty 
    
    def tick ( self ):
        if self.agent and self.agent.location != self.__lastPosition:
            self.__penalty += 1
            self.__lastPosition = self.agent.location
        return super(PenalizingEnvironment, self).tick()
         
    def reset ( self ):
        self.__penalty = 0
        self.__lastPosition = None
        return super(PenalizingEnvironment, self).reset()
    
    def registerAgent ( self, agent ):
        result = super(PenalizingEnvironment, self).registerAgent(agent)
        self.__lastPosition = self.agent.location
        return result


class ReflexCleaningAgentWithState(ReflexCleaningAgent):
    def __init__( self, name=None ):
        '''
        Constructor
        '''
        super(ReflexCleaningAgentWithState, self).__init__(name)
        self.reset()

    def reset ( self ):
        self.__visitedSquares = set()  # a set type would do better
        self.__area = 0
        
    def place ( self, env, loc ):
        result = super(ReflexCleaningAgentWithState, self).place(env, loc)
        self.__visitedSquares.add(self.location)
        self.__area = env.area  # cache area to speed up move()                
        return result
    
    def remove ( self ):
        self.reset()
        return super(ReflexCleaningAgentWithState, self).remove()
        
    def move ( self ):
        if len(self.__visitedSquares) < self.__area:
            result = super(ReflexCleaningAgentWithState, self).move()
            self.__visitedSquares.add(self.location)
            return result
