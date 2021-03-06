'''Integration test: Simple Agent Setup with Plan

'''
import pytest
import numpy as np

from fjarrsyn.core.agent import Agent
from fjarrsyn.core.instructor import Sensor, Interpreter, Moulder, Actuator
from fjarrsyn.core.message import Buzz, Belief, Direction

from fjarrsyn.core.policy import Clause, Heartbeat, AutoBeliefCondition

REF = ['ear','mouth','ear','mouth','ear','mouth','ear','ear','ear',
       'ear','mouth','ear','ear','mouth','ear']

RAND_INTS_FIXED =[[28,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [18,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [43,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [31,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [46,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [30,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [49,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

class Env(object):
    def ear(self):
        self.env_interactions.append('ear')
        ret = [np.sin(np.sqrt(x))**2 for x in RAND_INTS_FIXED.pop(0)]
        print (ret)
        return (ret,)

    def mouth(self, words):
        self.env_interactions.append('mouth')

    def __init__(self):
        self.env_interactions = []

def trigger_word(nerves):
    if nerves[0] > 0.5:
        yup = 0.99
    else:
        yup = 0.01
    return yup

def question_maker(p):
    question = 'Well hello, what can I do for you?'
    return question

N_HEARTS = 10
class SlimAgent(Agent):

    def __call__(self):
        while self.pump('beater'):
            if self.pronounce('sound_trigger'):
                self.pronounce('response_formation')
#        while self.heartbeat(self):
#            if self.clause['sound_trigger'](self):
#                self.clause['response_formation'](self)

    def __init__(self, name):
        super().__init__(name, strict_engine=True)

def test_main():
    # Define Messages
    #
    buzz = Buzz('audio_trigger', (tuple(['a' + str(n) for n in range(1, 20)]),))
    belief = Belief('trigger_spoken', ['probability'])
    direction = Direction('say_this', ['sentence'])

    #
    # Define Organs and their associated messages
    #
    env = Env()
    sensor = Sensor('listen', env.ear, buzz)
    interpreter = Interpreter('was_trigger_word_spoken', trigger_word, buzz, belief)
    moulder = Moulder('follow_up_question', question_maker, belief, direction)
    actuator = Actuator('speak', env.mouth, direction)

    #
    # Autonomous constraints
    #
    belief_condition = AutoBeliefCondition('heard_it', lambda x: x > 0.9, 'trigger_spoken')

    #
    # Plan
    #
    clause_1 = Clause('sound_trigger', [('sense', 'listen'),
                                        ('interpret', 'was_trigger_word_spoken')],
                    condition=belief_condition)
    clause_2 = Clause('response_formation', [('mould', 'follow_up_question'), ('act', 'speak')])
    heart = Heartbeat('beater', max_ticker=N_HEARTS)
    #
    # Initialize Agent
    #
    agent = SlimAgent('test_agent')
    agent.set_organ(sensor)
    agent.set_organ(interpreter)
    agent.set_organ(moulder)
    agent.set_organ(actuator)
    agent.set_policy(clause_1)
    agent.set_policy(clause_2)
    agent.set_policy(heart)

    agent()

    assert (env.env_interactions == REF)
