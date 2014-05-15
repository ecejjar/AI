'''
Created on 07/12/2011

@author: ecejjar
'''
import unittest
from Ex27 import *

class EnvironmentTest(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testRect(self):
        env = Environment(Environment.makeRect(2,1))
        self.assertEquals(env.dirtness(), 0, "New environment reports dirt (%i)" % env.dirtness())
        self.assertTrue(env.isIn((1,1)), "Environment reports square (1,1) being out")
        self.assertTrue(env.isIn((1,2)), "Environment reports square (1,2) being out")
        self.assertFalse(env.isIn((0,0)), "Environment reports square (0,0) being in")
        self.assertFalse(env.isIn((0,2)), "Environment reports square (0,2) being in")
        self.assertFalse(env.isIn((2,0)), "Environment reports square (2,0) being in")
        self.assertFalse(env.isIn((2,2)), "Environment reports square (2,2) being in")
        self.assertFalse(env.isIn((-1,-1)), "Environment reports square (-1,-1) being in")
        self.assertFalse(env.isIn((3,3)), "Environment reports square (3,3) being in")
        env.dirt((0,0))
        self.assert_(env.dirtness() == 0, "Environment allowed off dirtness")
        env.dirt((1,1))
        self.assert_(
            env.dirtness() == 1,
            "Environment reports different dirtness (%i) than expected (1)" % env.dirtness())
        env.dirt((1,2), 5)
        self.assert_(
            env.dirtness() == 6,
            "Environment reports different dirtness (%i) than expected (6)" % env.dirtness())
        env.clean((1,1))
        self.assert_(
            env.dirtness() == 5,
            "Environment reports different dirtness (%i) than expected (5)" % env.dirtness())
        env.clean()
        self.assert_(
            env.dirtness() == 0,
            "Just cleaned environment reports dirt (%i)" % env.dirtness())
        env.dirt((0,0))
        self.assert_(
            env.dirtness((0,0)) is None,
            "Environment reports a dirtness amount for off-square (0,0)")
        env.dirt((1,1))
        self.assert_(
            env.dirtness((1,1)) == 1,
            "Environment reports different dirtness (%i) than expected (1) for square (1,1)")

    def testGeom(self):
        env = Environment(Environment.makeRect(4,4))
        self.assertEquals(env.area, 4*4, "Environment reports wrong area size (%i)" % env.area)

    def testPerf(self):
        env = Environment(Environment.makeRect(2,2))
        for i in range(4): env.tick()
        self.assertEquals(
            env.performance, env.area,
            "Environment reports performance %r for dirt(t) = 0" % env.performance)

        env.reset()
        for i in range(4+1): env.tick() or env.dirt((i//2+1,i%2+1))
        self.assertEquals(
            env.performance, env.area/2,
            "Environment reports performance %r for dirt(t) = t" % env.performance)

        
class DeviceTest(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testDevice(self):
        d = Device()
        self.assert_(not d.isPlugged(), "OOTB nameless device reports plugged")
        self.assert_(not d.name, "OOTB nameless device reports having a name")
        self.assert_(not d.agent, "OOTB nameless device reports having an agent")
        
        d = Device('test')
        self.assert_(not d.isPlugged(), "OOTB device reports plugged")
        self.assert_(d.name == 'test', "OOTB device reports having a name distinct from 'test'")
        self.assert_(not d.agent, "OOTB device reports having an agent")

        a = Agent()
        d.plug(a)
        self.assert_(d.isPlugged(), "Plugged device reports not plugged")
        self.assert_(d.name == 'test', "Plugged device reports having a name distinct from 'test'")
        self.assert_(d.agent, "Plugged device reports not having an agent")
        d.unplug()
        self.assert_(not d.isPlugged(), "Unplugged device reports plugged")
        self.assert_(d.name == 'test', "Unplugged device reports having a name distinct from 'test'")
        self.assert_(not d.agent, "Unplugged device reports having an agent")

        
class SensorsTest(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testSensor(self):
        # re-test Device functionality just in case Sensor overloads something
        s = Sensor()
        self.assertFalse(s.isPlugged(), "OOTB nameless sensor reports plugged")
        self.assertFalse(s.name, "OOTB nameless sensor reports having a name")
        self.assertFalse(s.agent, "OOTB nameless sensor reports having an agent")
        
        s = Sensor('test')
        self.assertFalse(s.isPlugged(), "OOTB sensor reports plugged")
        self.assertEquals(s.name, 'test', "OOTB sensor reports having a name distinct from 'test'")
        self.assertFalse(s.agent, "OOTB sensor reports having an agent")

        a = Agent()
        s.plug(a)
        self.assert_(s.isPlugged(), "Plugged sensor reports not plugged")
        self.assert_(s.name == 'test', "Plugged sensor reports having a name distinct from 'test'")
        self.assert_(s.agent, "Plugged sensor reports not having an agent")
        self.assertEqual(a.sensors['test'], s, "Agent reports sensor 'test' not plugged")
        s.unplug()
        self.assert_(not s.isPlugged(), "Unplugged sensor reports plugged")
        self.assert_(s.name == 'test', "Unplugged sensor reports having a name distinct from 'test'")
        self.assert_(not s.agent, "Unplugged sensor reports having an agent")
        self.assertRaises(Exception, a.sensors['test'], "Agent reports sensor 'test' still plugged")
        self.assertRaises(Exception, Sensor.sense, s)
        
        s = DirtSensor('test')
        self.assertTrue(s.sense() is None, "Unplugged DirtSensor reports dirt")
        s.plug(a)   # == a.plug(s), but we're not testing Agent here
        self.assertTrue(s.sense() is None, "DirtSensor on unplaced agent reports dirt")
        env = Environment(Environment.makeRect(2,1))
        env.dirt((1,1))
        a.place(env, (1,1))
        self.assertTrue(
            s.sense() == 1,
            "DirtSensor on placed agent reports less dirt (%i) than expected (1)" % s.sense())
        

class ActuatorsTest(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testActuator(self):
        # re-test Device functionality just in case Sensor overloads something
        a = Actuator()
        self.assertFalse(a.isPlugged(), "OOTB nameless actuator reports plugged")
        self.assertFalse(a.name, "OOTB nameless actuator reports having a name")
        self.assertFalse(a.agent, "OOTB nameless actuator reports having an agent")
        
        a = Actuator('test')
        self.assertTrue(not a.isPlugged(), "OOTB actuator reports plugged")
        self.assertEquals(a.name, 'test', "OOTB actuator reports having a name distinct from 'test'")
        self.assertFalse(a.agent, "OOTB sensor reports having an agent")

        ag = Agent()
        a.plug(ag)  # == ag.plug(a), but we're not testing agents here
        self.assertTrue(a.isPlugged(), "Plugged actuator reports not plugged")
        self.assertEquals(a.name, 'test', "Plugged actuator reports having a name distinct from 'test'")
        self.assertTrue(a.agent, "Plugged actuator reports not having an agent")
        self.assertEquals(ag.actuators['test'], a, "Agent reports actuator 'test' not plugged")
        a.unplug()
        self.assertFalse(a.isPlugged(), "Unplugged actuator reports plugged")
        self.assertEquals(a.name, 'test', "Unplugged actuator reports having a name distinct from 'test'")
        self.assertFalse(a.agent, "Unplugged actuator reports having an agent")
        self.assertRaises(Exception, ag.actuators['test'], "Agent reports actuator 'test' still plugged")
        self.assertRaises(Exception, Actuator.act, a)

        a = VacuumActuator('test')
        self.assertFalse(a.act(), "Unplugged VacuumActuator reports something from act()")
        a.plug(ag)   # == ag.plug(a), but we're not testing Agent here
        self.assertFalse(a.act(), "VacuumActuator on unplaced agent reports something from act()")
        env = Environment(Environment.makeRect(2,1))
        env.dirt((1,1))
        ag.place(env, (1,1))
        a.act()
        self.assertTrue(
            env.dirtness() == 0,
            "VaccumActuator didn't clean square (1,1)")

class AgentsTest(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testAgent(self):
        a = Agent()
        self.assertFalse(a.name, "OOTB nameless agent reports having a name")
        self.assertFalse(a.environment, "OOTB nameless agent reports being in an environment")
        self.assertFalse(a.location, "OOTB nameless agent reports being located somewhere")
        
        env = Environment(Environment.makeRect(2,2))
        a.place(env, (1,1))
        self.assertEquals(a.environment, env, "Placed nameless agent reports wrong environment")
        self.assertEquals(a.location, (1,1), "Placed nameless agent reports wrong location")
        a.remove()
        self.assertFalse(a.environment, "Removed nameless agent reports being in an environment")
        self.assertFalse(a.location, "Removed nameless agent reports being located somewhere")
        self.assertRaises(Exception, Agent.place, a, env, (0,0))
        self.assertFalse(a.environment, "Misplaced nameless agent reports being in an environment")
        self.assertFalse(a.location, "Misplaced nameless agent reports being located somewhere")


class SystemTest(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testReflexAgent(self):
        env = Environment(Environment.makeRect(2, 1))
        agent = ReflexCleaningAgent('test')

        # First case has perfect performance
        for initialSquare in ((1,1), (1,2)):
            env.clean() or env.reset()
            agent.place(env, initialSquare)
            while True:
                agent.function()
                env.tick()
                if env.isClean(): break
            p1 = env.performance
            print("Performance for first case is %r" % p1)
                    
            # Second test: leftmost square dirty
            env.clean() or env.reset()
            agent.place(env, initialSquare)
            env.dirt((1,1))
            while True:
                agent.function()
                env.tick()
                if env.isClean(): break
            p2 = env.performance
            print("Performance for second case is %r" % p2)
            
            # Third test: rightmost square dirty
            env.clean() or env.reset()
            agent.place(env, initialSquare)
            env.dirt((1,2))
            while True:
                agent.function()
                env.tick()
                if env.isClean(): break
            p3 = env.performance
            print("Performance for third case is %r" % p3)
            
            # Fourth test: both squares dirty
            env.clean() or env.reset()
            agent.place(env, initialSquare)
            env.dirt((1,1)) or env.dirt((1,2))
            while True:
                agent.function()
                env.tick()
                if env.isClean(): break
            p4 = env.performance
            print("Performance for fourth case is %r" % p4)
        
            print("Average performance is %r" % ((p1 + p2 + p3 + p4)/4))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()