from core.agent import Agent
from core.instructor import Sensor
from core.message import Buzz
from core.policy import Plan

REF_ORDER = ['s1', 's2']

TEST_ORDER = []

def s1():
    TEST_ORDER.append('s1')
    return 1.0

def s2():
    TEST_ORDER.append('s2')
    return 2.0

buzz_1 = Buzz('B1', ('value',))
sensor_1 = Sensor('S1', s1, buzz_1)
buzz_2 = Buzz('B2', ('value',))
sensor_2 = Sensor('S2', s2, buzz_2)

agent = Agent('test', strict_engine=True)
agent.set_organs(sensor_1, sensor_2)
agent.set_messages(buzz_1, buzz_2)

plan = Plan('silly simple')
plan.add_cargo('sense', 'S1')
plan.add_cargo('sense', 'S2')
plan.add_dependency(0, 1)
plan.stamp_and_approve()
plan.enacted_by(agent)

assert (TEST_ORDER == REF_ORDER)
assert (buzz_1.values() == [1.0])
assert (buzz_2.values() == [2.0])
