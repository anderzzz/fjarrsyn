'''Integration test of agent setup of Moulder and Actuator organs including
Resource Maps

'''
from core.agent import Agent

from core.instructor import Moulder, Actuator
from core.message import Belief, Direction, Resource
from core.scaffold_map import ResourceMap, MapCollection 
from core.array import EmptyFlashError

REF_RESOURCE_OUTCOME = [99.0, 5, 7]

def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def make_decision(s1, s2, s3, s4):
    mask = [s > 0.5 for s in [s1, s2, s3, s4]]
    if all(mask):
        grab_volume = 10.0
        expend_energy = -2.0
    elif any(mask):
        grab_volume = 2.0
        expend_energy = -1.0
    else:
        grab_volume = 1.0
        expend_energy = 0.0

    return grab_volume, expend_energy

def shouter(s1, s2, s3, s4):
    return sum([s1, s2, s3, s4])

class Env(object):
    def shout_into_void(self, how_loud):
        self.loud_cumsum += how_loud

    def grabber(self, volume):
        return int(self.conc_carrot * volume), int(self.conc_leek * volume)

    def __init__(self):
        self.loud_cumsum = 0.0
        self.conc_carrot = 0.8
        self.conc_leek = 1.2

#
# Define Messages
#
belief = Belief('rich_environment', ('stuff_1', 'stuff_2', 'stuff_3', 'stuff_4'))
belief.set_values([0.7, 0.3, 0.6, 0.1])
direction1 = Direction('grab_this_much', ('grab_volume',))
direction2 = Direction('shout_loud', ('volume',))

#
# Define Scaffold and Map for it
#
agent_resources = Resource('internal_resource', ('internal_energy', 'carrot', 'leek'))
agent_resources.set_values([100.0, 4, 5])
change_energy = ResourceMap('adjust_energy', 'delta', 'internal_energy', ('expend_energy',))
change_carrot = ResourceMap('adjust_carrot', 'delta', 'carrot', ('tweak_carrot',))
change_leek = ResourceMap('adjust_leek', 'delta', 'leek', ('tweak_leek',))
hoarding_food = MapCollection([change_carrot, change_leek])

#
# Define Organs and their associated messages
#
moulder1 = Moulder('reach_and_grab', make_decision, belief, direction1,
                   change_energy)
moulder2 = Moulder('shout_how_much', shouter, belief, direction2)

env = Env()
actuator1 = Actuator('grab_it', env.grabber, direction1, hoarding_food)
actuator2 = Actuator('shout', env.shout_into_void, direction2)

#
# Initialize Agent
#
agent = Agent('test_agent', True)
agent.set_organ(moulder1)
agent.set_organ(moulder2)
agent.set_organ(actuator1)
agent.set_organ(actuator2)
agent.set_scaffold(agent_resources)

#
# Decide on direction and execute action
#
agent.mould('reach_and_grab')
agent.act('grab_it')

assert (agent.resource.values() == REF_RESOURCE_OUTCOME)

agent.mould('shout_how_much')
agent.act('shout')
agent.mould('shout_how_much')
agent.act('shout')

assert (isclose(env.loud_cumsum, 3.4))

try:
    agent.act('shout')
    raise AssertionError('Action without preceding moulding did not raise exception')
except EmptyFlashError: 
    pass
else:
    raise AssertionError('Action without preceding moulding did not raise expected exception')

