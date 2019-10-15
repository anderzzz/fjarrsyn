'''Integration test of agent setup of Cortex that generates a feature based on
agent essence

'''
import pytest

from fjarrsyn.core.agent import Agent
from fjarrsyn.core.instructor import Cortex
from fjarrsyn.core.message import Feature, Essence, MessageOperator

FLOAT_POOL = [0.5006681263403812, 0.4680674259481151, 0.5007825256422324,
              0.1491781654521081, 0.8202779358194150, 0.3213640316096379,
              0.7791739971074133, 0.8150803078792227, 0.01480227728137401]

REF1 = [0.9000, 0.3984, 1.0000]
REF2 = [0.8825, 0.4160, 0.9911]
REF3 = [0.0140, 0.0158, 0.0000]

def expose_distort(h, s, l, distort_degree):
    pert1 = distort_degree * (FLOAT_POOL.pop(0) - 0.5)
    pert2 = distort_degree * (FLOAT_POOL.pop(0) - 0.5)
    pert3 = distort_degree * (FLOAT_POOL.pop(0) - 0.5)
    h_ret = max(0.0, min(1.0, h + pert1))
    s_ret = max(0.0, min(1.0, s + pert2))
    l_ret = max(0.0, min(1.0, l + pert3))
    return h_ret, s_ret, l_ret 

def test_main():
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
    agent = Agent('test_agent', strict_engine=True)
    agent.set_organ(cortex)
    agent.set_scaffold(agent_essence)

    #
    # Tickle the cortex
    #
    tickle_me_1 = agent.tickle('colour_revealer')
    for val, ref_val in zip(tickle_me_1.values(), REF1):
        assert (val == pytest.approx(ref_val, abs=1e-3))

    tickle_me_2 = agent.tickle('colour_revealer')
    for val, ref_val in zip(tickle_me_2.values(), REF2):
        assert (val == pytest.approx(ref_val, abs=1e-3))

    agent_essence.set_values([0.0, 0.0, 0.0, 'hey'])
    tickle_me_3 = agent.tickle('colour_revealer')
    for val, ref_val in zip(tickle_me_3.values(), REF3):
        assert(val == pytest.approx(ref_val, abs=1e-3))

