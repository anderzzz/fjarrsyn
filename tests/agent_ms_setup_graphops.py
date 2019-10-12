'''Integration test of various ways to access the agent graph

'''
import numpy as np
import numpy.random
np.random.seed(79)

from fjarrsyn.core.agent import Agent
from fjarrsyn.core.agent_ms import AgentManagementSystem
from fjarrsyn.core.graph import Node

import networkx as nx

agent_1 = Agent('A1', strict_engine=True)
agent_2 = Agent('A2', strict_engine=True)
agent_3 = Agent('A3', strict_engine=True)
agents = [agent_1, agent_2, agent_3]
node = [Node('dummy', a) for a in agents]

graph = nx.Graph()
graph.add_nodes_from(node)
graph.add_edge(node[0], node[1])
graph.add_edge(node[1], node[2])

ams = AgentManagementSystem('tester', agents, graph)

n_to_1 = ams.neighbours_to(agent_1.agent_id_system)
n_to_2 = ams.neighbours_to(agent_2.agent_id_system)
n_to_3 = ams.neighbours_to(agent_3.agent_id_system)

assert (list(map(lambda x: x.name, n_to_1)) == ['A2'])
assert (sorted(list(map(lambda x: x.name, n_to_2))) == ['A1', 'A3'])
assert (list(map(lambda x: x.name, n_to_3)) == ['A2'])

assert (ams.edge_property(agent_1.agent_id_system, agent_2.agent_id_system)[0])
assert (not ams.edge_property(agent_1.agent_id_system, agent_3.agent_id_system)[0])
assert (ams.edge_property(agent_2.agent_id_system, agent_3.agent_id_system)[0])

ams.edge_edit(agent_1.agent_id_system, agent_3.agent_id_system, add=True)
ams.edge_edit(agent_1.agent_id_system, agent_2.agent_id_system, delete=True)

assert (not ams.edge_property(agent_1.agent_id_system, agent_2.agent_id_system)[0])
assert (ams.edge_property(agent_1.agent_id_system, agent_3.agent_id_system)[0])
assert (ams.edge_property(agent_2.agent_id_system, agent_3.agent_id_system)[0])

graph.add_node(Node('dummy', None))
assert (not ams.choice_nodes(True) is None)
assert (not ams.choice_nodes(True) is None)
assert (not ams.choice_nodes(True) is None)
assert (not ams.choice_nodes(True) is None)
assert (not ams.choice_nodes(True) is None)
assert (not ams.choice_nodes(True) is None)
assert (not ams.choice_nodes(True) is None)
assert (not ams.choice_nodes(True) is None)
assert (not ams.choice_nodes(True) is None)
assert (not ams.choice_nodes(True) is None)

n1 = 0
n2 = 0
n3 = 0
n_none = 0
for node in ams.shuffle_nodes(False, 16, replace=False):
    agent = node.agent_content
    if not agent is None:
        if agent.name == 'A1':
            n1 += 1
        if agent.name == 'A2':
            n2 += 1
        if agent.name == 'A3':
            n3 += 1
    else:
        n_none += 1

assert (n1 == 4)
assert (n2 == 4)
assert (n3 == 4)
assert (n_none == 4)
