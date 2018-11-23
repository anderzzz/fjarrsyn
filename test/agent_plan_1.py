from core.agent import Agent
from core.instructor import Sensor
from core.message import Buzz
from core.plan import Plan

def s1():
    print ('In s1')
    return 1.0

def s2():
    print ('In s2')
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
plan.make_plan_tree()
plan.enact_upon(agent)
