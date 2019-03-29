'''Test of restartable AMS

'''
from core.agent import Agent
from core.message import Belief, Essence, Resource
from core.instructor import Interpreter
from core.scaffold_map import ResourceMap, MapCollection
from core.agent_ms import AgentManagementSystem

import networkx as nx

class Env(object):

    def __init__(self, env_1, env_2):

        self.env_1 = env_1
        self.env_2 = env_2

class Bacteria(Agent):

    def belief_adj(self, b1_inp, b2_inp):

        b1_out = b1_inp + 0.1
        b2_out = b2_out * (-1)

        r1_shift = -1.0 * self.essence['E1']
        r2_shift = -1.0 * self.essence['E2']

        return b1_out, b2_out, r1_shift, r2_shift

    def __init__(self, name, e1, e2, r1, r2, b1, b2):

        super().__init__(name, True)

        essence = Essence('Bacteria Essence', ['E1', 'E2'])
        essence.set_values([e1, e2])
        
        resource = Resource('Bacteria Resource', ['R1', 'R2'])
        resource.set_values([r1, r2])

        belief = Belief('Bacteria Belief', ['B1', 'B2'])
        belief.set_values([b1, b2])

        self.set_messages(essence, resource, belief)

        metabolism_1 = ResourceMap('Eat stuff', 'delta', 'R1', ('shift',))
        metabolism_2 = ResourceMap('Eat stuff', 'delta', 'R2', ('shift',))
        metabolism = MapCollection([metabolism_1, metabolism_2])
        belief_organ = Interpreter('Belief and Resource Tweak',
                                   self.belief_adj,
                                   belief, belief,
                                   metabolism)

class Mess(AgentManagementSystem):

    def __init__(self, name, agents, graph, a_env):

        super().__init__(name, agents, graph, a_env, 
                         restartable=True, strict_engine=True)

a1 = Bacteria('bacteria 1', 1.0, 1.0, 10.0, 10.0, 0.5, 0.5)
a2 = Bacteria('bacteria 2', 1.0, 0.5, 5.0, 6.0, 0.5, 0.5)
a3 = Bacteria('bacteria 3', 1.1, 0.3, 10.0, 2.0, 0.9, 0.1)


