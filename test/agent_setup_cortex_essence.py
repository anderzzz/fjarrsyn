'''Simple Agent Setup Integration Test

'''
import numpy as np
import numpy.random
np.random.seed(79)

from core.agent import Agent

from core.organs import Cortex 
from core.message import Feature 
from core.scaffold import Essence

REF1 = [0.9000, 0.3984, 1.0000]
REF2 = [0.8825, 0.4160, 0.9911]

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
agent_essence.set_elements([0.9, 0.4, 1.0, 'jubilant'])
slice_of_essence = agent_essence.slicer(['hue', 'saturation', 'lightness'])

#
# Define Organs and their associated messages
#
cortex = Cortex('colour_revealer', slice_of_essence, expose_distort,
                feature, {'distort_degree' : 0.05})

#
# Initialize Agent
#
agent = Agent('test_agent')
agent.set_organ(cortex)
agent.set_scaffold(agent_essence)

#
# Tickle the cortex 
#
tickle_me_1 = agent.tickle('colour_revealer')
for val, ref_val in zip(tickle_me_1.read_value(), REF1):
    assert (isclose(val, ref_val, abs_tol=0.01))

tickle_me_2 = agent.tickle('colour_revealer')
for val, ref_val in zip(tickle_me_2.read_value(), REF2):
    assert (isclose(val, ref_val, abs_tol=0.01))
