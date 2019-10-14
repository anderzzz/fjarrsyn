'''Integration test of agent setup of Moulder and Actuator organs with multiple
output Directions and Resource Maps

'''
from fjarrsyn.core.agent import Agent

from fjarrsyn.core.instructor import Moulder, Actuator
from fjarrsyn.core.message import Belief, Direction, Resource, MessageOperator
from fjarrsyn.core.scaffold_map import ResourceMap, MapCollection
from fjarrsyn.core.array import EmptyFlashError

REF_REPO = [('v', 0, 1.0), ('h', -1, 0.5), ('v', -1, 1.0), ('h', 1, 0.5)]
REF_E = [15.0, 10.0]

def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def make_decision(s, h, a):
    energy_tot = 0.0
    if s < 50.0:
        return 0, 0.0, 0, 0.0, energy_tot
    else:
        h_m = 0.5
        a_m = 1.0
        if h < 1.0:
            h_d = -1
            energy_tot += 5.0
        else:
            h_d = 1
            energy_tot += 3.0

        if a < -0.3:
            a_d = -1
            energy_tot += 2.0
        elif a > 0.3:
            a_d = 1
            energy_tot += 2.0
        else: 
            a_d = 0
            energy_tot += 0.0

        return h_d, h_m, a_d, a_m, -1.0 * energy_tot

REPO = []
def move_rule_horizontal(d, m):
    REPO.append(('h',d,m))
def move_rule_vertical(d, m):
    REPO.append(('v',d,m))

#
# Define Messages
#
belief = Belief('Projectile status', ('speed', 'height', 'angle'))
belief.set_values([100.0, 0.3, 0.2])
direction = Direction('motion', ('horizontal direction', 
                                 'horizontal magnitude',
                                 'vertical direction',
                                 'vertical magnitude'))

#
# Define Scaffold and Map for it
#
agent_resources = Resource('internal_resource', ('internal_energy',))
agent_resources.set_values(20.0)
change_energy = ResourceMap('adjust_energy', 'delta', 'internal_energy', ('expend_energy',))

#
# Define Organs and their associated messages
#
moulder = Moulder('take evasive action?', make_decision, 
                  belief, direction, 
                  change_energy)
splitter_1 = MessageOperator(direction, slice_labels=['horizontal direction', 
                                                      'horizontal magnitude'])
splitter_2 = MessageOperator(direction, slice_labels=['vertical direction', 
                                                      'vertical magnitude'])
actuator1 = Actuator('move left right', move_rule_horizontal, splitter_1)
actuator2 = Actuator('move up down', move_rule_vertical, splitter_2)

#
# Initialize Agent
#
agent = Agent('test_agent', strict_engine=True)
agent.set_organ(moulder)
agent.set_organ(actuator1)
agent.set_organ(actuator2)
agent.set_scaffold(agent_resources)
agent.set_message(belief)

#
# Decide on direction and execute action
#
agent.mould('take evasive action?')
agent.act('move up down')
agent.act('move left right')
assert (agent.resource['internal_energy'] == REF_E[0])
belief.set_values([100.0, 1.3, -0.5])
agent.mould('take evasive action?')
agent.act('move up down')
agent.act('move left right')
assert (agent.resource['internal_energy'] == REF_E[1])
for e1, e2 in zip(REPO, REF_REPO):
    assert(e1 == e2)

try:
    agent.act('move up down')
    raise AssertionError('Action without preceding moulding did not raise exception')
except EmptyFlashError: 
    pass
else:
    raise AssertionError('Action without preceding moulding did not raise expected exception')
try:
    agent.act('move left right')
    raise AssertionError('Action without preceding moulding did not raise exception')
except EmptyFlashError: 
    pass
else:
    raise AssertionError('Action without preceding moulding did not raise expected exception')
