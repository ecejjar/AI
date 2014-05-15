'''
Created on 21/12/2011

@author: ecejjar
'''
import unittest
from Ex27 import ReflexCleaningAgent
from Ex29 import PenalizingEnvironment, ReflexCleaningAgentWithState

class PenalizingEnvironmentTest(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testPerf(self):
        agent = ReflexCleaningAgent('test')
        env = PenalizingEnvironment(PenalizingEnvironment.makeRect(4,4))
        
        env.reset()
        agent.place(env, (1,1))
        while env.time < 4: env.tick()
        self.assertEquals(
            env.getPerformance(), env.area,  # agent hasn't moved
            "Environment reports performance %r for dirt(t) = 0" % env.performance)
                
        env.reset()
        agent.place(env, (1,1))
        while env.time < 4:
            agent.function()
            env.tick()
        self.assertEquals(
            env.getPerformance(), env.area - env.time,  # since env is clean, agent moves once per tick
            "Environment reports performance %r for dirt(t) = 0 at t = %d" % (env.performance, env.time))
        
        env.reset()
        agent.place(env, (1,1))
        while env.time < 16:
            agent.function()
            env.tick()
        self.assertEquals(
            env.getPerformance(), env.area - env.time,
            "Environment reports performance %r for dirt(t) = 0 at t = %d" % (env.performance, env.time))

        env.reset()
        agent.place(env, (1,1))
        while env.time < 20:
            agent.function()
            env.tick()
        self.assertEquals(
            env.getPerformance(), env.area - env.time,
            "Environment reports performance %r for dirt(t) = 0 at t = %d" % (env.performance, env.time))
        
        agent = ReflexCleaningAgentWithState('test')
        env.reset()
        agent.place(env, (1,1))
        while env.time < 100:
            agent.function()
            env.tick()
        self.assertGreater(
            env.performance, env.area - env.time,
            "Environment reports performance %r for dirt(t) = 0 at t = %d" % (env.performance, env.time))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()