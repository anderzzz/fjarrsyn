'''Integration test of mutation in its most basic form

'''
import pytest

import numpy as np
import numpy.random
np.random.seed(79)

from fjarrsyn.core.agent import Agent
from fjarrsyn.core.agent_ms import AgentManagementSystem
from fjarrsyn.core.message import Essence
from fjarrsyn.core.instructor import Mutation
from fjarrsyn.core.scaffold_map import EssenceMap

REF = [[0.7, 1.5, 0.5],
       [0.7, 1.5, 0.5],
       [0.7, 1.5, 0.5],
       [1.50705003, 1.5, 0.5],
       [1.61002839, 1.5, 0.5],
       [1.61002839, 1.5, 0.5],
       [1.61002839, 1.40113383, 0.5],
       [1.61002839, 1.40113383, 0.5],
       [1.61002839, 1.96674934, 0.5]]

def test_main():
    # HOW TO DEAL WITH RANDOM NUMBERS IN PYTEST?
    assert 1==2
    essence = Essence('inclinations', ['t_1', 't_2', 'volatility'])
    essence.set_values([0.7, 1.5, 0.5])

    agent = Agent('thin agent', strict_engine=True)
    agent.set_scaffold(essence)

    ams = AgentManagementSystem('exterior laws', [agent])

    mapper_1 = EssenceMap('tweak_1', 'wiener', 't_1', ('range_step',))
    mapper_2 = EssenceMap('tweak_2', 'wiener', 't_2', ('range_step',))
    mutate_1 = Mutation('jumps_1', essence.__getitem__, mapper_1,
                        mutation_prob=0.5,
                        mutate_func_kwargs={'key' : 'volatility'})
    mutate_2 = Mutation('jumps_2', essence.__getitem__, mapper_2,
                        mutation_prob=0.5,
                        mutate_func_kwargs={'key' : 'volatility'})
    ams.set_laws(mutate_1, mutate_2)

    print (agent.essence.values())
    assert (all([a == pytest.approx(b) for a, b in zip(agent.essence.values(), REF[0])]))
    ams.mutate(agent, 'jumps_1')
    print (agent.essence.values())
    assert (all([a == pytest.approx(b) for a, b in zip(agent.essence.values(), REF[1])]))
    ams.mutate(agent, 'jumps_1')
    print(agent.essence.values())
    assert (all([a == pytest.approx(b) for a, b in zip(agent.essence.values(), REF[2])]))
    ams.mutate(agent, 'jumps_1')
    print(agent.essence.values())
    assert (all([a == pytest.approx(b) for a, b in zip(agent.essence.values(), REF[3])]))
    ams.mutate(agent, 'jumps_1')
    print(agent.essence.values())
    assert (all([a == pytest.approx(b) for a, b in zip(agent.essence.values(), REF[4])]))
    ams.mutate(agent, 'jumps_2')
    print(agent.essence.values())
    assert (all([a == pytest.approx(b) for a, b in zip(agent.essence.values(), REF[5])]))
    ams.mutate(agent, 'jumps_2')
    print(agent.essence.values())
    assert (all([a == pytest.approx(b) for a, b in zip(agent.essence.values(), REF[6])]))
    ams.mutate(agent, 'jumps_2')
    print(agent.essence.values())
    assert (all([a == pytest.approx(b) for a, b in zip(agent.essence.values(), REF[7])]))
    ams.mutate(agent, 'jumps_2')
    print(agent.essence.values())
    assert (all([a == pytest.approx(b) for a, b in zip(agent.essence.values(), REF[8])]))
