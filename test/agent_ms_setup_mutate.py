'''Integration test of mutation in its most basic form

'''
import numpy as np
import numpy.random
np.random.seed(79)

from core.agent import Agent
from core.agent_ms import AgentManagementSystem
from core.message import Essence
from core.instructor import Mutation
from core.scaffold_map import EssenceMap

def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

REF = [[0.7, 1.5, 0.5],
       [0.7, 1.5, 0.5],
       [0.10474766, 1.5, 0.5],
       [0.10474766, 1.5, 0.5],
       [0.10607540, 1.5, 0.5],
       [0.10607540, 1.5, 0.5],
       [0.10607540, 1.5, 0.5],
       [0.10607540, 1.87377771, 0.5],
       [0.10607540, 1.87377771, 0.5]]

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

assert (all([isclose(a, b, abs_tol=0.0000001) for a, b in zip(agent.essence.values(), REF[0])]))
ams.mutate(agent, 'jumps_1')
assert (all([isclose(a, b, abs_tol=0.0000001) for a, b in zip(agent.essence.values(), REF[1])]))
ams.mutate(agent, 'jumps_1')
assert (all([isclose(a, b, abs_tol=0.0000001) for a, b in zip(agent.essence.values(), REF[2])]))
ams.mutate(agent, 'jumps_1')
assert (all([isclose(a, b, abs_tol=0.0000001) for a, b in zip(agent.essence.values(), REF[3])]))
ams.mutate(agent, 'jumps_1')
assert (all([isclose(a, b, abs_tol=0.0000001) for a, b in zip(agent.essence.values(), REF[4])]))
ams.mutate(agent, 'jumps_2')
assert (all([isclose(a, b, abs_tol=0.0000001) for a, b in zip(agent.essence.values(), REF[5])]))
ams.mutate(agent, 'jumps_2')
assert (all([isclose(a, b, abs_tol=0.0000001) for a, b in zip(agent.essence.values(), REF[6])]))
ams.mutate(agent, 'jumps_2')
assert (all([isclose(a, b, abs_tol=0.0000001) for a, b in zip(agent.essence.values(), REF[7])]))
ams.mutate(agent, 'jumps_2')
assert (all([isclose(a, b, abs_tol=0.0000001) for a, b in zip(agent.essence.values(), REF[8])]))
