'''Integration test of agent setup including all organs from start to finish

'''
from core.instructor import Sensor, Interpreter, Moulder, Actuator, Cortex
from core.message import Buzz, Direction, Belief, Feature
from core.agent import Agent

import numpy as np
import numpy.random
np.random.seed(79)

REF = ['Well Gee Maybe', 'Well Gee Maybe', 'Well Gee Maybe', 'Well Oh No', 'Well Oh Yes']

def smeller(agent_index):
    ENV_STATE = np.random.random()
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

def speak(w1, w2, well, agent_index):
    if well:
        ENV_SPOKEN.append('Well ' + w1 + ' ' + w2)
    else:
        ENV_SPOKEN.append(w1 + ' ' + w2)

buzz = Buzz('nose_tingle', ['nerve_1', 'nerve_2'])
sensor = Sensor('smell_the_roses', smeller, buzz)
belief = Belief('world_blossoms', ['certainty'])
interpreter = Interpreter('does_the_world_blossom', nerve_analyzer, buzz, belief)
direction = Direction('words_to_say', ['first_word','second_word'])
moulder = Moulder('what_to_say', word_smith, belief, direction)
actuator = Actuator('say_it', speak, direction, 
                    actuator_func_kwargs={'well' : True})

agent = Agent('simple human')
agent.set_organs(sensor, interpreter, moulder, actuator)

ENV_SPOKEN = []
agent.engage(['smell_the_roses','does_the_world_blossom','what_to_say','say_it'])
assert (ENV_SPOKEN[0] == REF[0])
ENV_SPOKEN = []
agent.engage(['smell_the_roses','does_the_world_blossom','what_to_say','say_it'])
assert (ENV_SPOKEN[0] == REF[1])
ENV_SPOKEN = []
agent.engage(['smell_the_roses','does_the_world_blossom','what_to_say','say_it'])
assert (ENV_SPOKEN[0] == REF[2])
ENV_SPOKEN = []
agent.engage(['smell_the_roses','does_the_world_blossom','what_to_say','say_it'])
assert (ENV_SPOKEN[0] == REF[3])
ENV_SPOKEN = []
agent.engage(['smell_the_roses','does_the_world_blossom','what_to_say','say_it'])
assert (ENV_SPOKEN[0] == REF[4])
