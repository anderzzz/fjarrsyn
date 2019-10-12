'''Integration test of various agent and system sampling scenarios

'''
from fjarrsyn.core.agent import Agent
from fjarrsyn.core.agent_ms import AgentManagementSystem
from fjarrsyn.core.message import Belief, Essence, Resource
from fjarrsyn.core.graph import Node

import networkx as nx

REF1 = {'essence' : [('Coordinator Essence', 'param_1'),
                     ('Coordinator Essence', 'param_2'),
                     ('Coordinator Essence', 'param_3'),
                     ('Coordinator Essence', 'param_4'),
                     ('Coordinator Essence', 'param_5'),
                     ('Coordinator Essence', 'param_6')],
        'resource' : [('Coordinator Resource', 'Energy Status')]}
REF1_LENS = {'essence' : 6, 'resource' : 1}
REF2 = {'essence' : [('Leaf Essence', 'param_1')],
        'belief' : [('Kind World', 'value'),
                    ('Physical World', 'temp'),
                    ('Physical World', 'wind'),
                    ('Physical World', 'humidity')]}
REF2_LENS = {'essence' : 1, 'belief' : 4}


agent_core = Agent('Coordinator')
essence = Essence('Coordinator Essence', ('param_1', 'param_2', 'param_3',
                                          'param_4', 'param_5', 'param_6'))
essence.set_values([1.0,2.0,3.0,4.0,5.0,6.0])
resource = Resource('Coordinator Resource', ('Energy Status',))
resource.set_values([75.0])
agent_core.set_scaffolds(essence, resource)

agents = [agent_core]
nodes = [Node('A1', agent_core)]

agent_leaf = Agent('Leaf')
essence = Essence('Leaf Essence', ('param_1',))
essence.set_values([-100.0])
agent_leaf.set_scaffold(essence)

belief_1 = Belief('Kind World', ('value',))
belief_2 = Belief('Physical World', ('temp', 'wind', 'humidity'))
agent_leaf.set_messages(belief_1, belief_2)

agents.append(agent_leaf)
nodes.append(Node('A2', agent_leaf))

star_graph = nx.generators.classic.star_graph(nodes)
ams = AgentManagementSystem('tests', agents, star_graph)

for agent in ams.cycle_nodes(agents_only=True, max_iter=2):
    data = agent.get_imprint_repr()

    if 'resource' in data.keys():
        for imprint_type, vals in data.items():
            for val_tuple in vals:
                assert (val_tuple in REF1[imprint_type])

            assert (len(vals) == REF1_LENS[imprint_type])

    elif 'belief' in data.keys():
        for imprint_type, vals in data.items():
            for val_tuple in vals:
                assert (val_tuple in REF2[imprint_type])

            assert (len(vals) == REF2_LENS[imprint_type])


