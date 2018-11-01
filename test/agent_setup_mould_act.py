'''Simple Agent Setup Integration Test

'''
from core.agent import Agent

from core.organs import Moulder, Actuator 
from core.message import Belief, Direction
from core.scaffold import Resource
from core.naturallaw import ObjectMapOneOne

#
# Define Messages
#
belief = Belief('rich_environment', ['stuff_1, stuff_2, stuff_3, stuff_4'])
direction = Direction('grab_this_much', ['grab_volume'])

#
# Define Scaffold and ObjectMap for it
#
resource_scaffold = Resource(['internal_energy', 'food_storage'])
object_map = ObjectMapOneOne(resource_scaffold, 

#
# Define Organs and their associated messages
#
moulder = Moulder('reach_and_grab', belief, make_decision, direction)
actuator = Actuator('grab_it', direction, grabber, XXX)

#
# Initialize Agent
#
agent = Agent('test_agent')
agent.set_organ(moulder)
agent.set_organ(actuator)
agent.set_scaffold

beliefs = []
for k in range(0, 20):
    agent.sense('random_roll')
    agent.interpret('good_roll')
    beliefs.append(agent.belief['world_is_good'].read_value()[0])

assert (beliefs == REF_OUTCOME)
