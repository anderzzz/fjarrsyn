'''Simple Agent Setup Integration Test of sensor and interpreter operating as a
belief updater

'''
import pytest
from fjarrsyn.core.agent import Agent

from fjarrsyn.core.instructor import Sensor, Interpreter
from fjarrsyn.core.message import Buzz, Belief

ROLLS_OF_FIVE = [[1,4,4,5,3],[4,6,5,5,2],[2,2,1,6,1],[3,4,3,3,1],[6,6,6,6,2]]
REF_OUTCOME = [0, 1, 0, -1, 1]

def dice_sensor():
    return ROLLS_OF_FIVE.pop(0) 

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

def test_main():
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
    for k in range(0, 5):
        agent.sense('check_roll')
        agent.interpret('was_it_good_roll')
        beliefs.append(agent.belief['world_is_good'].values()[0])
    
    assert (beliefs == REF_OUTCOME)

