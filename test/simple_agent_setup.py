'''Simple Agent Setup Integration Test

'''
from core.agent import Agent

from core.organs import Sensor, Interpreter
from core.message import Buzz, Belief

import numpy as np
from numpy.random import random_integers

def dice_sensor(agent_index):
    return list(random_integers(1, 6, 5))

def roll_interpreter(current_joy, dice_values):
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

    if current_joy[0] is None:
        joy = 0
    else:
        joy = current_joy[0]

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
sensor = Sensor('test_sensor', 'random_roll', dice_sensor, buzz)
interpreter = Interpreter('good_roll', buzz, roll_interpreter, belief,
                          belief_updater=True)

#
# Initialize Agent
#
agent = Agent('test_agent')
agent.set_organ(sensor)
agent.set_organ(interpreter)

agent.sense('random_roll')
agent.interpret('good_roll')

print (agent.belief)
print (agent.belief['world_is_good'].read_value())
