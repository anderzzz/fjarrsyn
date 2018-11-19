'''Integration test of agent setup of Cortex that generates a feature based on
agent essence

'''
import numpy as np
import numpy.random
np.random.seed(79)

from core.agent import Agent

from core.instructor import Cortex 
from core.message import Feature, Essence, MessageOperator

REF1 = [0.9000, 0.3984, 1.0000]
REF2 = [0.8825, 0.4160, 0.9911]
REF3 = [0.0140, 0.0158, 0.0000]

def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def expose_distort(h, s, l, distort_degree):
    pert1 = distort_degree * (np.random.random() - 0.5)
    pert2 = distort_degree * (np.random.random() - 0.5)
    pert3 = distort_degree * (np.random.random() - 0.5)
    h_ret = max(0.0, min(1.0, h + pert1))
    s_ret = max(0.0, min(1.0, s + pert2))
    l_ret = max(0.0, min(1.0, l + pert3))
    return h_ret, s_ret, l_ret 
#
# Define Messages
#
feature = Feature('colour', ('hue', 'saturation', 'lightness'))

#
# Define Scaffold 
#
agent_essence = Essence('my_parameters', ('hue', 'saturation', 'lightness', 'mood'))
agent_essence.set_values([0.9, 0.4, 1.0, 'jubilant'])
slicer_of_essence = MessageOperator(agent_essence, 
                        slice_labels=['hue', 'saturation', 'lightness'])
#
# Define Organs and their associated messages
#
cortex = Cortex('colour_revealer', expose_distort, slicer_of_essence,
                feature, cortex_func_kwargs={'distort_degree' : 0.05})

#
# Initialize Agent
#
agent = Agent('test_agent', True)
agent.set_organ(cortex)
agent.set_scaffold(agent_essence)

#
# Tickle the cortex 
#
tickle_me_1 = agent.tickle('colour_revealer')
for val, ref_val in zip(tickle_me_1.values(), REF1):
    assert (isclose(val, ref_val, abs_tol=0.01))

tickle_me_2 = agent.tickle('colour_revealer')
for val, ref_val in zip(tickle_me_2.values(), REF2):
    assert (isclose(val, ref_val, abs_tol=0.01))

agent_essence.set_values([0.0, 0.0, 0.0, 'hey'])
tickle_me_3 = agent.tickle('colour_revealer')
for val, ref_val in zip(tickle_me_3.values(), REF3):
    assert(isclose(val, ref_val, abs_tol=0.01))

