'''Main runner routine for cooperative and trust growers

'''
from core.simulator import FiniteSystemRunner
from core.sampler import AgentSampler, GraphSampler, EnvSampler, SystemIO
from core.graph import Node

from unit import Unit, AgentAuxEnv
from world import World
from propagation import UnitPolicy, system_propagator 

import networkx as nx
import numpy as np

'''Parameters for running simulation

'''
'''Type and size of spatial network'''
NETWORK_TYPE = '2d grid lattice'
SQRT_N_AGENTS = 3
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
RESOURCE_JUMP_PROB = 0.01

'''Simulation parameters'''
N_ITER = 10000 
N_SAMPLE = 1000

if __name__ == '__main__':

    #
    # Define the spatial arrangement
    #
    if NETWORK_TYPE == '2d grid lattice':
        network = nx.generators.lattice.grid_2d_graph(SQRT_N_AGENTS,
                      SQRT_N_AGENTS, periodic=True)

    elif NETWORK_TYPE == 'small world':
        network = nx.generators.random_graphs.connected_watts_strogatz_graph(TOTAL_AGENTS,
                      4, 0.25)

    else:
        raise RuntimeError('Unknown network type: {0}'.format(NETWORK_TYPE))

    #
    # Define agent intentions
    #
    agent_policy = UnitPolicy('One Heartbeat Step', THRS_INFO_TO_SPLIT,
                              THRS_BAD_INFO_DEATH)

    #
    # Place agents in spatial arrangement and assing them intentions
    #
    agents = []
    mapping = {}
    for k_agent, coord in enumerate(network.nodes()):
        init_essence = INIT_ESSENCE_POOL[np.random.randint(len(INIT_ESSENCE_POOL))]
        agent_x = Unit('Agent', *init_essence)
        agent_x.set_policies(*agent_policy.all)
        agents.append(agent_x)

        env_x = AgentAuxEnv(0.0, 0.0, 0.0, 0.0, ENV_DECAY_INVERSE)
        node = Node('{0}'.format(k_agent), agent_x, env_x)

        mapping[coord] = node

    network = nx.relabel_nodes(network, mapping)

    #
    # Define the world
    #
    ww = World('Agent World', agents, network,
               MID_MAX_MOVE, MAX_MAX_MOVE, MUT_PROB,
               RESOURCE_JUMP_MAG, RESOURCE_JUMP_PROB)

    #
    # Define samplers
    #
    a_sampler = AgentSampler(essence_args=[('Exterior Disposition', 'midpoint_share'),
                    ('Exterior Disposition', 'max_share'),
                    ('Exterior Disposition', 'midpoint_gulp'),
                    ('Exterior Disposition', 'max_gulp'),
                    ('Exterior Disposition', 'midpoint_tox'),
                    ('Exterior Disposition', 'max_tox')],
                             resource_args=[('Internal Resources', 'info_a'),
                    ('Internal Resources', 'info_b'),
                    ('Internal Resources', 'info_c'),
                    ('Internal Resources', 'bad_info')],
                             sample_steps=N_SAMPLE)
    g_sampler = GraphSampler(sample_steps=N_SAMPLE)
    system_io = SystemIO([('agent_sample', a_sampler, 'to_csv'), 
                          ('graph_sample', g_sampler, 'edgelist.write_edgelist')])

    #
    # Set up how to propagate and sample world with agents
    #
    simulator = FiniteSystemRunner(N_ITER, system_propagator,
                    system_io=system_io,
                    system_propagator_kwargs={'plan_name' : 'One Heartbeat Step'})


    #
    # Run simulation
    #
    simulator(ww)
