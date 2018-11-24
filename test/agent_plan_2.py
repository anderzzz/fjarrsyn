from core.agent import Agent
from core.message import Buzz, Belief, Direction, Resource, MessageOperator
from core.instructor import Sensor, Interpreter, Moulder, Actuator, Compulsion
from core.plan import Plan
from core.policy import Clause, AutoBeliefCondition, AutoResourceCondition
from core.scaffold_map import ResourceMap

def listen():
    pass

def word_estimator(b1, b2, b3):
    pass

battery = Resource('battery power', ('potential',))
suck_power = ResourceMap('suck power', 'delta', 'battery power', ('reduction',))
b1 = Buzz('sound stimulation', ('band_1', 'band_2', 'band_3'))
s1 = Sensor('sound in surrounding', listen, b1, suck_power)
belief_1 = Belief('The word was spoken', ('probability',))
int1 = Interpreter('Was the word spoken?', word_estimator, b1, belief_1)
dir_1 = Direction('follow up request', ('word_section_1', 'word_section_2',
                                        'word_section_3', 'word_section_4'))
moul1 = Moulder('What response to give', responder, belief_1, dir_1)
a1 = Actuator('loudspeaker vibrations', loudspeaker_api, dir_1, suck_power)
moul2 = Moulder('Select warn statement', warn_statement, None, dir_1,
                resource_op_input=battery)

bc = AutoBeliefCondition('Sufficiently confident of word spoken',
                         lambda p: p > 0.75, 'The word was spoken')
rc = AutoResourceCondition('Sufficient power left',
                           lambda pot: pot > 0.2, 'battery power')
clausul_1 = Clause('listen for the word', 
                   [('sense', 'sound in surrounding'),
                    ('interpret', 'Was the word spoken?')],
                   condition=bc)

clausul_2 = Clause('say something to the user',
                   [('mould', 'What response to give'),
                    ('act', 'loudspeaker vibrations')])
clausul_3 = Clause('power check', condition=rc)
clausul_4 = Clause('power warn', 
                   [('mould', 'Select warn statement'),
                    ('act', 'loudspeaker vibrations')])

plan = Plan('Clever stuff')
plan.add_cargo('pronounce', 'listen for the word')
plan.add_cargo('pronounce', 'say something to the user')
plan.add_cargo('pronounce', 'power check')
plan.add_cargo('pronounce', 'power warm')
plan.add_dependency(3, 0, 4)
plan.add_dependency(0, 1)
plan.add_dependency(1, 2)
