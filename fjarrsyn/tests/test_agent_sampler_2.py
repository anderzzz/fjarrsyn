'''Test of sampling as method of agent and AMS 

'''
import pytest

from fjarrsyn.core.agent import Agent
from fjarrsyn.core.message import Belief, Essence, Resource
from fjarrsyn.core.agent_ms import AgentManagementSystem
from fjarrsyn.core.graph import Node
from fjarrsyn.simulation.sampler import AgentSampler, EnvSampler, GraphSampler

import networkx as nx
import pandas as pd

def _get_data(aux_env):
    return {'env_data_1' : aux_env.env_1, 
            'env_data_2' : aux_env.env_2}

class Env(object):

    def __init__(self, name, env_1, env_2):

        self.name = name
        self.env_1 = env_1
        self.env_2 = env_2

class Bacteria(Agent):

    def __init__(self, name, e1, e2, r1, r2, b1, b2):

        super().__init__(name, strict_engine=True)

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


def test_main():

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

    env_sampler = EnvSampler('feel_the_env', _get_data)
    g_sampler = GraphSampler('connections')

    mess = AgentManagementSystem('3 bacteria', [a1, a2, a3], a_graph)
    mess.set_sampler(a1.sampler['full_state'])
    mess.set_sampler(env_sampler)
    mess.set_sampler(g_sampler)

    x1 = a1.sample('full_state')
    x2 = a2.sample('full_state')
    x3 = a3.sample('full_state')

    y1 = mess.sample('full_state')
    y2 = mess.sample('feel_the_env')
    y3 = mess.sample('connections')

    assert (x1.shape == (6, 1))
    assert (x2.shape == (6, 1))
    assert (x3.shape == (6, 1))
    assert (x1.index.nlevels == 4)
    assert (x2.index.nlevels == 4)
    assert (x3.index.nlevels == 4)
    v1 = x1.loc[(slice(None), slice(None), slice(None), 'belief:Bacteria Belief:B1'), 'value'].values[0]
    v2 = x1.loc[(slice(None), slice(None), slice(None), 'belief:Bacteria Belief:B2'), 'value'].values[0]
    v3 = x1.loc[(slice(None), slice(None), slice(None), 'essence:Bacteria Essence:E1'), 'value'].values[0]
    v4 = x1.loc[(slice(None), slice(None), slice(None), 'essence:Bacteria Essence:E2'), 'value'].values[0]
    v5 = x1.loc[(slice(None), slice(None), slice(None), 'resource:Bacteria Resource:R1'), 'value'].values[0]
    v6 = x1.loc[(slice(None), slice(None), slice(None), 'resource:Bacteria Resource:R2'), 'value'].values[0]
    assert (v1 == 0.5)
    assert (v2 == 0.5)
    assert (v3 == 1.0)
    assert (v4 == 1.0)
    assert (v5 == 10.0)
    assert (v6 == 10.0)
    v1 = x2.loc[(slice(None), slice(None), slice(None), 'belief:Bacteria Belief:B1'), 'value'].values[0]
    v2 = x2.loc[(slice(None), slice(None), slice(None), 'belief:Bacteria Belief:B2'), 'value'].values[0]
    v3 = x2.loc[(slice(None), slice(None), slice(None), 'essence:Bacteria Essence:E1'), 'value'].values[0]
    v4 = x2.loc[(slice(None), slice(None), slice(None), 'essence:Bacteria Essence:E2'), 'value'].values[0]
    v5 = x2.loc[(slice(None), slice(None), slice(None), 'resource:Bacteria Resource:R1'), 'value'].values[0]
    v6 = x2.loc[(slice(None), slice(None), slice(None), 'resource:Bacteria Resource:R2'), 'value'].values[0]
    assert (v1 == 0.5)
    assert (v2 == 0.5)
    assert (v3 == 1.0)
    assert (v4 == 0.5)
    assert (v5 == 5.0)
    assert (v6 == 6.0)
    v1 = x3.loc[(slice(None), slice(None), slice(None), 'belief:Bacteria Belief:B1'), 'value'].values[0]
    v2 = x3.loc[(slice(None), slice(None), slice(None), 'belief:Bacteria Belief:B2'), 'value'].values[0]
    v3 = x3.loc[(slice(None), slice(None), slice(None), 'essence:Bacteria Essence:E1'), 'value'].values[0]
    v4 = x3.loc[(slice(None), slice(None), slice(None), 'essence:Bacteria Essence:E2'), 'value'].values[0]
    v5 = x3.loc[(slice(None), slice(None), slice(None), 'resource:Bacteria Resource:R1'), 'value'].values[0]
    v6 = x3.loc[(slice(None), slice(None), slice(None), 'resource:Bacteria Resource:R2'), 'value'].values[0]
    assert (v1 == 0.9)
    assert (v2 == 0.1)
    assert (v3 == 1.1)
    assert (v4 == 0.3)
    assert (v5 == 10.0)
    assert (v6 == 2.0)

    assert (y1.shape == (18, 1))
    assert (y1.index.nlevels == 4)
    assert (y1.index.levshape == (1, 3, 3, 6))
    ident = y1 == pd.concat([x1, x2, x3])
    assert (all(ident.values))

    assert (y2.shape == (6, 1))
    assert (y2.index.levshape == (1, 3, 3, 2))
    v1 = y2.loc[(slice(None), 'bacteria 1', slice(None), 'env_data_1'), 'value'].values[0]
    v2 = y2.loc[(slice(None), 'bacteria 1', slice(None), 'env_data_2'), 'value'].values[0]
    v3 = y2.loc[(slice(None), 'bacteria 2', slice(None), 'env_data_1'), 'value'].values[0]
    v4 = y2.loc[(slice(None), 'bacteria 2', slice(None), 'env_data_2'), 'value'].values[0]
    v5 = y2.loc[(slice(None), 'bacteria 3', slice(None), 'env_data_1'), 'value'].values[0]
    v6 = y2.loc[(slice(None), 'bacteria 3', slice(None), 'env_data_2'), 'value'].values[0]
    assert (v1 == 0.1)
    assert (v2 == 0.1)
    assert (v3 == 0.2)
    assert (v4 == 0.2)
    assert (v5 == 0.3)
    assert (v6 == 0.3)

    REF = [sorted((a1.agent_id_system, a2.agent_id_system)),
           sorted((a2.agent_id_system, a3.agent_id_system))]
    for ee in y3.edges:
        canonical = sorted(ee)
        assert (canonical in REF)
