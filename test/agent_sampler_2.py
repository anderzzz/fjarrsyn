'''Test of restartable AMS

'''
from core.agent import Agent
from core.message import Belief, Essence, Resource
from core.agent_ms import AgentManagementSystem
from core.graph import Node
from core.sampler import AgentSampler

import networkx as nx

class Env(object):

    def __init__(self, name, env_1, env_2):

        self.name = name
        self.env_1 = env_1
        self.env_2 = env_2

class Bacteria(Agent):

    def __init__(self, name, e1, e2, r1, r2, b1, b2):

        super().__init__(name, True)

        essence = Essence('Bacteria Essence', ['E1', 'E2'])
        essence.set_values([e1, e2])
        
        resource = Resource('Bacteria Resource', ['R1', 'R2'])
        resource.set_values([r1, r2])

        belief = Belief('Bacteria Belief', ['B1', 'B2'])
        belief.set_values([b1, b2])

        self.set_scaffolds(essence, resource)
        self.set_message(belief)

        imprints = self.get_imprint_repr()
        total_a_sampler = AgentSampler('full_state',
                               resource_args=imprints['resource'],
                               essence_args=imprints['essence'],
                               belief_args=imprints['belief'])
        self.set_sampler(total_a_sampler)

a1 = Bacteria('bacteria 1', 1.0, 1.0, 10.0, 10.0, 0.5, 0.5)
a2 = Bacteria('bacteria 2', 1.0, 0.5, 5.0, 6.0, 0.5, 0.5)
a3 = Bacteria('bacteria 3', 1.1, 0.3, 10.0, 2.0, 0.9, 0.1)
e1 = Env('environment 1', 0.1, 0.1)
e2 = Env('environment 2', 0.2, 0.2)
e3 = Env('environment 3', 0.3, 0.3)
n1 = Node('first', a1, e1)
n2 = Node('second', a2, e2)
n3 = Node('third', a3, e3)

a_graph = nx.Graph()
a_graph.add_edge(n1, n2)
a_graph.add_edge(n2, n3)

mess = AgentManagementSystem('3 bacteria', [a1, a2, a3], a_graph)

xx = a1.sample('full_state')
print (xx)
xx = a2.sample('full_state')
print (xx)
xx = a3.sample('full_state')
print (xx)

raise NotImplementedError('Test not fully made')
