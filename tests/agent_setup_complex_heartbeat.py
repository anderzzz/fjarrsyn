from fjarrsyn.core.agent import Agent
from fjarrsyn.core.instructor import Interpreter
from fjarrsyn.core.message import Belief, Resource
from fjarrsyn.core.scaffold_map import ResourceMap
from fjarrsyn.core.policy import AutoResourceCondition, Heartbeat

REF_B1 = [1,2,3,3]
REF_I1 = [False, False, False, True]
REF_B2 = [4,5,6,6,6]
REF_I2 = [False, False, False, True, True]

belief = Belief('dummy', ('a1',))
resource = Resource('internal energy', ('level',))
mapper = ResourceMap('eat energy', 'delta', 'level', ('shift',))
interpreter1 = Interpreter('thinker', lambda x: (x + 1, -1), belief, belief,
                           resource_map_output=mapper)
interpreter2 = Interpreter('thinker X', lambda x: (x + 1, -3), belief, belief,
                           resource_map_output=mapper)
battery = AutoResourceCondition('battery left', lambda x: x>0)
heart_1 = Heartbeat('big heart', battery, ticker_arithmetic=lambda : 2, max_ticker=4)
heart_2 = Heartbeat('small heart', battery, ticker_arithmetic=lambda : 1, max_ticker=4)

agent_1 = Agent('A1')
agent_1.set_organs(interpreter1, interpreter2)
belief.set_values([1])
resource.set_values([10])
agent_1.set_message(belief)
agent_1.set_scaffold(resource)
agent_1.set_policies(heart_1, heart_2)

assert (agent_1.belief['dummy'].values()[0] == REF_B1[0])
assert (agent_1.inert == REF_I1[0])
agent_1.pump('big heart')
agent_1.interpret('thinker')
assert (agent_1.belief['dummy'].values()[0] == REF_B1[1])
assert (agent_1.inert == REF_I1[1])
agent_1.pump('big heart')
agent_1.interpret('thinker')
assert (agent_1.belief['dummy'].values()[0] == REF_B1[2])
assert (agent_1.inert == REF_I1[2])
agent_1.pump('big heart')
agent_1.interpret('thinker')
assert (agent_1.belief['dummy'].values()[0] == REF_B1[3])
assert (agent_1.inert == REF_I1[3])

agent_1.revive()
assert (agent_1.inert == False)

agent_1.pump('small heart')
agent_1.interpret('thinker X')
assert (agent_1.belief['dummy'].values()[0] == REF_B2[0])
assert (agent_1.inert == REF_I2[0])
agent_1.pump('small heart')
agent_1.interpret('thinker X')
assert (agent_1.belief['dummy'].values()[0] == REF_B2[1])
assert (agent_1.inert == REF_I2[1])
agent_1.pump('small heart')
agent_1.interpret('thinker X')
assert (agent_1.belief['dummy'].values()[0] == REF_B2[2])
assert (agent_1.inert == REF_I2[2])
agent_1.pump('small heart')
agent_1.interpret('thinker X')
assert (agent_1.belief['dummy'].values()[0] == REF_B2[3])
assert (agent_1.inert == REF_I2[3])
agent_1.pump('small heart')
agent_1.interpret('thinker X')
assert (agent_1.belief['dummy'].values()[0] == REF_B2[4])
assert (agent_1.inert == REF_I2[4])
