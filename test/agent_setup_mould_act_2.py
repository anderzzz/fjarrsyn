'''Integration test of agent setup of Moulder and Actuator including
multi-valued resource map functions

'''
from core.agent import Agent

from core.instructor import Moulder, Actuator
from core.message import Belief, Direction, Resource
from core.scaffold_map import ResourceMap, MapCollection 
from core.array import EmptyFlashError

REF = {'A' : 1.01, 'B' : 0.75, 'C' : 0.63}

def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def make_decision(stress_degree):
    return stress_degree / 100.0
    

class Env(object):
    def excretor(self, intake_volume):
        a_piece = self.a_amount * intake_volume
        b_piece = self.b_amount * intake_volume
        c_piece = self.c_amount * intake_volume
        self.a_amount -= a_piece
        self.b_amount -= b_piece
        self.c_amount -= c_piece
        return a_piece, 0.5, b_piece, 0.75, c_piece, 0.9 

    def __init__(self):
        self.a_amount = 0.2
        self.b_amount = 0.0
        self.c_amount = 2.0

#
# Define Messages
#
belief = Belief('stressed', ('degree',))
belief.set_values(10.0)
direction1 = Direction('collect_amount', ('intake_volume',))

#
# Define Scaffold and Map for it
#
agent_resources = Resource('internal_molecules', ('A','B','C'))
agent_resources.set_values([2.0, 1.0, 0.5])
added_a = ResourceMap('get_A', 'delta_scale', 'A', ('add','dilute',))
added_b = ResourceMap('get_B', 'delta_scale', 'B', ('add','dilute',))
added_c = ResourceMap('get_C', 'delta_scale', 'C', ('add','dilute',))
add_internal = MapCollection([added_a, added_b, added_c])

#
# Define Organs and their associated messages
#
moulder1 = Moulder('discard_or_not', make_decision, belief, direction1)

env = Env()
actuator1 = Actuator('collect', env.excretor, direction1, add_internal)

#
# Initialize Agent
#
agent = Agent('test_agent', True)
agent.set_organ(moulder1)
agent.set_organ(actuator1)
agent.set_scaffold(agent_resources)

#
# Decide on direction and execute action
#
agent.mould('discard_or_not')
agent.act('collect')

for mol in REF:
    assert (isclose(REF[mol], agent.resource[mol], abs_tol=0.0001))

try:
    agent.act('collect')
    raise AssertionError('Acting twice in sequence did not raise correct exception')
except EmptyFlashError: 
    pass
