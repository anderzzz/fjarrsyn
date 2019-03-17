'''Main runner routine for cooperative and trust growers

'''
from core.simulator import FiniteSystemRunner
from core.sampler import AgentSampler, EnvSampler, SystemIO
from core.graph import Node

from unit import Unit, AgentAuxEnv
from world import World
from propagation import UnitPlan, system_propagator 

import networkx as nx
import numpy as np

'''Parameters for running simulation

'''
'''Type and size of spatial network'''
NETWORK_TYPE = 'hexagonal lattice'
SQRT_N_AGENTS = 10
TOTAL_AGENTS = SQRT_N_AGENTS * SQRT_N_AGENTS

'''Rate of decay of compounds put into environment'''
ENV_DECAY_INVERSE = 0.0

'''Pool of agent essence for initialization agents'''
INIT_ESSENCE_POOL = [(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)]

'''Birth and Death parameters of agent'''
THRS_INFO_TO_SPLIT = 2.0
THRS_BAD_INFO_DEATH = 1.0

'''Non-Intentional System Parameters'''
MID_MAX_MOVE = 0.5
MAX_MAX_MOVE = 0.5
MUT_PROB = 0.01
RESOURCE_JUMP_MAG = 1.0
RESOURCE_JUMP_PROB = 0.05

'''Simulation parameters'''
N_ITER = 10

if __name__ == '__main__':

    if NETWORK_TYPE == 'hexagonal lattice':
        network = nx.generators.lattice.hexagonal_lattice_graph(SQRT_N_AGENTS,
                      SQRT_N_AGENTS, periodic=True)

    elif NETWORK_TYPE == 'small world':
        network = nx.generators.random_graphs.connected_watts_strogatz_graph(TOTAL_AGENTS,
                      6, 0.25)

    agent_plan = UnitPlan('One Heartbeat Step', THRS_INFO_TO_SPLIT,
                          THRS_BAD_INFO_DEATH)

    agents = []
    mapping = {}
    for coord in network.nodes():
        init_essence = np.random.choice(INIT_ESSENCE_POOL)
        agent_x = Unit('Agent', *init_essence)
        agent_x.set_policy(agent_plan)
        agents.append(agent_x)
        env_x = AgentAuxEnv(0.0, 0.0, 0.0, 0.0, ENV_DECAY_INVERSE)
        node = Node('{0}'.format(k_agent), agent_x, env_x)

        mapping[coord] = node
    network = nx.relabel_nodes(network, mapping)

    ww = World('Agent World', agents, network,
               MID_MAX_MOVE, MAX_MAX_MOVE, MUT_PROB,
               RESOURCE_JUMP_MAG, RESOURCE_JUMP_PROB)

    simulator = FiniteSystemRunner(N_ITER, system_propagator,
                    system_propagator_kwargs={'plan_name' : 'One Heartbeat Step'})

    simulator(ww)
