'''Integration test of agent setup including all organs from start to finish

'''
import pytest

from fjarrsyn.core.instructor import Sensor, Interpreter, Moulder, Actuator, Cortex
from fjarrsyn.core.message import Buzz, Direction, Belief, Feature
from fjarrsyn.core.agent import Agent

FLOAT_POOL = [0.5006681263403812, 0.4680674259481151, 0.5007825256422324, 0.14917816545210816, 0.820277935819415]

REF = ['Well Gee Maybe', 'Well Gee Maybe', 'Well Gee Maybe', 'Well Oh No', 'Well Oh Yes']

def smeller():
    ENV_STATE = FLOAT_POOL.pop(0)
    if ENV_STATE < 0.25:
        x1 = 0.0
        x2 = 0.0
    elif ENV_STATE < 0.75:
        x1 = 1.0
        x2 = 0.0
    else:
        x1 = 1.0
        x2 = 1.0
    return x1, x2

def nerve_analyzer(n1, n2):
    return (1.0 + n1)**2 + (1.0 + n2)**2

def word_smith(mood_intensity):
    if mood_intensity < 2.1:
        first_word = 'Oh'
        second_word = 'No'
    elif mood_intensity < 5.1:
        first_word = 'Gee'
        second_word = 'Maybe'
    else:
        first_word = 'Oh'
        second_word = 'Yes'
    return first_word, second_word

ENV_SPOKEN = []
def speak(w1, w2, well):
    if well:
        ENV_SPOKEN.append('Well ' + w1 + ' ' + w2)
    else:
        ENV_SPOKEN.append(w1 + ' ' + w2)

def read_env():
    return ENV_SPOKEN

def test_main():

    buzz = Buzz('nose_tingle', ['nerve_1', 'nerve_2'])
    sensor = Sensor('smell_the_roses', smeller, buzz)
    belief = Belief('world_blossoms', ['certainty'])
    interpreter = Interpreter('does_the_world_blossom', nerve_analyzer, buzz, belief)
    direction = Direction('words_to_say', ['first_word','second_word'])
    moulder = Moulder('what_to_say', word_smith, belief, direction)
    actuator = Actuator('say_it', speak, direction,
                        actuator_func_kwargs={'well' : True})

    agent = Agent('simple human', strict_engine=True)
    agent.set_organs(sensor, interpreter, moulder, actuator)

    agent.sense('smell_the_roses')
    agent.interpret('does_the_world_blossom')
    agent.mould('what_to_say')
    agent.act('say_it')

    agent.sense('smell_the_roses')
    agent.interpret('does_the_world_blossom')
    agent.mould('what_to_say')
    agent.act('say_it')

    agent.sense('smell_the_roses')
    agent.interpret('does_the_world_blossom')
    agent.mould('what_to_say')
    agent.act('say_it')

    agent.sense('smell_the_roses')
    agent.interpret('does_the_world_blossom')
    agent.mould('what_to_say')
    agent.act('say_it')

    agent.sense('smell_the_roses')
    agent.interpret('does_the_world_blossom')
    agent.mould('what_to_say')
    agent.act('say_it')

    assert (read_env() == REF)
