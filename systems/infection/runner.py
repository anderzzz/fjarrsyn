'''Main runner routine for cooperative and trust growers

'''
from core.simulator import FiniteSystemRunner
from core.sampler import AgentSampler, EnvSampler, SystemIO
from core.graph import Node

from unit import Unit, AgentAuxEnv
from world import World
from propagation import UnitPlan

import networkx as nx
import numpy as np

NETWORK_TYPE = 'hexagonal lattice'
SQRT_N_AGENTS = 10
TOTAL_AGENTS = SQRT_N_AGENTS * SQRT_N_AGENTS

ENV_DECAY_INVERSE = 0.0

INIT_ESSENCE_POOL = [(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)]

if __name__ == '__main__':

    if NETWORK_TYPE == 'hexagonal lattice':
        network = nx.generators.lattice.hexagonal_lattice_graph(SQRT_N_AGENTS,
                      SQRT_N_AGENTS, periodic=True)

    elif NETWORK_TYPE == 'small world':
        network = nx.generators.random_graphs.connected_watts_strogatz_graph(TOTAL_AGENTS,
                      6, 0.25)

    mapping = {}
    for coord in network.nodes():
        init_essence = np.random.choice(INIT_ESSENCE_POOL)
        agent_x = Unit('Agent', *init_essence)
        env_x = AgentAuxEnv(0.0, 0.0, 0.0, 0.0, ENV_DECAY_INVERSE)
        node = Node('{0}'.format(k_agent), agent_x, env_x)

        mapping[coord] = node
    network = nx.relabel_nodes(network, mapping)

u1 = Unit('test0', 0.5, 0.8, 0.0, 1.0, 1.0, 1.0)
u2 = Unit('test1', 0.5, 0.8, 0.0, 0.0, 1.0, 1.0)

u_plan = UnitPlan('One Time Step', 1.0, 1.0)
u1.set_policy(u_plan)
u2.set_policy(u_plan)

env_agent = [AgentAuxEnv(0.0, 2.0, 0.0, 0.0), AgentAuxEnv(0.5, 0.5, 0.5, 0.0)]

ww = World('test_world', [u1, u2], env_agent, 0.5, 0.5, 0.25)

u1.sense('Feel Neighbour Surface')
u1.interpret('Friendly Environment')
u1.mould('Share Resources')
u1.act('Share Resources to Neighbours')
u1.mould('Eject Lies')
u1.act('Spread Lies to Neighbours')
u1.mould('Gulp from Env')
u1.act('Gulp Environment')

ww.mutate(u1, 'Perturb Essence 1')

for nn in ww:
    print (nn)
    print (nn.agent_content.name)
    print (nn.agent_content.resource, nn.aux_content.container,
    nn.agent_content.essence)

u1.mould('Create Agent Offspring')
u1.act('Push Offspring Onto World')

for nn in ww:
    print (nn)
    print (nn.agent_content.name)
    print (nn.agent_content.resource, nn.aux_content.container,
    nn.agent_content.essence)

