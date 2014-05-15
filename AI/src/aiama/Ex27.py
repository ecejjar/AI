'''
Created on 30/11/2011

Code for Exercises 2.7 and 2.8 from AI: A Modern Approach

@author: ecejjar
'''

from functools import reduce    # Only for Python 3

class Environment(object):
    '''
    An environment simulator for the Vacuum Cleaner agent (see Exercise 2.7).
    Works with convex shapes only.
    '''
    
    @staticmethod
    def makeRect ( width, height ):
        '''
        Returns a list of 2-element tuples, each tuple representing a point
         in the cartesian space of integer numbers, all such points building
         a rectangle of size width*height which lower-left corner lies at
         point (0,0).
        '''
        assert type(width) is int, "Wrong type(%s) for width parameter" % type(width)
        assert type(height) is int, "Wrong type(%s) for height parameter" % type(width)
        if width > 0 and height > 0:
            shape = list(zip([0]*(width+2), range(width+2)))            # bottom
            shape += zip(range(1, height+2), [width+1]*(height+1))      # right
            shape += zip([height+1]*(width+2), range(width+1, 0, -1))   # top
            shape += zip(range(height+1, 0, -1), [0]*(height+2))        # left
            return shape
        else:
            raise Exception('This environment does not support empty areas')

    @staticmethod
    def row ( square ):
        'Returns the first element in list square'
        assert \
            type(square) is tuple or type(square) is list, \
            "Wrong type (%s) for square parameter" % type(square)
        return square[0]
                
    @staticmethod
    def col ( square ):
        'Returns the second element in list square'
        assert \
            type(square) is tuple or type(square) is list, \
            "Wrong type (%s) for square parameter" % type(square)
        return square[1]
                
    def __init__ ( self, shape ):
        self.__shape = shape
        self.__area = self.area # Cache the area 
        self.clean()
        self.reset()
        
    def getShape ( self ):
        return self.__shape
    shape = property(getShape)

    def getTime ( self ):
        return self.__time
    time = property(getTime)

    def getPerformance ( self ):
        if self.__time == 0:
            raise Exception("Time has not started yet - you need to tick() first!!")
        
        return self.__dirthistory / self.__time
    performance = property(getPerformance)
        
    def getArea ( self ):
        def findOpposite ( square, dir=0 ):
            assert dir >= 0 and dir <=1, "Wrong dir parameter, dir must be either 0 or 1"
            
            # if the square has no neighboring inner points opposite is itself
            # (it's either a vertex or part of a line)
            if not (self.isIn((square[0]-dir, square[1]-(1-dir))) or
                    self.isIn((square[0]+dir, square[1]+(1-dir)))):
                return square
             
            # find all squares in the same row (dir=0) / column (dir=1)
            # Notice that the resulting list includes the square itself
            candidates = \
                [bordersquare for bordersquare in self.__shape if bordersquare[dir] == square[dir]]

            # use the obtained list for checking validity of square parameter 
            if not candidates:
                raise Exception('Square (%i,%i) lies outside environment' % square)
            else:
                if len(candidates) > 2:
                    # more than 2 candidates; we're dealing with a concave area or an off-border point
                    if self.isIn(square): 
                        raise Exception('This environment only supports convex areas')
                    else:
                        raise Exception('Square (%i,%i) lies outside environment' % square)

            # place the square in reference to the candidate squares
            candidates.sort(key=lambda t: t[1-dir])
                
            i = candidates.index(square)
            assert(i >= 0 and i < len(candidates))
            return candidates[len(candidates)-1-i]
            
        def distanceToOpposite ( square, dir=0 ):
            d = square[1-dir] - findOpposite(square, dir)[1-dir] - 1
            
            # Discard negative values since each of those has a positive counterpart
            return (d > 0 and d) or 0
            
        return reduce(lambda x,y: x+y, map(distanceToOpposite, self.__shape))
    area = property(getArea) 
    
    def isIn ( self, square ):
        'Tells whether a square is within the environment\'s bounds'
        
        rowends = sorted([bordersq[1] for bordersq in self.__shape if bordersq[0] == square[0]])
        colends = sorted([bordersq[0] for bordersq in self.__shape if bordersq[1] == square[1]])
        if len(rowends) < 2 or len(colends) < 2:
            return False
        else:
            return (colends[0] < square[0] and square[0] < colends[1]) \
                   and (rowends[0] < square[1] and square[1] < rowends[1])

    def dirtness ( self, square=None ):
        '''
        Returns the amount of dirt in a square (0 means square clean)
         or in the whole environment (when square argument is None);
        If the square lies outside bounds it returns None.
        '''
        
        if square:
            if self.isIn(square):
                try:
                    return self.__dirt[square]
                except KeyError:
                    return 0
            else:
                return None
        else:
            return reduce(lambda x,y:x+y, self.__dirt.values(), 0)
    
    def dirt ( self, square, amount=1 ):
        'Sets the amount of dirt in a square to amount'
        if square and self.isIn(square):
            try:
                self.__dirt[square] += amount
            except:
                self.__dirt[square] = amount

    def clean ( self, square=None ):
        '''
        Removes all dirt from a square, or from the whole environment
         (when square argument is None).
        '''
        if square and self.isIn(square):
            del self.__dirt[square]
        else:
            self.__dirt = {}

    def isClean ( self ):
        return len(self.__dirt) == 0
    
    def tick ( self ):
        'Advances time by one unit'
        self.__time += 1
        self.__dirthistory += (self.__area - self.dirtness()) 
        
    def reset ( self ):
        'Resets time to instant 0'
        self.__time = 0
        self.__dirthistory = 0

    def registerAgent ( self, agent ):
        if agent.environment != self:
            raise Exception("Environment cannot register agent placed at another environment")
        if not self.isIn(agent.location):
            raise Exception("Environment cannot register agent placed off limits")
        self.__agent = agent
    
    def getAgent ( self ):
        return self.__agent
    agent = property(getAgent)


