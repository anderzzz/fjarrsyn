'''Integration test of AMS where the two agents can sense each others cortices

'''
import numpy as np
import numpy.random
np.random.seed(79)

from fjarrsyn.core.agent_ms import AgentManagementSystem

from fjarrsyn.core.agent import Agent
from fjarrsyn.core.instructor import Sensor, Cortex
from fjarrsyn.core.message import Buzz, Feature, Essence

REF_VALUES = [[('type_sense', 0.50078), ('honesty_sense', 0.5)],
              [('type_sense', 0.50067), ('honesty_sense', 0.2)]]

def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class TestAgentMS(AgentManagementSystem):

    def type_query(self, agent_index):

        neighbours = self.neighbours_to(agent_index)

        the_other_agent = neighbours.pop()
        feature_return = the_other_agent.tickle('my_type')
        
        revealed_type = feature_return['revealed_type']

        if self[agent_index].essence['my_mood'] < 0.25:
            honest_assessment = 0.2
        elif self[agent_index].essence['my_mood'] < 0.55:
            honest_assessment = 0.5
        else:
            honest_assessment = 1.0

        return revealed_type, honest_assessment 

    def __init__(self, name, agents_init):

        super().__init__(name, agents_init)

        for node in self:
            agent = node.agent_content
            buzz = Buzz('type_discovery', ('type_sense', 'honesty_sense'))
            sensor = Sensor('discover_neighbour_type', self.type_query, buzz,
                            agent_id_to_engine=True)
            feature = Feature('revealed_type', ('revealed_type',))
            essence = Essence('who_am_i', ('my_type', 'my_mood'))
            cortex = Cortex('my_type', agent.reveal_type, essence, feature)
            agent.set_organs(sensor, cortex)

            essence.set_values([np.random.random(), np.random.random()])
            agent.set_scaffold(essence)

class TestAgent(Agent):

    def reveal_type(self, the_type, parameter):
        return the_type 


agents_init = [TestAgent('LEFT', strict_engine=True), TestAgent('RIGHT', strict_engine=True)]
agent_ms = TestAgentMS('pair_of_agents', agents_init)

cnt = 0
for node in agent_ms:
    agent = node.agent_content
    agent.sense('discover_neighbour_type')
    the_buzz = agent.buzz['type_discovery']

    xx = the_buzz['type_sense']
    yy = the_buzz['honesty_sense']

    assert (isclose(xx, REF_VALUES[cnt][0][1], abs_tol=0.00001))
    assert (isclose(yy, REF_VALUES[cnt][1][1], abs_tol=0.00001))

    cnt += 1
