'''Integration test of mutation in its most basic form

'''
import numpy as np
import numpy.random
np.random.seed(79)

from fjarrsyn.core.agent import Agent
from fjarrsyn.core.agent_ms import AgentManagementSystem
from fjarrsyn.core.message import Essence
from fjarrsyn.core.instructor import MultiMutation
from fjarrsyn.core.scaffold_map import EssenceMap, MapCollection

def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

REF = [[0.0, 0.0, 0.0, 0.0, 0.0],
       [0.0, 1.080244, 0.0, -0.691219, 0.0],
       [0.0, 1.056428, 1.460206, -0.691219, 0.0],
       [0.0, 1.056428, 0.628979, -1.344839, 0.578392],
       [-2.513790, 1.056428, 0.628979, -1.344839, 0.578392]]

essence = Essence('inclinations', ['t_1', 't_2', 't_3', 't_4', 't_5']) 
essence.set_values([0.0, 0.0, 0.0, 0.0, 0.0])

agent = Agent('thin agent', strict_engine=True)
agent.set_scaffold(essence)

ams = AgentManagementSystem('exterior laws', [agent])

mapper_1 = EssenceMap('tweak', 'wiener', 't_1', ('range_step',))
mapper_2 = EssenceMap('tweak', 'wiener', 't_2', ('range_step',))
mapper_3 = EssenceMap('tweak', 'wiener', 't_3', ('range_step',))
mapper_4 = EssenceMap('tweak', 'wiener', 't_4', ('range_step',))
mapper_5 = EssenceMap('tweak', 'wiener', 't_5', ('range_step',))
mapper = MapCollection([mapper_1, mapper_2, mapper_3, mapper_4, mapper_5])
mutate = MultiMutation('jumps', lambda : 1.0, mapper, 
                       mutation_prob=0.5)
ams.set_law(mutate)

vals = agent.essence.values()
assert (all([isclose(x, y, abs_tol=0.000001) for x, y in zip(vals, REF[0])]))
ams.mutate(agent, 'jumps')
vals = agent.essence.values()
assert (all([isclose(x, y, abs_tol=0.000001) for x, y in zip(vals, REF[1])]))
ams.mutate(agent, 'jumps')
vals = agent.essence.values()
assert (all([isclose(x, y, abs_tol=0.000001) for x, y in zip(vals, REF[2])]))
ams.mutate(agent, 'jumps')
vals = agent.essence.values()
assert (all([isclose(x, y, abs_tol=0.000001) for x, y in zip(vals, REF[3])]))
ams.mutate(agent, 'jumps')
vals = agent.essence.values()
assert (all([isclose(x, y, abs_tol=0.000001) for x, y in zip(vals, REF[4])]))
