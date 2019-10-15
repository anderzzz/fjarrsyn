'''Integration test: simple plan test

'''
import pytest

from fjarrsyn.core.agent import Agent
from fjarrsyn.core.message import Buzz, Belief, Direction, Resource, MessageOperator
from fjarrsyn.core.instructor import Sensor, Interpreter, Moulder, Actuator, Compulsion
from fjarrsyn.core.policy import Plan, Clause, AutoBeliefCondition, AutoResourceCondition
from fjarrsyn.core.scaffold_map import ResourceMap

def listen():
    return 1.0, 2.0, 3.0, -0.1

def word_estimator(b1, b2, b3):
    return 0.90

def responder(prob):
    if prob > 0.95:
        return 'a', 'b', 'c', 'd'
    else:
        return 'a', 'b', 'q', 'r'

def loudspeaker_api(x1, x2, x3, x4):
    pass

def warn_statement(potential):
    return 'Battery left %s' %(str(potential)), 'w', 'w', 'w'

def test_main():

    # Not fully implemented
    assert 1==2

    battery = Resource('battery power', ('potential',))
    battery.set_values(0.401)
    suck_power = ResourceMap('suck power', 'delta', 'potential', ('reduction',))
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
                               lambda pot: pot > 0.2, 'potential')
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
    plan.add_cargo('pronounce', 'power warn')
    plan.add_dependency(2, 0, 3)
    plan.add_dependency(0, 1)
    plan.stamp_and_approve()

    agent = Agent('smart loudspeaker')
    agent.set_organs(s1, int1, moul1, moul2, a1)
    agent.set_messages(b1, belief_1, dir_1)
    agent.set_scaffold(battery)
    agent.set_policies(clausul_1, clausul_2, clausul_3, clausul_4, plan)

    agent.enact('Clever stuff')
    agent.enact('Clever stuff')
    agent.enact('Clever stuff')
    agent.enact('Clever stuff')

    # ADD HEARTBEAT CONDITION ON BATTERY POWER
