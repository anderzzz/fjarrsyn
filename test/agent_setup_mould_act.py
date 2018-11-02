'''Simple Agent Setup Integration Test

'''
from core.agent import Agent

from core.organs import Moulder, Actuator 
from core.message import Belief, Direction
from core.scaffold import Resource, ResourceMap

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

    print (s1, s2, s3, s4)
    print (grab_volume, expend_energy)
    return grab_volume, expend_energy
    
#
# Define Messages
#
belief = Belief('rich_environment', ('stuff_1', 'stuff_2', 'stuff_3', 'stuff_4'))
belief.set_elements([0.7, 0.3, 0.6, 0.1])
direction = Direction('grab_this_much', ('grab_volume',))

#
# Define Scaffold and Map for it
#
agent_resources = Resource('internal_resource', ('internal_energy', 'carrot', 'leek'))
agent_resources.set_elements([100.0, 4, 5])
change_energy = ResourceMap('adjust_energy', ('internal_energy',), ('delta',))
hoard_food = ResourceMap('hoard_food', ('carrot', 'leek'), ('delta', 'delta'))

#
# Define Organs and their associated messages
#
moulder = Moulder('reach_and_grab', belief, make_decision, direction,
                  change_energy)

#actuator = Actuator('grab_it', direction, grabber)

#
# Initialize Agent
#
agent = Agent('test_agent')
agent.set_organ(moulder)
#agent.set_organ(actuator)
agent.set_scaffold(agent_resources)

#
# Decide on direction and execute action
#
agent.mould('reach_and_grab')
print (direction.read_value())
#agent.act('grab_it')

