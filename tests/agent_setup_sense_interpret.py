'''Simple Agent Setup Integration Test of sensor and interpreter operating as a
belief updater

'''
from fjarrsyn.core.agent import Agent

from fjarrsyn.core.instructor import Sensor, Interpreter
from fjarrsyn.core.message import Buzz, Belief

import numpy as np
from numpy.random import random_integers
np.random.seed(79)

REF_OUTCOME = [0, -1, 0, 0, 2, 3, 3, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 4, 3] 

def dice_sensor():
    return list(random_integers(1, 6, 5))

def roll_interpreter(d1, d2, d3, d4, d5, current_joy):
    dice_values = [d1, d2, d3, d4, d5]
    if sum(dice_values) >= 25:
        up = 2
    elif sum(dice_values) >= 20:
        up = 1
    elif sum(dice_values) >= 15:
        up = 0
    elif sum(dice_values) >= 10:
        up = -1
    else:
        up = -2

    if current_joy is None:
        joy = 0
    else:
        joy = current_joy

    new_joy = max(-5, min(5, joy + up))

    return new_joy

#
# Define Messages
#
buzz = Buzz('view_of_dice', ['dice_1', 'dice_2', 'dice_3', 
                             'dice_4', 'dice_5'])
belief = Belief('world_is_good', ['joy_index'])

#
# Define Organs and their associated messages
#
sensor = Sensor('check_roll', dice_sensor, buzz)
interpreter = Interpreter('was_it_good_roll', roll_interpreter, buzz, belief,
                          belief_updater=True)

#
# Initialize Agent
#
agent = Agent('test_agent', strict_engine=True)
agent.set_organ(sensor)
agent.set_organ(interpreter)

beliefs = []
for k in range(0, 20):
    agent.sense('check_roll')
    agent.interpret('was_it_good_roll')
    beliefs.append(agent.belief['world_is_good'].values()[0])

assert (beliefs == REF_OUTCOME)