class Device(object):
    'A prototypical device'
    
    def __init__ ( self, name=None ):
        self.__name = name
        self.unplug()
        
    def plug ( self, agent ):
        assert agent is not None, "Attempt to plug device to None"
        self.__agent = agent
    
    def unplug ( self ):
        self.__agent = None
        
    def isPlugged ( self ):
        return self.__agent is not None
    
    def getName ( self ):
        return self.__name
    name = property(getName)
    
    def getAgent ( self ):
        return self.__agent
    agent = property(getAgent)

    
class Sensor(Device):
    'A prototypical sensor'
    
    def __init__ ( self, name=None ):
        super(Sensor, self).__init__(name)
        
    def plug ( self, agent ):
        assert self.name, "Cannot plug unnamed device to agent"
        super(Sensor, self).plug(agent)
        agent.sensors[self.name] = self
        
    def unplug ( self ):
        super(Sensor, self).unplug()
        if self.isPlugged(): del self.agent.sensors[self.name]
        
    def sense ( self ):
        raise NotImplemented("Sensor.sense()")

class DirtSensor(Sensor):
    def __init__ ( self, name=None ):
        super(DirtSensor, self).__init__(name)
    
    def sense ( self ):
        if self.isPlugged() and self.agent.isPlaced():
            return self.agent.environment.dirtness(self.agent.location)
        else:
            return None

             
class Actuator(Device):
    'A prototypical actuator class'
    
    def __init__ ( self, name=None ):
        super(Actuator, self).__init__(name)
        
    def plug ( self, agent ):
        super(Actuator, self).plug(agent)
        agent.actuators[self.name] = self
        
    def unplug ( self ):
        super(Actuator, self).unplug()
        if self.isPlugged(): del self.agent.actuators[self.name]
        
    def act ( self, *args ):
        raise NotImplemented("Actuator.act()")
        
class VacuumActuator(Actuator):
    def __init__ ( self, name=None ):
        super(VacuumActuator, self).__init__(name)
        
    def act ( self, *args ):
        if self.isPlugged() and self.agent.isPlaced():
            self.agent.environment.clean(self.agent.location)


class Agent(object):
    'A prototypical agent class'
    
    def __init__ ( self, name=None ):
        self.__name = name
        self.sensors = {}
        self.actuators = {}
        self.__direction = 1
        self.remove()
        
    def plug ( self, device ):
        device.plug(self)
    
    def place ( self, env, loc ):
        assert(env and loc, "Agent cannot be placed at " + str(env) + "(" + str(loc) + ")")
        self.__env = env
        self.__loc = loc
        try:
            env.registerAgent(self)
        except:
            self.remove()
            raise
            
    def remove ( self ):
        self.__env = None
        self.__loc = None
        
    def isPlaced ( self ):
        return self.__env and self.__loc
    
    def getName(self):
        return self.__name
    name = property(getName)
    
    def getEnv(self):
        if self.isPlaced(): return self.__env
        else: return None
    environment = property(getEnv)
    
    def getLoc(self):
        if self.isPlaced(): return self.__loc
        else: return None        
    location = property(getLoc)
        
    def move ( self ):
        if self.isPlaced():
            nextSquare = \
                (Environment.row(self.location),
                 Environment.col(self.location) + self.__direction)
            if self.environment.isIn(nextSquare):
                self.__loc = nextSquare
            else:
                self.__direction = -self.__direction
                if self.__direction > 0:
                    nextSquare = \
                        (Environment.row(self.location) + 1,
                         Environment.col(self.location))
                    if self.environment.isIn(nextSquare):
                        self.__loc = nextSquare
                    else:
                        self.move()
                else:
                    self.move()
        else:
            raise Exception("Agent is not placed, it can't move")
            
    def sense ( self, name=None ):
        if name is None:
            v = reduce(lambda x,y: x+y, map(lambda x:x.sense(), self.sensors.values()), 0)
            return v
        else:
            return self.sensors[name].sense()
        
    def act ( self, name=None, *args ):
        if name is None:
            for a in self.actuators.values(): a.act(args)
        else:
            self.actuators[name].act(args)

    def function ( self, *args ):
        raise NotImplemented("This is an abstract agent with no behavior")


class CleaningAgent(Agent):
    'An specialization of the basic agent that has a dirt sensor and a vacuum actuator'
    
    def __init__ ( self, name=None ):
        super(CleaningAgent, self).__init__(name)
        self.plug(DirtSensor('sensor'))
        self.plug(VacuumActuator('actuator'))
        

class ReflexCleaningAgent(CleaningAgent):
    def __init__ ( self, name=None ):
        super(ReflexCleaningAgent, self).__init__(name)
    
    def function ( self, *args ):
        dirt = self.sense()
        if dirt: self.act()
        else: self.move()



        