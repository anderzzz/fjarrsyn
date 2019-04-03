'''Main runner routine for cooperative and trust growers

'''
import sys
from core.simulator import FiniteSystemRunner
from core.sampler import AgentSampler, GraphSampler, EnvSampler, SystemIO
from core.graph import Node

from unit import Unit, AgentAuxEnv
from world import World
from propagation import UnitPolicy, system_propagator 

import networkx as nx
import numpy as np
import pandas as pd
import pickle

'''Parameters for running simulation

'''
'''Type and size of spatial network'''
NETWORK_TYPE = '2d grid lattice'
SQRT_N_AGENTS = 20 
TOTAL_AGENTS = SQRT_N_AGENTS * SQRT_N_AGENTS

'''Rate of decay of compounds put into environment'''
ENV_DECAY_INVERSE = 0.0

'''Pool of agent essence for initialization agents'''
TRUTHFUL_REVEAL = 1.0
INVERSE_FORGET_RATE = 0.0
INIT_ESSENCE_POOL = [(-0.5, 0.0, -0.5, 1.0, 0.0, 0.0, 
                      TRUTHFUL_REVEAL, INVERSE_FORGET_RATE),
                     (-0.5, 1.0, -0.5, 1.0, 0.0, 0.0,
                      TRUTHFUL_REVEAL, INVERSE_FORGET_RATE),
                     (0.9, 1.0, -0.5, 1.0, 0.0, 0.0,
                      TRUTHFUL_REVEAL, INVERSE_FORGET_RATE),
                     (0.9, 1.0, -0.5, 1.0, 0.0, 0.0,
                      TRUTHFUL_REVEAL, INVERSE_FORGET_RATE),
                     (0.9, 1.0, -0.5, 1.0, 0.0, 0.0,
                      TRUTHFUL_REVEAL, INVERSE_FORGET_RATE),
                     (0.9, 1.0, -0.5, 1.0, 0.0, 0.0,
                      TRUTHFUL_REVEAL, INVERSE_FORGET_RATE),
                     (0.9, 1.0, -0.5, 1.0, 0.0, 0.0,
                      TRUTHFUL_REVEAL, INVERSE_FORGET_RATE)]

'''Birth and Death parameters of agent'''
THRS_INFO_TO_SPLIT = 2.0
THRS_BAD_INFO_DEATH = 2.0

'''Non-Intentional System Parameters'''
MID_MAX_MOVE = 0.5
MAX_MAX_MOVE = 0.5
MUT_PROB = 0.001
RESOURCE_JUMP_MAG = 1.0
RESOURCE_JUMP_PROB = 0.05
MUT_ESSENCE = ['share','gulp','tox']

'''Simulation parameters'''
N_ITER = 10001 
N_SAMPLE = 1000

'''Load or Start New World'''
LOAD_WORLD=False
GENERATION_OFFSET=0

def _extract_env_container(aux):
    return aux.container

def load_old_world(load_dir):

    #
    # Saved files
    #
    agent_file = load_dir + '/save_agent_state0.csv'
    env_file = load_dir + '/save_env_state0.csv'
    graph_file = load_dir + '/save_graph_state0.edgelist'

    #
    # Define agent intentions
    #
    agent_policy = UnitPolicy('One Heartbeat Step', THRS_INFO_TO_SPLIT,
                              THRS_BAD_INFO_DEATH)

    #
    # Create populated Agents
    #
    df_a = pd.read_csv(agent_file)
    gg_a = df_a.groupby('agent_index')
    agents = {} 
    for a_id, a_data in gg_a:
        belief_d = {}
        essence_d = {}
        resource_d = {}

        agent = Unit('Agent', agent_id=a_id)
        for _, row in a_data.iterrows():
            dd = row.to_dict()
            xx = dd['variable'].split(':')

            if xx[0] == 'belief':
                belief_d[(xx[1], xx[2])] = dd['value']
            if xx[0] == 'essence':
                essence_d[xx[2]] = dd['value']
            if xx[0] == 'resource':
                resource_d[xx[2]] = dd['value']

        essence_val = []
        for e_key in agent.essence.keys():
            essence_val.append(essence_d[e_key])

        resource_val = []
        for r_key in agent.resource.keys():
            resource_val.append(resource_d[r_key])

        belief_val = []
        for b_key_1 in agent.belief:
            for b_key_2 in agent.belief[b_key_1].keys():
                belief_val.append(belief_d[(b_key_1, b_key_2)])

        agent.essence.set_values(essence_val)
        agent.resource.set_values(resource_val)
        agent.belief[b_key_1].set_values(belief_val)
        agent.set_policies(*agent_policy.all)

        agents[a_id] = agent

    #
    # Create populated environments
    #
    df_e = pd.read_csv(env_file)
    gg_e = df_e.groupby('agent_index')
    envs = {}
    for a_id, e_data in gg_e:
        r_container = {}
        for _, row in e_data.iterrows():
            dd = row.to_dict()
            r_container[dd['variable']] = dd['value']
        env = AgentAuxEnv(**r_container)

        envs[a_id] = env

    #
    # Make Nodes
    #
    nodes = {}
    for a_id in agents:
        nn = Node('', agents[a_id], envs[a_id])
        nodes[a_id] = nn

    #
    # Make the Graph
    #
    graph = nx.Graph()
    graph.add_nodes_from(nodes.values())
    fin = open(graph_file)
    lines = fin.read().split('\n')
    for line in lines[:-1]:
        xx = line.split(' ')
        n1 = nodes[xx[0]]
        n2 = nodes[xx[1]]
        graph.add_edge(n1, n2)

    ww = World('Agent World', agents.values(), graph,
               MID_MAX_MOVE, MAX_MAX_MOVE, MUT_PROB,
               RESOURCE_JUMP_MAG, RESOURCE_JUMP_PROB,
               MUT_ESSENCE)

    return ww

def create_new_world():

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
               RESOURCE_JUMP_MAG, RESOURCE_JUMP_PROB,
               MUT_ESSENCE)

    return ww

if __name__ == '__main__':

    path_root = sys.argv[1]

    if LOAD_WORLD:
        ww = load_old_world(path_root)

    else:
        ww = create_new_world()

    #
    # Define samplers
    #
    a_sampler = AgentSampler('standard_agent',
                             essence_args=[('Exterior Disposition', 'midpoint_share'),
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
    g_sampler = GraphSampler('standard_graph', sample_steps=N_SAMPLE)
    e_sampler = EnvSampler('standard_env', _extract_env_container, sample_steps=N_SAMPLE)

    system_io = SystemIO([(path_root + '/agent_sample', a_sampler, 'to_csv'), 
                          (path_root + '/graph_sample', g_sampler, 'edgelist.write_edgelist'),
                          (path_root + '/env_sample', e_sampler, 'to_csv')])

    #
    # Set up how to propagate and sample world with agents
    #
    simulator = FiniteSystemRunner(N_ITER, system_propagator,
                    GENERATION_OFFSET,
                    system_io=system_io,
                    system_propagator_kwargs={'plan_name' : 'One Heartbeat Step'})


    #
    # Run simulation
    #
    simulator(ww)

    #
    # Pickle the world for restarts
    #
    ww.save(path_root)

