'''Integration test: move agent and agent environment around in a graph

'''
import pytest

from fjarrsyn.core.agent import Agent
from fjarrsyn.core.agent_ms import AgentManagementSystem
from fjarrsyn.core.graph import Node

import networkx as nx

class LocalEnv(object):
    def __init__(self, value):
        self.value = value

agent_1 = Agent('The first')
agent_2 = Agent('The second')
agent_3 = Agent('The third')
node_1 = Node('N1', agent_1, LocalEnv(1))
node_2 = Node('N2', agent_2, LocalEnv(2))
node_3 = Node('N3', agent_3, LocalEnv(3))
node_4 = Node('N4', None, LocalEnv(4))
node_5 = Node('N5', None, LocalEnv(5))
node_6 = Node('N6', None, LocalEnv(6))
nodes = [node_1, node_2, node_3, node_4, node_5, node_6]
agraph = nx.generators.classic.cycle_graph(nodes)

ams = AgentManagementSystem('cycle', [agent_1, agent_2, agent_3],
                            full_agents_graph=agraph)

ams.switch_node_content(node_1, node_2, switch_agent=True, switch_aux=True)
node_x = ams.get(agent_1.agent_id_system, get_node=True)
node_y = ams.get(agent_2.agent_id_system, get_node=True)

assert (node_x.name == 'N2')
assert (node_y.name == 'N1')
assert (node_x.aux_content.value == 1)
assert (node_y.aux_content.value == 2)

ams.switch_node_content(node_3, node_4, switch_agent=True, switch_aux=False)
node_x = ams.get(agent_3.agent_id_system, get_node=True)

assert (node_x.name == 'N4')
assert (node_3.agent_content is None)
assert (node_x.aux_content.value == 4)
assert (node_3.aux_content.value == 3)

ams.switch_node_content(node_6, node_1, switch_agent=True, switch_aux=True)

assert (node_1.agent_content is None)
assert (node_6.agent_content.name == 'The second')
assert (node_1.aux_content.value == 6)
assert (node_6.aux_content.value == 2)

ams.switch_node_content(node_6, node_1, switch_agent=False, switch_aux=True)

assert (node_1.agent_content is None)
assert (node_6.agent_content.name == 'The second')
assert (node_1.aux_content.value == 2)
assert (node_6.aux_content.value == 6)
